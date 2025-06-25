from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from base.models import FieldBoundary

class FieldBoundarySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FieldBoundary
        geo_field = 'boundary'  # The PolygonField
        fields = [
            'uuid', 'farm', 'boundary', 'area_hectares',
            'soil_type', 'soil_texture', 'soil_ph',
            'organic_carbon', 'recommended_crops', 'created_at'
        ]
        read_only_fields = ['uuid', 'created_at']
