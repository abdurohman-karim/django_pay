from django.urls import path
from .views import (
    TransactionCreateView,
    TransactionConfirmView,
    TransactionCancelView,
    TransactionHistoryView
)

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('confirm/', TransactionConfirmView.as_view(), name='transaction-confirm'),
    path('cancel/', TransactionCancelView.as_view(), name='transaction-cancel'),
    path('history/', TransactionHistoryView.as_view(), name='transaction-history'),
]
