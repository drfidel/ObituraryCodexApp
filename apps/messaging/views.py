from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CondolenceMessage, Reaction
from .serializers import CondolenceMessageSerializer, ReactionSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class CondolenceMessageViewSet(viewsets.ModelViewSet):
    serializer_class = CondolenceMessageSerializer

    def get_queryset(self):
        qs = CondolenceMessage.objects.select_related("user", "obituary", "parent")
        if self.request.user.is_staff:
            return qs
        return qs.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        message = self.get_object()
        message.is_approved = True
        message.save(update_fields=["is_approved"])
        return Response({"approved": True})


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
