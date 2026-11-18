import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction as db_tx
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.banking_accounts.models import BankAccount
from apps.transfers.models import Transaction
from .models import Investment, InvestmentPlan
from .serializers import (
    CreateInvestmentSerializer,
    InvestmentPlanSerializer,
    InvestmentSerializer,
)


class InvestmentPlanListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        plans = InvestmentPlan.objects.filter(is_active=True)
        return Response(InvestmentPlanSerializer(plans, many=True).data, status=status.HTTP_200_OK)


class InvestmentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Investment.objects.select_related('plan', 'funding_account').filter(user=request.user)
        return Response(InvestmentSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateInvestmentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        inv = serializer.save()
        return Response(InvestmentSerializer(inv).data, status=status.HTTP_201_CREATED)


class InvestmentCloseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, investment_id):
        inv = get_object_or_404(
            Investment.objects.select_related('plan', 'funding_account'),
            investment_id=investment_id,
            user=request.user,
        )
        if inv.investment_status != 'ACTIVE':
            return Response(
                {'detail': f'Investment is already {inv.investment_status}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.localdate()
        is_mature = today >= inv.maturity_date
        if is_mature:
            payout = inv.projected_maturity_amount
            new_status = 'MATURED'
        else:
            # Return principal minus premature penalty on accrued return (or 0.5% flat demo payout)
            penalty = (inv.principal_amount * (inv.plan.premature_penalty_pct / Decimal('100'))).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            payout = max(Decimal('0.00'), inv.principal_amount - penalty)
            new_status = 'PREMATURE_CLOSED'

        with db_tx.atomic():
            acc = BankAccount.objects.select_for_update().get(account_id=inv.funding_account_id)
            acc.balance += payout
            acc.save(update_fields=['balance', 'updated_at'])

            inv.investment_status = new_status
            inv.save(update_fields=['investment_status'])

            Transaction.objects.create(
                account=acc,
                reference_utr=f'BNKIP{timezone.now().strftime("%Y%m%d")}{uuid.uuid4().hex[:8].upper()}',
                transaction_type='CREDIT',
                channel='INVESTMENT',
                amount=payout,
                balance_after=acc.balance,
                description=f'Investment Payout {inv.certificate_number} ({new_status})',
                status='SUCCESS',
                initiated_ip=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            )

        return Response(
            {'message': f'Investment {new_status} with payout ₹{payout}.', 'investment': InvestmentSerializer(inv).data},
            status=status.HTTP_200_OK,
        )
