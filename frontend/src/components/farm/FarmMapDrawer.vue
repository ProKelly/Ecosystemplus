<script setup lang="ts">
import { ref, onMounted, defineProps, defineEmits, defineExpose } from 'vue'
import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'

const props = defineProps({
  initialGeojson: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['complete', 'cancel'])

const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let drawnItems: L.FeatureGroup = new L.FeatureGroup()
let drawControl: L.Control.Draw | null = null

onMounted(() => {
  if (!mapContainer.value) return

  // Initialize map
  map = L.map(mapContainer.value).setView([-1.286389, 36.817223], 13) // Default to Nairobi center
  
  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map)

  // Initialize the feature group to store drawn items
  drawnItems = new L.FeatureGroup()
  map.addLayer(drawnItems)

  // Add draw control
  drawControl = new L.Control.Draw({
    position: 'topright',
    draw: {
      polygon: {
        allowIntersection: false,
        showArea: false, // PATCH: avoid leaflet-draw type error
        metric: true,
        shapeOptions: {
          color: '#10B981' // emerald-600
        }
      },
      rectangle: true,
      circle: false,
      marker: false,
      circlemarker: false,
      polyline: false
    },
    edit: {
      featureGroup: drawnItems
    }
  })
  map.addControl(drawControl)

  // Load initial geometry if provided
  if (props.initialGeojson) {
    const layer = L.geoJSON(props.initialGeojson, {
      style: {
        color: '#10B981',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.3
      }
    })
    drawnItems.addLayer(layer)
    map.fitBounds(layer.getBounds())
  }

  // Event listeners
  map.on(L.Draw.Event.CREATED, (e: any) => {
    const type = e.layerType
    const layer = e.layer
    
    // Clear any existing layers
    drawnItems.clearLayers()
    
    // Add new layer
    drawnItems.addLayer(layer)
  })

  map.on(L.Draw.Event.EDITED, (e: any) => {
    const layers = e.layers
    layers.eachLayer((layer: any) => {
      drawnItems.addLayer(layer)
    })
  })
})

const saveDrawing = () => {
  if (drawnItems.getLayers().length === 0) {
    emit('complete', null)
    return
  }
  
  const layer = drawnItems.getLayers()[0]
  const geojson = layer.toGeoJSON()
  emit('complete', geojson)
}

defineExpose({ saveDrawing })
</script>

<template>
  <div ref="mapContainer" class="w-full h-full"></div>
</template>

<style>
.leaflet-container {
  background-color: #f8fafc !important; /* gray-50 */
}

.leaflet-draw-toolbar a {
  background-image: none !important;
}

.leaflet-draw-toolbar .leaflet-draw-draw-polygon {
  background-color: #10B981; /* emerald-600 */
  color: white;
}

.leaflet-draw-toolbar .leaflet-draw-draw-rectangle {
  background-color: #10B981; /* emerald-600 */
  color: white;
}
</style>