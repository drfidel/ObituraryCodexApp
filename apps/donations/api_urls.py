from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, PayoutRequestViewSet, flutterwave_webhook

router = DefaultRouter()
router.register(r"", DonationViewSet, basename="donations")
router.register(r"payouts", PayoutRequestViewSet, basename="payouts")

urlpatterns = [path("webhooks/flutterwave/", flutterwave_webhook, name="flutterwave_webhook")] + router.urls
