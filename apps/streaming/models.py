from django.db import models


class Video(models.Model):
    class Type(models.TextChoices):
        UPLOAD = "upload", "Upload"
        YOUTUBE = "youtube", "YouTube Live"
        VIMEO = "vimeo", "Vimeo"
        WEBRTC = "webrtc", "WebRTC"

    obituary = models.ForeignKey("obituaries.DoctorObituary", on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_type = models.CharField(max_length=20, choices=Type.choices)
    video_file = models.FileField(upload_to="videos/uploads/", null=True, blank=True)
    external_url = models.URLField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
