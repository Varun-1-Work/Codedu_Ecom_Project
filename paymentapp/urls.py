from django.urls import path
from . import views

urlpatterns = [
    path("start-payment/", views.start_payment, name="start-payment"),
    path("success/", views.payment_success, name="payment-success"),
]
