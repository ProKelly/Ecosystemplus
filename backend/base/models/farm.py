from django.db import models
from django.contrib.gis.db import models as gis_models
from .user import User
import uuid

class Farm(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    
    # By default, it uses SRID 4326 (WGS84 - lat/long), which is standard for OpenStreetMap data.
    coordinates = gis_models.PolygonField(srid=4326)

    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='farms', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Farm'
        verbose_name_plural = 'Farms'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name