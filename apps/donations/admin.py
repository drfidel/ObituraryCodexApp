from django.contrib import admin
from .models import Donation, PayoutRequest

admin.site.register(Donation)
admin.site.register(PayoutRequest)
