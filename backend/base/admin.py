from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from .models import User, Community, AdminAccessRequest
from .models import Farm, FieldBoundary

admin.site.register([User, Community, AdminAccessRequest])

@admin.register(Farm)
class FarmAdmin(gis_admin.GISModelAdmin):
    list_display = ('name', 'owner', 'community', 'created_at')
    search_fields = ('name', 'owner__first_name', 'community__name')
    list_filter = ('community', 'created_at')
    default_lon = 0
    default_lat = 0
    default_zoom = 10
    openlayers_url = 'https://openlayers.org/en/v4.6.5/build/ol.js'
    attribute_prefix = 'Ecosystem+'

@admin.register(FieldBoundary)
class FieldBoundaryAdmin(gis_admin.GISModelAdmin):
    list_display = ('farm', 'area_hectares', 'soil_type', 'created_at')
    search_fields = ('farm__name', 'soil_type')
    list_filter = ('farm__community', 'created_at')
    default_lon = 0
    default_lat = 0
    default_zoom = 10
    openlayers_url = 'https://openlayers.org/en/v4.6.5/build/ol.js'
    attribute_prefix = 'Ecosystem+'

