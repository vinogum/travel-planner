from rest_framework import viewsets, exceptions

from apps.projects.models import Place, TravelProject
from apps.projects.serializers import (
    PlaceReadSerializer,
    PlaceWriteSerializer,
    TravelProjectReadSerializer,
    TravelProjectWriteSerializer,
)


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TravelProjectReadSerializer
        return TravelProjectWriteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.places.filter(is_visited=True).exists():
            raise exceptions.ValidationError(
                {"detail": "Cannot delete a project that has visited places."}
            )
        return super().destroy(request, *args, **kwargs)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.none()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PlaceReadSerializer
        return PlaceWriteSerializer

    def get_queryset(self):
        return Place.objects.filter(project_id=self.kwargs["travel_project_pk"])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["travel_project_pk"])
