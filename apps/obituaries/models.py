from django.conf import settings
from django.db import models
from django.utils.text import slugify


class DoctorObituary(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_obituaries")
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    photo = models.ImageField(upload_to="obituaries/photos/", blank=True, null=True)
    specialty = models.CharField(max_length=255)
    hospital_affiliations = models.TextField()
    biography = models.TextField()
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    funeral_location = models.CharField(max_length=255)
    funeral_date = models.DateTimeField()
    funeral_map_url = models.URLField(blank=True)
    page_views = models.PositiveIntegerField(default=0)
    seo_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class FuneralEvent(models.Model):
    obituary = models.ForeignKey(DoctorObituary, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    map_url = models.URLField(blank=True)

    class Meta:
        ordering = ["starts_at"]


class PhotoGalleryItem(models.Model):
    obituary = models.ForeignKey(DoctorObituary, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="obituaries/gallery/")
    caption = models.CharField(max_length=255, blank=True)
