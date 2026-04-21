from rest_framework import serializers
from .models import CondolenceMessage, Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        read_only_fields = ["user"]


class CondolenceMessageSerializer(serializers.ModelSerializer):
    reactions = ReactionSerializer(many=True, read_only=True)

    class Meta:
        model = CondolenceMessage
        fields = "__all__"
        read_only_fields = ["user", "is_approved"]
