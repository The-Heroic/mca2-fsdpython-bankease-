from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BillerDirectory, BillPayment, CustomerBiller
from .serializers import (
    BillerDirectorySerializer,
    BillPaymentSerializer,
    CustomerBillerSerializer,
    ExecuteBillPaySerializer,
)


class BillerDirectoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = BillerDirectory.objects.filter(is_active=True)
        cat = request.query_params.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return Response(BillerDirectorySerializer(qs, many=True).data, status=status.HTTP_200_OK)


class CustomerBillerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = CustomerBiller.objects.select_related('biller').filter(user=request.user)
        return Response(CustomerBillerSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerBillerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cb = serializer.save()
        return Response(CustomerBillerSerializer(cb).data, status=status.HTTP_201_CREATED)


class ExecuteBillPayView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ExecuteBillPaySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(
            {
                'message': 'Bill paid successfully.',
                'payment': BillPaymentSerializer(payment).data,
            },
            status=status.HTTP_201_CREATED,
        )


class BillPaymentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = BillPayment.objects.select_related(
            'customer_biller__biller', 'account'
        ).filter(customer_biller__user=request.user)
        return Response(BillPaymentSerializer(qs, many=True).data, status=status.HTTP_200_OK)
