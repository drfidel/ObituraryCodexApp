from rest_framework.routers import DefaultRouter
from .views import DoctorObituaryViewSet, FuneralEventViewSet

router = DefaultRouter()
router.register(r"", DoctorObituaryViewSet, basename="obituary")
router.register(r"events", FuneralEventViewSet, basename="event")

urlpatterns = router.urls
