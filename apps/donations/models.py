from django.conf import settings
from django.db import models


class Donation(models.Model):
    class Provider(models.TextChoices):
        FLUTTERWAVE = "flutterwave", "Flutterwave"
        MTN_MOMO = "mtn_momo", "MTN MoMo"
        AIRTEL_MONEY = "airtel_money", "Airtel Money"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    obituary = models.ForeignKey("obituaries.DoctorObituary", on_delete=models.CASCADE, related_name="donations")
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="UGX")
    provider = models.CharField(max_length=30, choices=Provider.choices)
    provider_reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class PayoutRequest(models.Model):
    obituary = models.ForeignKey("obituaries.DoctorObituary", on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
