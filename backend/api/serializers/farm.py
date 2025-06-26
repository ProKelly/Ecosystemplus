from rest_framework_gis.serializers import GeometryField
from rest_framework import serializers
from base.models import Farm
from .fieldboundary import FieldBoundarySerializer  # if using modular files

class FarmSerializer(serializers.ModelSerializer):
    coordinates = GeometryField()
    field_boundaries = FieldBoundarySerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Farm
        fields = [
            'uuid', 'name', 'coordinates', 'owner',
            'community', 'created_at', 'field_boundaries'
        ]
        read_only_fields = ['uuid', 'created_at']