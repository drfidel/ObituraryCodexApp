from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("apps.accounts.api_urls")),
    path("api/obituaries/", include("apps.obituaries.api_urls")),
    path("api/messages/", include("apps.messaging.api_urls")),
    path("api/donations/", include("apps.donations.api_urls")),
    path("api/streaming/", include("apps.streaming.api_urls")),
    path("", include("apps.obituaries.web_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
