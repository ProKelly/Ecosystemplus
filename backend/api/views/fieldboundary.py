from rest_framework import viewsets, permissions
from base.models import FieldBoundary
from api.serializers import FieldBoundarySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from api.utils import analyze_soil
from rest_framework.exceptions import PermissionDenied

class IsFarmOwnerForField(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.farm.owner == request.user

class FieldBoundaryViewSet(viewsets.ModelViewSet):
    serializer_class = FieldBoundarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'community':
            # Community can see all field boundaries of all farms in their territory
            return FieldBoundary.objects.filter(farm__community=user.administered_community)
        return FieldBoundary.objects.filter(farm__owner=user)

    def perform_create(self, serializer):
        farm = serializer.validated_data.get('farm')
        if farm.owner != self.request.user:
            raise PermissionDenied("You do not own this farm.")

        field = serializer.save()

        # After saving, call the GEE + FAO integration using the field's boundary
        soil_data = analyze_soil(field.boundary.geojson)
        
        # Update the field with external data
        for key, value in soil_data.items():
            setattr(field, key, value)
        field.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reanalyze(self, request, pk=None):
        field = self.get_object()
        if field.farm.owner != request.user:
            raise PermissionDenied("You do not own this field.")

        soil_data = analyze_soil(field.boundary.geojson)
        for key, value in soil_data.items():
            setattr(field, key, value)
        field.save()

        return Response({"status": "updated", "data": FieldBoundarySerializer(field).data})
