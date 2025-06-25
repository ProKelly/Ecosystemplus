from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import FarmViewSet

router = DefaultRouter()
router.register(r'farms/', FarmViewSet, basename='farm')

urlpatterns = [
    path('', include(router.urls)),
]