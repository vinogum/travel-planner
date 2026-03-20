from django.urls import path, include
from rest_framework_nested import routers
from .views import TravelProjectViewSet, PlaceViewSet

router = routers.DefaultRouter()
router.register(r"travel-projects", TravelProjectViewSet, basename="travel-project")

projects_router = routers.NestedSimpleRouter(
    router, r"travel-projects", lookup="travel_project"
)
projects_router.register(r"places", PlaceViewSet, basename="travel-project-places")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(projects_router.urls)),
]
