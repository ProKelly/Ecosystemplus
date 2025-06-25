from rest_framework import viewsets, permissions
from base.models import Farm
from api.serializers import FarmSerializer

class IsFarmOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user

class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'community':
            # Community admin: see all farms in their community
            return Farm.objects.filter(community=user.administered_community)
        return Farm.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Assign the farm to the currently logged-in user
        user = self.request.user
        community = user.administered_community if user.role == 'community' else None
        serializer.save(owner=user, community=community)
