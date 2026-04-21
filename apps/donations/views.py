import json
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Donation, PayoutRequest
from .payments import verify_flutterwave_signature
from .serializers import DonationSerializer, PayoutRequestSerializer


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.select_related("obituary", "donor")
    serializer_class = DonationSerializer

    @action(detail=False, methods=["get"], url_path="obituary/(?P<obituary_id>[^/.]+)/summary")
    def obituary_summary(self, request, obituary_id=None):
        queryset = self.queryset.filter(obituary_id=obituary_id, status=Donation.Status.SUCCESS)
        total = queryset.aggregate(total=Sum("amount"))["total"] or 0
        recent = queryset.order_by("-created_at")[:10]
        return Response({"total": total, "recent": DonationSerializer(recent, many=True).data})


class PayoutRequestViewSet(viewsets.ModelViewSet):
    queryset = PayoutRequest.objects.select_related("obituary", "requested_by")
    serializer_class = PayoutRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def flutterwave_webhook(request):
    signature = request.headers.get("verif-hash", "")
    raw_body = request.body
    if not verify_flutterwave_signature(raw_body, signature):
        return HttpResponseBadRequest("Invalid signature")

    payload = json.loads(raw_body.decode("utf-8"))
    tx_ref = payload.get("data", {}).get("tx_ref")
    status = payload.get("data", {}).get("status")
    if tx_ref:
        Donation.objects.filter(provider_reference=tx_ref).update(
            status=Donation.Status.SUCCESS if status == "successful" else Donation.Status.FAILED
        )
    return Response({"ok": True})
