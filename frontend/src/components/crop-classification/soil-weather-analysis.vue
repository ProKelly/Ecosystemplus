<script setup lang="ts">
// Import necessary dependencies and components
import { ref, onMounted, watch, computed, inject } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'
import ClimateChart from '../charts/ClimateChart.vue'
import axios from 'axios'

// const injectedSelectedFarmData = inject('selectedFarmData')

// const selectedFarmData = computed(() => injectedSelectedFarmData?.value ?? null)

// Initialize farm data with demo values
const registeredField = ref({
  name: 'Demo Farm',
  coordinates: [
    [2.5, 7.6],
    [2.6, 7.8],
    [2.5, 7.7],
    [2.4, 7.9],
  ],
  surfaceArea: '5.2 ha',
  timestamp: '2025-06-16T10:00:00Z',
})

// Refs for map and data management
const staticMapContainer = ref<HTMLElement | null>(null)
const coordinateMidpoint = ref<{ lat: number; lng: number } | null>(null)

// Soil analysis data structure
const soilAnalysis = ref({
  type: 'Loamy',
  ndmi: 0.56, // Normalized Difference Moisture Index
  spi: -0.2, // Standardized Precipitation Index
  ndwi: 0.34, // Normalized Difference Water Index
  ndvi: 0.67, // Normalized Difference Vegetation Index
})

// Weather data management
const weatherTab = ref<'temperature' | 'humidity' | 'rainfall' | 'evapotranspiration'>(
  'temperature',
)

// Initialize weather data structure with empty arrays
const weatherData = ref({
  temperature: Array(12).fill(0),
  humidity: Array(12).fill(0),
  rainfall: Array(12).fill(0),
  evapotranspiration: Array(12).fill(0),
})

// Static recommendations for different weather conditions
// const recommendations = {
//   temperature: 'Ensure optimal irrigation in hotter months (March-May).',
//   humidity: 'Monitor fungal risk in high humidity (July-August).',
//   rainfall: 'Plant water-loving crops during high rainfall (August).',
//   evapotranspiration: 'Minimize water loss through mulching during dry periods.',
// }

// Initialize map and draw field shape
onMounted(() => {
  const coords = registeredField.value.coordinates
  calculateMidpoint(coords)

  if (!staticMapContainer.value) return

  // Configure map with disabled interactions for static display
  const map = L.map(staticMapContainer.value, {
    zoomControl: false,
    attributionControl: false,
    dragging: false,
    scrollWheelZoom: false,
    touchZoom: false,
    doubleClickZoom: false,
    keyboard: false,
  })

  // Add dark themed map tiles
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '',
  }).addTo(map)

  // Draw field polygon with styling
  const polygon = L.polygon(coords, {
    color: '#22c55e',
    fillColor: '#22c55e',
    fillOpacity: 0.5,
    weight: 2,
    dashArray: '',
  }).addTo(map)

  // Add markers at polygon vertices
  coords.forEach((coord) => {
    L.circleMarker(coord, {
      radius: 4,
      fillColor: '#fff',
      color: '#22c55e',
      weight: 2,
      opacity: 1,
      fillOpacity: 1,
    }).addTo(map)
  })

  // Fit map view to polygon bounds
  map.fitBounds(polygon.getBounds(), {
    padding: [20, 20],
    maxZoom: 16,
  })
})

/**
 * Fetches climate data from OpenMeteo API
 * @param midpoint Geographic coordinates of field center
 */
async function fetchClimateDataFromOpenMeteo(midpoint: { lat: number; lng: number }) {
  const year = new Date().getFullYear()
  const start_date = `${year}-01-01`
  const end_date = `${year}-12-31`

  // Construct API URL with parameters
  const url = `https://climate-api.open-meteo.com/v1/climate?latitude=${midpoint.lat}&longitude=${midpoint.lng}&start_date=${start_date}&end_date=${end_date}&models=MRI_AGCM3_2_S&daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,et0_fao_evapotranspiration_sum&timezone=auto`

  try {
    const res = await axios.get(url)
    const daily = res.data?.daily

    if (daily) {
      // Initialize arrays for monthly data aggregation
      const monthlyData = {
        temperature: Array(12)
          .fill(0)
          .map(() => []),
        humidity: Array(12)
          .fill(0)
          .map(() => []),
        rainfall: Array(12)
          .fill(0)
          .map(() => []),
        evapotranspiration: Array(12)
          .fill(0)
          .map(() => []),
      }

      // Group daily data by months
      daily.time.forEach((dateStr: string, i: number) => {
        const month = new Date(dateStr).getMonth()
        monthlyData.temperature[month].push(daily.temperature_2m_mean[i])
        monthlyData.humidity[month].push(daily.relative_humidity_2m_mean[i])
        monthlyData.rainfall[month].push(daily.precipitation_sum[i])
        monthlyData.evapotranspiration[month].push(daily.et0_fao_evapotranspiration_sum[i])
      })

      // Calculate monthly averages
      const averaged = (data: number[][]) =>
        data.map((arr) => (arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0))

      // Update weather data with calculated averages
      weatherData.value.temperature = averaged(monthlyData.temperature)
      weatherData.value.humidity = averaged(monthlyData.humidity)
      weatherData.value.rainfall = averaged(monthlyData.rainfall)
      weatherData.value.evapotranspiration = averaged(monthlyData.evapotranspiration)
    }
  } catch (err) {
    console.error('Failed to fetch climate data:', err)
  }
}

/**
 * Calculates the center point of the field
 * @param coords Array of coordinate pairs defining the field boundary
 */
function calculateMidpoint(coords: [number, number][]) {
  const lat = coords.reduce((acc, val) => acc + val[0], 0) / coords.length
  const lng = coords.reduce((acc, val) => acc + val[1], 0) / coords.length
  coordinateMidpoint.value = { lat, lng }

  fetchClimateDataFromOpenMeteo({ lat, lng })
}

// Compute dynamic recommendations based on weather data
const dynamicRecommendation = computed(() => {
  const data = weatherData.value[weatherTab.value]

  if (!data.length) return 'No data available.'

  const avg = data.reduce((a, b) => a + b, 0) / data.length
  const max = Math.max(...data)
  const min = Math.min(...data)

  // Return specific recommendations based on weather conditions
  switch (weatherTab.value) {
    case 'temperature':
      if (avg > 30) return 'High temperatures detected — schedule irrigation frequently.'
      if (avg < 18) return 'Temperature is low — consider frost-protecting crops.'
      return 'Temperature is optimal for most crops.'
    case 'humidity':
      if (avg > 80) return 'High humidity — monitor for fungal diseases.'
      if (avg < 40) return 'Low humidity — risk of dehydration, consider mist irrigation.'
      return 'Humidity levels are moderate.'
    case 'rainfall':
      if (max > 100) return 'Heavy rainfall expected — implement drainage strategies.'
      if (avg < 30) return 'Low rainfall — water-loving crops may be at risk.'
      return 'Rainfall is within normal range.'
    case 'evapotranspiration':
      if (avg > 5) return 'High evapotranspiration — increase mulching to retain soil moisture.'
      return 'Evapotranspiration is manageable.'
    default:
      return 'No specific recommendation available.'
  }
})
</script>

<template>
  <div class="p-6 sm:p-8 space-y-8 shadow-md bg-white">
    <!-- Header section -->
    <div class="rounded-lg p-4 sm:p-6">
      <h2 class="text-xl font-semibold text-green-700">Registered Farm View</h2>
    </div>

    <!-- Flex container for map and soil analysis -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Map section -->
      <div class="shadow-md rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold mb-4 text-green-700">Field Shape</h3>
        <div
          ref="staticMapContainer"
          class="aspect-square w-full rounded-lg border-2 bg-black z-2 border-green-400 shadow-sm"
          style="max-width: 300px; margin: 0 auto"
        ></div>
        <div class="mt-3 text-sm text-gray-500 text-center">Field Shape Preview</div>
      </div>

      <!-- Soil analysis section -->
      <div class="rounded-lg p-4 sm:p-6">
        <h3 class="text-lg font-semibold mb-4 text-green-700">Analysis of the Soil</h3>
        <div class="grid grid-cols-2 gap-6 bg-gray-50 p-6 rounded-lg">
          <div class="flex flex-col">
            <span class="font-medium text-gray-700">Soil Type:</span>
            <span class="mt-1">{{ soilAnalysis.type }}</span>
          </div>
          <div class="flex flex-col">
            <span class="font-medium text-gray-700">NDMI:</span>
            <span class="mt-1">{{ soilAnalysis.ndmi }}</span>
          </div>
          <div class="flex flex-col">
            <span class="font-medium text-gray-700">SPI:</span>
            <span class="mt-1">{{ soilAnalysis.spi }}</span>
          </div>
          <div class="flex flex-col">
            <span class="font-medium text-gray-700">NDWI:</span>
            <span class="mt-1">{{ soilAnalysis.ndwi }}</span>
          </div>
          <div class="flex flex-col">
            <span class="font-medium text-gray-700">NDVI:</span>
            <span class="mt-1">{{ soilAnalysis.ndvi }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Weather section -->
    <div class="rounded-lg p-4 sm:p-6">
      <h3 class="text-lg font-semibold mb-4 text-green-700">
        Weather Conditions and Recommendations
      </h3>

      <div class="flex flex-wrap gap-3 mb-6">
        <button
          v-for="key in ['temperature', 'humidity', 'rainfall', 'evapotranspiration']"
          :key="key"
          @click="weatherTab = key"
          :class="{
            'bg-green-600 text-white': weatherTab === key,
            'bg-gray-100 text-gray-700 hover:bg-gray-200': weatherTab !== key,
          }"
          class="px-4 py-2 rounded transition-colors duration-200 text-sm my-4"
        >
          {{ key.charAt(0).toUpperCase() + key.slice(1) }}
        </button>
      </div>

      <!-- Weather chart section -->
      <div class="bg-gray-50 rounded-lg border border-gray-200 p-6 mb-4">
        <div class="h-64 w-full">
          <ClimateChart
            :label="weatherTab.charAt(0).toUpperCase() + weatherTab.slice(1)"
            :data="weatherData[weatherTab]"
            :type="weatherTab"
          />
        </div>
      </div>

      <p class="text-sm text-gray-700 italic bg-green-100 p-4 rounded-lg">
        Recommendation: {{ dynamicRecommendation }}
      </p>
    </div>
  </div>
</template>
