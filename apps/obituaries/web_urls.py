from django.urls import path
from .views import obituary_detail, obituary_list

urlpatterns = [
    path("", obituary_list, name="obituary_list"),
    path("tribute/<slug:slug>/", obituary_detail, name="obituary_detail"),
]
