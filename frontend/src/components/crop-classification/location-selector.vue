<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'
import 'leaflet-geometryutil'
import type { LatLng, Map, FeatureGroup, Control, TileLayer } from 'leaflet'

// Leaflet marker icon fix
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
})

// Data & refs
const showMap = ref(false)
const farmName = ref('')
const polygonCoordinates = ref<LatLng[]>([])
const manualCoordinates = ref<{ lat: number; lng: number }[]>([])
const selectedFarm = ref('')
const manualMode = ref(false)
const farms = ref<Record<string, any>>({})
const mapContainer = ref<HTMLElement | null>(null)
const map = ref<Map | null>(null)
const isFullScreen = ref(false)
const showRegistrationMethods = ref(false)

// Computed available farms
const farmList = computed(() => Object.values(farms.value))
const selectedFarmData = computed(() => {
  if (farmList.value.length === 0) return null
  if (farmList.value.length === 1) return farmList.value[0]
  return farms.value[selectedFarm.value] || null
})

function computeArea(coords: L.LatLng[]): number {
  const latlngs = coords.map((p) => [p.lat, p.lng]) as [number, number][]
  return L.GeometryUtil.geodesicArea(latlngs)
}

function computeBounds(coords: L.LatLng[]) {
  const lats = coords.map((p) => p.lat)
  const lngs = coords.map((p) => p.lng)
  const latMin = Math.min(...lats),
    latMax = Math.max(...lats)
  const lngMin = Math.min(...lngs),
    lngMax = Math.max(...lngs)
  const latDist = mapDistance(latMin, lngMin, latMax, lngMin)
  const lngDist = mapDistance(latMin, lngMin, latMin, lngMax)
  return {
    length: Math.max(latDist, lngDist).toFixed(2) + ' m',
    width: Math.min(latDist, lngDist).toFixed(2) + ' m',
  }
}

function mapDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
  return L.latLng(lat1, lng1).distanceTo(L.latLng(lat2, lng2))
}

function registerFromMap() {
  if (!farmName.value || polygonCoordinates.value.length < 3) {
    alert('Please draw an area and enter a farm name.')
    return
  }
  const area = computeArea(polygonCoordinates.value)
  const bounds = computeBounds(polygonCoordinates.value)
  farms.value[farmName.value] = {
    name: farmName.value,
    coordinates: polygonCoordinates.value.map((p) => ({ lat: p.lat, lng: p.lng })),
    surfaceArea: `${(area / 10000).toFixed(2)} ha`,
    ...bounds,
    timestamp: new Date().toISOString(),
  }
  selectedFarm.value = farmName.value
  farmName.value = ''
  polygonCoordinates.value = []
}

function registerManually() {
  if (!farmName.value || manualCoordinates.value.length < 4) {
    alert('Please add at least 4 points and a farm name.')
    return
  }
  farms.value[farmName.value] = {
    name: farmName.value,
    coordinates: [...manualCoordinates.value],
    surfaceArea: 'Unknown',
    length: 'Unknown',
    width: 'Unknown',
    timestamp: new Date().toISOString(),
  }
  selectedFarm.value = farmName.value
  farmName.value = ''
  manualCoordinates.value = []
}

function markManualPoint() {
  const randomLat = 7 + Math.random() * 0.5
  const randomLng = 13 + Math.random() * 0.5
  manualCoordinates.value.push({ lat: randomLat, lng: randomLng })
}

function toggleFullScreen() {
  isFullScreen.value = !isFullScreen.value
  if (map.value) map.value.invalidateSize()
}

function initializeMap() {
  if (!mapContainer.value || map.value) return
  const leafletMap = L.map(mapContainer.value).setView([7.5, 13.5], 6)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(leafletMap)
  const drawnItems = new L.FeatureGroup()
  leafletMap.addLayer(drawnItems)

  const drawControl = new L.Control.Draw({
    draw: {
      polygon: {
        allowIntersection: false,
        drawError: { color: '#e1e4e8', message: 'Invalid shape!' },
        shapeOptions: { color: '#22c55e' },
      },
      polyline: false,
      rectangle: false,
      circle: false,
      marker: false,
      circlemarker: false,
    },
    edit: { featureGroup: drawnItems },
  })
  leafletMap.addControl(drawControl)

  leafletMap.on(L.Draw.Event.CREATED, (event: any) => {
    drawnItems.clearLayers()
    const layer = event.layer
    drawnItems.addLayer(layer)
    if (layer instanceof L.Polygon) {
      polygonCoordinates.value = layer.getLatLngs()[0]
    }
  })

  map.value = leafletMap
}

watch([() => mapContainer.value, showMap], ([container, visible]) => {
  if (container && visible) setTimeout(() => initializeMap(), 100)
})

onUnmounted(() => {
  if (map.value) map.value.remove()
})

function activateMapMethod() {
  showRegistrationMethods.value = false
  manualMode.value = false
  showMap.value = true
}

function activateManualMethod() {
  showRegistrationMethods.value = false
  manualMode.value = true
  showMap.value = false
}

function cancelRegistration() {
  showMap.value = false
  manualMode.value = false
  showRegistrationMethods.value = false
  farmName.value = ''
  polygonCoordinates.value = []
  manualCoordinates.value = []
}

function deleteFarm(farmName: string) {
  if (confirm(`Are you sure you want to delete "${farmName}"?`)) {
    delete farms.value[farmName]
    selectedFarm.value = ''
  }
}

// making variable easily accessible in order components
// import { provide } from 'vue'

// provide('selectedFarmData', selectedFarmData)
</script>

<template>
  <div class="bg-white shadow-sm rounded-lg p-6">
    <!-- Farm Selection Section -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-green-700 mb-4">Select Farm</h2>

      <transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 transform -translate-y-4"
        enter-to-class="opacity-100 transform translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 transform translate-y-0"
        leave-to-class="opacity-0 transform -translate-y-4"
      >
        <div v-if="farmList.length === 0" class="text-center py-6 bg-gray-50 rounded-md">
          <div class="text-gray-600 space-y-2 mb-6">
            <p class="text-lg">No farms registered yet!</p>
            <p class="text-sm">
              Start by registering your first farm to begin crop classification.
            </p>
          </div>
          <button
            @click="showRegistrationMethods = true"
            class="register-btn bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-sm text-sm transition-colors shadow-sm mx-2"
          >
            Register New Farm
          </button>
        </div>

        <div v-else-if="!showRegistrationMethods" class="space-y-4">
          <div class="flex gap-2 items-center">
            <select
              v-model="selectedFarm"
              class="flex-1 p-2 border rounded-sm focus:ring-green-500 focus:border-green-500"
            >
              <option value="" disabled>Select a farm</option>
              <option v-for="farm in farmList" :key="farm.name" :value="farm.name">
                {{ farm.name }}
              </option>
            </select>
            <button
              v-if="selectedFarm"
              @click="deleteFarm(selectedFarm)"
              class="bg-red-500 text-white hover:bg-red-100 hover:text-red-500 px-2 rounded-sm transition-colors"
              title="Delete farm"
              style="margin-bottom: 5px"
            >
              <!-- <span style="" class="text-lg">×</span> -->
              <font-awesome-icon icon="trash-alt" />
            </button>
          </div>

          <div class="flex justify-center mt-4">
            <button
              @click="showRegistrationMethods = true"
              class="add-farm-btn bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-sm text-sm transition-colors shadow-sm mx-2"
              style="margin-top: 3px"
            >
              Add Another Farm
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Registration Methods Section -->
    <transition
      enter-active-class="transition-all duration-500 ease-out"
      enter-from-class="opacity-0 transform scale-95"
      enter-to-class="opacity-100 transform scale-100"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="opacity-100 transform scale-100"
      leave-to-class="opacity-0 transform scale-95"
    >
      <div v-if="showRegistrationMethods" class="w-full border-t pt-6 relative">
        <button
          @click="showRegistrationMethods = false"
          class="absolute top-5 left-24/25 text-gray-400 bg-red-500 text-white rounded px-2 shadow-md hover:text-red-600 hover:bg-red-200 transition-colors"
        >
          <!-- <font-awesome-icon class="text-lg" icon="xmark" /> -->
          <span>×</span>
        </button>
        <h3 class="text-lg font-medium text-green-700 mb-6">Choose Registration Method</h3>

        <div class="space-y-6">
          <!-- Map Method -->
          <div
            class="bg-gray-50 rounded-sm p-5 transition-transform hover:scale-[1.01] duration-300"
          >
            <h4 class="font-medium text-gray-800 mb-2">Map Drawing Method</h4>
            <p class="text-gray-600 text-sm mb-4">
              Draw your farm boundaries directly on the map. This method provides accurate
              measurements and is recommended for precise field mapping.
            </p>
            <button
              @click="activateMapMethod"
              class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-sm text-sm transition-colors shadow-sm"
            >
              Use Map Method
            </button>
          </div>

          <!-- Manual Method -->
          <div
            class="bg-gray-50 rounded-sm p-5 transition-transform hover:scale-[1.01] duration-300"
          >
            <h4 class="font-medium text-gray-800 mb-2">Manual Coordinate Method</h4>
            <p class="text-gray-600 text-sm mb-4">
              Manually mark field corners. Use this method if you already know your field
              coordinates or prefer point-by-point marking.
            </p>
            <button
              @click="activateManualMethod"
              class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-sm text-sm transition-colors shadow-sm"
            >
              Use Manual Method
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Map Section -->
    <div
      v-if="showMap || manualMode"
      style="margin-top: 10px"
      class="flex justify-between items-center mb-4"
    >
      <h3 class="text-lg font-medium text-green-700" style="margin-bottom: 3px">
        Farm Registration
      </h3>
      <button
        @click="cancelRegistration"
        style="margin-bottom: 3px; margin-right: 3px"
        class="bg-red-500 text-white hover:bg-red-200 hover:bg-red-200 px-2 rounded-sm text-lg transition-colors"
      >
        <span style="" class="">×</span>
      </button>
    </div>

    <div v-if="showMap" class="mt-6">
      <div class="mb-4">
        <input
          v-model="farmName"
          type="text"
          placeholder="Enter farm name"
          class="w-full p-2 border rounded-lg focus:ring-green-500 focus:border-green-500"
        />
      </div>

      <div :class="[isFullScreen ? 'fixed inset-0 z-50 bg-white' : 'relative h-[400px]']">
        <div ref="mapContainer" class="z-9 w-full h-full rounded-lg border border-gray-200" />
        <div class="absolute top-3 right-3 flex gap-2 z-10">
          <button
            @click="registerFromMap"
            class="absolute bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded-sm text-sm z-10 transition-colors shadow-sm"
          >
            <!-- Save Farm -->
            <font-awesome-icon icon="save" />
          </button>
          <button
            @click="toggleFullScreen"
            class="bg-green-600 hover:bg-green-700 text-white px-2 py-2 rounded-sm text-sm transition-colors shadow-sm flex items-center gap-2"
          >
            <font-awesome-icon :icon="isFullScreen ? 'compress' : 'expand'" />
            <!-- <span>{{ isFullScreen ? 'Exit Fullscreen' : 'Fullscreen' }}</span> -->
          </button>
        </div>
      </div>
    </div>

    <!-- Manual Registration Section -->
    <div v-if="manualMode" class="mt-6">
      <div class="mb-4">
        <input
          v-model="farmName"
          type="text"
          placeholder="Enter farm name"
          class="w-full p-2 border rounded-lg focus:ring-green-500 focus:border-green-500"
        />
      </div>

      <div class="flex items-center gap-10">
        <button
          @click="markManualPoint"
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-sm text-sm transition-colors shadow-sm"
          style="margin: 2px 0"
        >
          Mark Point
        </button>
        <span class="text-sm text-gray-600">Points marked: {{ manualCoordinates.length }}</span>
      </div>

      <button
        v-if="manualCoordinates.length >= 3"
        @click="registerManually"
        class="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-sm text-sm transition-colors shadow-sm"
      >
        Save Farm
      </button>
    </div>
  </div>
</template>

<style scoped>
.register-btn,
.add-farm-btn {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(22, 163, 74, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(22, 163, 74, 0);
  }
}

/* Smoother transitions */
.transition-all {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Button hover effect */
button {
  position: relative;
  overflow: hidden;
}

button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120%;
  height: 120%;
  background: rgba(255, 255, 255, 0.1);
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.5s;
  border-radius: 50%;
}

button:hover::after {
  transform: translate(-50%, -50%) scale(1);
}

/* Add to your existing styles */
.bg-red-100 {
  transition: all 0.2s ease-in-out;
}

.bg-red-100:hover {
  transform: scale(1.02);
}

/* Other existing styles... */
</style>
