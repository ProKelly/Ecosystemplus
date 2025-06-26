from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import FieldBoundaryViewSet

router = DefaultRouter()
router.register(r'field-boundaries', FieldBoundaryViewSet, basename='fieldboundary')

urlpatterns = [
    path('', include(router.urls)),
]