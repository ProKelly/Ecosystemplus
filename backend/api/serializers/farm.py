from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from base.models import Farm
from .fieldboundary import FieldBoundarySerializer  # if using modular files

class FarmSerializer(GeoFeatureModelSerializer):
    field_boundaries = FieldBoundarySerializer(many=True, read_only=True)

    class Meta:
        model = Farm
        geo_field = 'coordinates'  # The farm polygon
        fields = [
            'uuid', 'name', 'coordinates', 'owner',
            'community', 'created_at', 'field_boundaries'
        ]
        read_only_fields = ['uuid', 'created_at']
