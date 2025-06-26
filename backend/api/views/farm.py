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
        community_uuid = self.request.query_params.get('community')
        user = self.request.user
        print(f"[DEBUG] community_uuid param: {community_uuid}, user: {user}, user.role: {getattr(user, 'role', None)}")
        if community_uuid:
            qs = Farm.objects.filter(community__uuid=community_uuid)
            print(f"[DEBUG] Farms for community {community_uuid}: {[f.uuid for f in qs]}")
            return qs
        if user.role == 'community':
            qs = Farm.objects.filter(community=user.administered_community)
            print(f"[DEBUG] Farms for community admin {user}: {[f.uuid for f in qs]}")
            return qs
        qs = Farm.objects.filter(owner=user)
        print(f"[DEBUG] Farms for user {user}: {[f.uuid for f in qs]}")
        return qs

    def perform_create(self, serializer):
        # Assign the farm to the currently logged-in user
        user = self.request.user
        community = user.administered_community if user.role == 'community' else None
        serializer.save(owner=user, community=community)
