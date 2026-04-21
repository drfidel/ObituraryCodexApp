from django.conf import settings
from django.db import models


class CondolenceMessage(models.Model):
    obituary = models.ForeignKey("obituaries.DoctorObituary", on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="condolence_messages")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    image = models.ImageField(upload_to="messages/images/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Reaction(models.Model):
    class Kind(models.TextChoices):
        PRAYER = "prayer", "Prayer"
        HEART = "heart", "Heart"
        SUPPORT = "support", "Support"

    message = models.ForeignKey(CondolenceMessage, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=Kind.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "user", "kind")
