from django.contrib import admin
from .models import DoctorObituary, FuneralEvent, PhotoGalleryItem


class FuneralEventInline(admin.TabularInline):
    model = FuneralEvent
    extra = 1


@admin.register(DoctorObituary)
class DoctorObituaryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("full_name",)}
    list_display = ("full_name", "specialty", "date_of_death", "page_views")
    search_fields = ("full_name", "specialty", "hospital_affiliations")
    inlines = [FuneralEventInline]


admin.site.register(PhotoGalleryItem)
