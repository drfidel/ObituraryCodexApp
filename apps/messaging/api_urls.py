from rest_framework.routers import DefaultRouter
from .views import CondolenceMessageViewSet, ReactionViewSet

router = DefaultRouter()
router.register(r"", CondolenceMessageViewSet, basename="messages")
router.register(r"reactions", ReactionViewSet, basename="reactions")

urlpatterns = router.urls
