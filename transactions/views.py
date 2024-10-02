from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Transaction
from .serializers import TransactionCreateSerializer, TransactionConfirmSerializer, TransactionCancelSerializer, TransactionHistorySerializer
import random
from django.utils import timezone


class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=request.user, status='pending')
            # Генерация OTP
            transaction.otp = str(random.randint(100000, 999999))
            transaction.save()
            return Response({
                'transaction_id': transaction.id,
                'status': transaction.status,
                'otp': transaction.otp  # Возвращаем OTP
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = Transaction.objects.get(id=serializer.validated_data['transaction_id'], user=request.user)
                if transaction.otp == serializer.validated_data['otp']:
                    transaction.status = 'confirmed'
                    transaction.save()
                    return Response({'status': 'confirmed'}, status=status.HTTP_200_OK)
                else:
                    transaction.status = 'failed'
                    transaction.save()
                    return Response({'status': 'failed', 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except Transaction.DoesNotExist:
                return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionCancelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = Transaction.objects.get(id=serializer.validated_data['transaction_id'], user=request.user)
                transaction.status = 'cancelled'
                transaction.save()
                return Response({'status': 'cancelled'}, status=status.HTTP_200_OK)
            except Transaction.DoesNotExist:
                return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.GET.get('status')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        transactions = Transaction.objects.filter(user=request.user)

        if status_filter:
            transactions = transactions.filter(status=status_filter)

        if date_from and date_to:
            try:
                date_from_dt = timezone.datetime.fromisoformat(date_from)
                date_to_dt = timezone.datetime.fromisoformat(date_to)

                transactions = transactions.filter(created_at__range=[date_from_dt, date_to_dt])
            except ValueError:
                return Response({"error": "Invalid date format."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)
