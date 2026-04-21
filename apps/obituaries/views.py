from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DoctorObituary, FuneralEvent
from .permissions import IsOrganizerOrAdminOrReadOnly
from .serializers import DoctorObituarySerializer, FuneralEventSerializer


class DoctorObituaryViewSet(viewsets.ModelViewSet):
    queryset = DoctorObituary.objects.select_related("organizer").prefetch_related("events", "photos")
    serializer_class = DoctorObituarySerializer
    permission_classes = [IsOrganizerOrAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "specialty", "hospital_affiliations"]
    ordering_fields = ["date_of_death", "created_at"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        if year:
            queryset = queryset.filter(date_of_death__year=year)
        if month:
            queryset = queryset.filter(date_of_death__month=month)
        return queryset

    @action(detail=True, methods=["post"])
    def increment_view(self, request, pk=None):
        obituary = self.get_object()
        obituary.page_views += 1
        obituary.save(update_fields=["page_views"])
        return Response({"page_views": obituary.page_views})


class FuneralEventViewSet(viewsets.ModelViewSet):
    queryset = FuneralEvent.objects.all()
    serializer_class = FuneralEventSerializer


def obituary_detail(request, slug):
    obituary = get_object_or_404(DoctorObituary.objects.prefetch_related("events", "photos"), slug=slug)
    next_event = obituary.events.filter(starts_at__gte=timezone.now()).first()
    return render(request, "obituaries/detail.html", {"obituary": obituary, "next_event": next_event})


def obituary_list(request):
    query = request.GET.get("q", "")
    obituaries = DoctorObituary.objects.all()
    if query:
        obituaries = obituaries.filter(
            Q(full_name__icontains=query)
            | Q(specialty__icontains=query)
            | Q(hospital_affiliations__icontains=query)
        )
    return render(request, "obituaries/list.html", {"obituaries": obituaries, "query": query})
