import ee
import requests
from django.conf import settings

# Initialize once
ee.Initialize(project='ecosystemplus')

def analyze_soil(polygon_geojson):
    """
    Clip FAO SoilGrids and Earth Engine datasets to the polygon,
    return summarized soil attributes and crop recommendations.
    """

    # 1. Parse boundary
    geom = ee.Geometry.Polygon(polygon_geojson['coordinates'])

    # 2. SoilGrids layers via Earth Engine
    layers = {
        'sand': 'projects/soilgrids-isric/sand_mean',
        'silt': 'projects/soilgrids-isric/silt_mean',
        'clay': 'projects/soilgrids-isric/clay_mean',
        'ph': 'projects/soilgrids-isric/phh2o_mean',
        'organic_carbon': 'projects/soilgrids-isric/orc_mean'
    }

    stats = {}
    for key, asset in layers.items():
        img = ee.ImageCollection(asset).first()
        mean = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geom,
            scale=250
        ).get(info=key)
        stats[key] = mean.getInfo()

    # 3. Derive texture
    sand, silt, clay = stats['sand'], stats['silt'], stats['clay']
    soil_texture = f"{round(sand)}% sand, {round(silt)}% silt, {round(clay)}% clay"

    # 4. Get moisture via FAO API (example endpoint)
    resp = requests.get(
        settings.SOI_MOISTURE_API_URL,
        params={'geojson': polygon_geojson}
    )
    moisture = resp.json().get('moisture') if resp.status_code == 200 else None

    # 5. Recommend crops (example rules)
    recs = []
    ph = stats['ph']
    oc = stats['organic_carbon']
    if ph and 5.5 <= ph <= 7.0:
        recs += ['Maize', 'Groundnut']
    if oc and oc > 5:
        recs += ['Vegetables']
    soil_type = 'Loam'  # Simplified example
    
    return {
        "soil_type": soil_type,
        "soil_texture": soil_texture,
        "soil_ph": round(ph, 2) if ph else None,
        "organic_carbon": round(oc, 2) if oc else None,
        "moisture": moisture,
        "recommended_crops": ", ".join(recs)
    }
