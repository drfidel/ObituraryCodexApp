from rest_framework import serializers
from .models import DoctorObituary, FuneralEvent, PhotoGalleryItem


class FuneralEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuneralEvent
        fields = "__all__"


class PhotoGalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoGalleryItem
        fields = "__all__"


class DoctorObituarySerializer(serializers.ModelSerializer):
    events = FuneralEventSerializer(many=True, read_only=True)
    photos = PhotoGalleryItemSerializer(many=True, read_only=True)

    class Meta:
        model = DoctorObituary
        fields = "__all__"
        read_only_fields = ["slug", "page_views", "created_at"]
