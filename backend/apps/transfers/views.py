from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Beneficiary, Transaction
from .serializers import (
    BeneficiarySerializer,
    ExecuteTransferSerializer,
    TransactionSerializer,
)


class BeneficiaryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Beneficiary.objects.filter(user=request.user)
        return Response(BeneficiarySerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        cooling = int(request.data.get('cooling_minutes', 0))
        serializer = BeneficiarySerializer(
            data=request.data,
            context={'request': request, 'cooling_minutes': cooling},
        )
        serializer.is_valid(raise_exception=True)
        beneficiary = serializer.save()
        return Response(BeneficiarySerializer(beneficiary).data, status=status.HTTP_201_CREATED)


class BeneficiaryActivateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, beneficiary_id):
        beneficiary = get_object_or_404(Beneficiary, beneficiary_id=beneficiary_id, user=request.user)
        beneficiary.status = 'ACTIVE'
        beneficiary.is_verified = True
        beneficiary.cooling_ends_at = timezone.now()
        beneficiary.save(update_fields=['status', 'is_verified', 'cooling_ends_at'])
        return Response(BeneficiarySerializer(beneficiary).data, status=status.HTTP_200_OK)


class ExecuteTransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ExecuteTransferSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        tx = serializer.save()
        return Response(
            {
                'message': 'Transfer executed successfully.',
                'transaction': TransactionSerializer(tx).data,
            },
            status=status.HTTP_201_CREATED,
        )


class TransferHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role.role_code in ('ADMIN', 'BANK_OFFICER', 'AUDITOR'):
            qs = Transaction.objects.select_related('account', 'beneficiary').all()[:100]
        else:
            qs = Transaction.objects.select_related('account', 'beneficiary').filter(
                account__user=user
            )[:100]
        return Response(TransactionSerializer(qs, many=True).data, status=status.HTTP_200_OK)
