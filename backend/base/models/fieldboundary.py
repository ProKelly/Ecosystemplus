from django.db import models
from django.contrib.gis.db import models as gis_models
import uuid

class FieldBoundary(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='field_boundaries')

    # Geometry of the field boundary (usually a polygon within the farm)
    boundary = gis_models.PolygonField(srid=4326)

    # Metadata extracted via model/analysis
    area_hectares = models.FloatField(help_text="Size of the field in hectares", null=True, blank=True)

    soil_type = models.CharField(max_length=100, null=True, blank=True)
    soil_texture = models.CharField(max_length=100, null=True, blank=True)
    soil_ph = models.FloatField(null=True, blank=True)
    organic_carbon = models.CharField(max_length=100, null=True, blank=True)

    recommended_crops = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Field Boundary'
        verbose_name_plural = 'Field Boundaries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Field in {self.farm.name} - {round(self.area_hectares, 2)} ha"
    
    def save(self, *args, **kwargs):
        if self.boundary:
            # Transform to SRID 3857 for accurate area calculation in meters²
            projected = self.boundary.transform(3857, clone=True)
            self.area_hectares = projected.area / 10000  # convert m² to hectares
        super().save(*args, **kwargs)
