from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts_auth.views import IsBankOfficerOrAdmin
from apps.transfers.models import Transaction
from apps.transfers.serializers import TransactionSerializer
from .models import BankAccount
from .serializers import (
    BankAccountSerializer,
    OpenAccountSerializer,
    UpdateAccountStatusSerializer,
)


class AccountListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role.role_code in ('ADMIN', 'BANK_OFFICER', 'AUDITOR'):
            qs = BankAccount.objects.select_related('user', 'branch').all()
        else:
            qs = BankAccount.objects.select_related('user', 'branch').filter(user=user)

        acc_status = request.query_params.get('status')
        if acc_status:
            qs = qs.filter(account_status=acc_status)

        return Response(BankAccountSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OpenAccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        return Response(BankAccountSerializer(account).data, status=status.HTTP_201_CREATED)


class AccountDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        account = get_object_or_404(BankAccount.objects.select_related('user', 'branch'), account_id=account_id)
        if request.user.role.role_code not in ('ADMIN', 'BANK_OFFICER', 'AUDITOR') and account.user_id != request.user.user_id:
            return Response({'detail': 'Not authorized to view this account.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(BankAccountSerializer(account).data, status=status.HTTP_200_OK)


class AccountStatusUpdateView(APIView):
    permission_classes = [IsBankOfficerOrAdmin]

    def patch(self, request, account_id):
        account = get_object_or_404(BankAccount, account_id=account_id)
        serializer = UpdateAccountStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['account_status']
        account.account_status = new_status
        if new_status == 'CLOSED':
            account.closed_at = timezone.localdate()
        if new_status == 'ACTIVE' and account.user.kyc_status != 'VERIFIED':
            account.user.kyc_status = 'VERIFIED'
            account.user.save(update_fields=['kyc_status'])

        account.save(update_fields=['account_status', 'closed_at', 'updated_at'])
        return Response(BankAccountSerializer(account).data, status=status.HTTP_200_OK)


class AccountStatementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        account = get_object_or_404(BankAccount, account_id=account_id)
        if request.user.role.role_code not in ('ADMIN', 'BANK_OFFICER', 'AUDITOR') and account.user_id != request.user.user_id:
            return Response({'detail': 'Not authorized to view this statement.'}, status=status.HTTP_403_FORBIDDEN)

        qs = Transaction.objects.filter(account=account).order_by('-transaction_date', '-transaction_id')
        tx_type = request.query_params.get('type')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        if tx_type in ('DEBIT', 'CREDIT'):
            qs = qs.filter(transaction_type=tx_type)
        if from_date:
            qs = qs.filter(transaction_date__date__gte=from_date)
        if to_date:
            qs = qs.filter(transaction_date__date__lte=to_date)

        return Response(
            {
                'account': BankAccountSerializer(account).data,
                'transactions': TransactionSerializer(qs, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
