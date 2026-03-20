from rest_framework import serializers

from apps.projects.models import Place, TravelProject
from apps.projects.services import check_artwork_exists


# ──────────────────────────────────────────────
# Validators
# ──────────────────────────────────────────────


def validate_artwork_external_id(value: str) -> str:
    if not check_artwork_exists(value):
        raise serializers.ValidationError(
            "This artwork does not exist in the Art Institute."
        )
    return value


# ──────────────────────────────────────────────
# Place
# ──────────────────────────────────────────────


class PlaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "external_id", "notes", "is_visited"]
        read_only_fields = fields


class PlaceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "external_id", "notes", "is_visited"]
        read_only_fields = ["id"]

    def validate_external_id(self, value: str) -> str:
        if self.instance:
            if str(value) != str(self.instance.external_id):
                raise serializers.ValidationError(
                    "Changing external_id is not allowed."
                )
            return value

        return validate_artwork_external_id(value)

    def validate(self, attrs: dict) -> dict:
        view = self.context.get("view")

        if not (
            view and hasattr(view, "kwargs") and "travel_project_pk" in view.kwargs
        ):
            return attrs

        project_id = view.kwargs["travel_project_pk"]
        project = TravelProject.objects.filter(pk=project_id).first()

        if project is None:
            raise serializers.ValidationError("Project not found.")

        if not self.instance:
            if project.places.count() >= 10:
                raise serializers.ValidationError(
                    "A project can have at most 10 places."
                )

            external_id = attrs.get("external_id")
            if Place.objects.filter(
                project_id=project_id, external_id=external_id
            ).exists():
                raise serializers.ValidationError(
                    {"external_id": "This place is already in the project."}
                )

        return attrs


# ──────────────────────────────────────────────
# TravelProject
# ──────────────────────────────────────────────


class TravelProjectReadSerializer(serializers.ModelSerializer):
    places = PlaceReadSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = ("id", "name", "description", "start_date", "is_completed", "places")
        read_only_fields = fields


class TravelProjectWriteSerializer(serializers.ModelSerializer):
    places = PlaceWriteSerializer(many=True, required=False, allow_empty=False)

    class Meta:
        model = TravelProject
        fields = ("id", "name", "description", "start_date", "places")
        read_only_fields = ("id",)

    def validate_places(self, value: list[dict]) -> list[dict]:
        if len(value) > 10:
            raise serializers.ValidationError("A project can have at most 10 places.")

        external_ids = [p["external_id"] for p in value if "external_id" in p]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError(
                "Duplicate places in the request are not allowed."
            )

        return value

    def create(self, validated_data: dict) -> TravelProject:
        places_data = validated_data.pop("places", [])
        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            Place.objects.create(project=project, **place_data)

        return project

    def update(self, instance: TravelProject, validated_data: dict) -> TravelProject:
        validated_data.pop("places", None)
        return super().update(instance, validated_data)
