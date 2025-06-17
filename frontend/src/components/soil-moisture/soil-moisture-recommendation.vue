<template>
  <div class="bg-white p-6 shadow-md mt-6">
    <!-- Tab Navigation -->
    <div class="flex space-x-4 mb-6">
      <button
        @click="activeTab = 'today'"
        :class="[
          'px-2 py-1 rounded font-medium',
          activeTab === 'today'
            ? 'bg-green-600 text-white'
            : 'bg-green-100 text-green-700 hover:bg-green-200',
        ]"
      >
        Today's Status
      </button>
      <button
        @click="activeTab = 'forecast'"
        :class="[
          'px-2 py-1 mr-2 rounded font-medium',
          activeTab === 'forecast'
            ? 'bg-green-600 text-white'
            : 'bg-green-100 text-green-700 hover:bg-green-200',
        ]"
      >
        Forecast
      </button>
    </div>

    <!-- Date Selector for Forecast -->
    <div v-if="activeTab === 'forecast'" class="mb-6">
      <label class="block text-green-700 mb-2">Select Date:</label>
      <input
        type="date"
        v-model="selectedDate"
        class="border-2 border-green-200 rounded-lg p-2 w-full focus:border-green-500 focus:outline-none"
        @change="handleDateSelection"
      />
    </div>

    <h2 class="text-xl font-bold mb-4 text-green-700">
      {{ activeTab === 'today' ? "Today's" : 'Forecast' }} Irrigation Recommendation
    </h2>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 rounded-md mb-6">
      <p class="text-red-700">{{ error }}</p>
      <button
        @click="retryFetch"
        class="mt-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
      >
        Retry Loading
      </button>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="text-gray-500">Loading soil moisture data...</div>

    <!-- Content -->
    <div v-else>
      <div class="text-center">
        <div class="text-5xl font-bold text-green-700">
          {{ averageMoisture.toFixed(2) }}
          <span
            :class="{
              'text-green-500': status === 'green',
              'text-yellow-400': status === 'yellow',
              'text-red-500': status === 'red',
            }"
            >⬤</span
          >
        </div>
        <p class="text-sm mt-1 text-green-600">Status: {{ statusText }}</p>
      </div>

      <div class="mt-6 bg-green-50 border-l-4 border-green-400 p-4 rounded-md">
        <p class="font-semibold text-green-700">Recommendation:</p>
        <p class="text-green-800">{{ recommendation }}</p>
        <p class="mt-2 italic text-sm text-green-600">Method: {{ method }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'

// Constants
const latitude = 5.0
const longitude = 10.0

// State Management
interface TabData {
  moisture: number
  status: 'green' | 'yellow' | 'red'
  recommendation: string
  method: string
  statusText: string
}

interface MoistureCache {
  date: string
  data: TabData
}

const averageMoisture = ref(0)
const loading = ref(true)
const error = ref('')
const status = ref<'green' | 'yellow' | 'red'>('green')
const recommendation = ref('')
const method = ref('')
const statusText = ref('')
const activeTab = ref('today')
const selectedDate = ref('')

// Cache Management
const moistureCache = ref<MoistureCache[]>([])
const todaysData = ref<TabData | null>(null)
const lastForecastData = ref<{ date: string; data: TabData } | null>(null)

// Update UI with cached data
const updateUI = (data: TabData) => {
  averageMoisture.value = data.moisture
  status.value = data.status
  recommendation.value = data.recommendation
  method.value = data.method
  statusText.value = data.statusText
}

// Generate recommendations based on moisture level
const generateRecommendations = (moisture: number): TabData => {
  const data: TabData = {
    moisture,
    status: 'green',
    recommendation: '',
    method: '',
    statusText: '',
  }

  if (moisture < 0.175) {
    data.status = 'red'
    data.recommendation = 'High irrigation needed (6–10 mm/day).'
    data.method = 'Use drip irrigation or traditional furrow method with 2 sessions daily.'
    data.statusText = 'Very Low'
  } else if (moisture < 0.3) {
    data.status = 'yellow'
    data.recommendation = 'Moderate irrigation needed (3–5 mm/day).'
    data.method = 'Use watering cans or low-flow hose method.'
    data.statusText = 'Low'
  } else {
    data.status = 'green'
    data.recommendation = 'No irrigation needed. Soil moisture is adequate.'
    data.method = 'Monitor soil every 2–3 days.'
    data.statusText = 'Adequate'
  }

  return data
}

// Fetch data from API
const fetchData = async (targetDate: Date) => {
  const dateStr = formatDate(targetDate)

  // Check cache first
  const cachedData = moistureCache.value.find((item) => item.date === dateStr)
  if (cachedData) {
    updateUI(cachedData.data)
    return
  }

  loading.value = true
  error.value = ''

  try {
    const url = `https://climate-api.open-meteo.com/v1/climate?latitude=${latitude}&longitude=${longitude}&start_date=${dateStr}&end_date=${dateStr}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`

    const response = await fetch(url)
    if (!response.ok) throw new Error('Failed to fetch data from server')

    const data = await response.json()
    const moistureValue = data.daily.soil_moisture_0_to_10cm_mean[0]
    const recommendations = generateRecommendations(moistureValue)

    // Cache the data
    moistureCache.value.push({
      date: dateStr,
      data: recommendations,
    })

    // Store specific cache based on tab
    if (dateStr === formatDate(new Date())) {
      todaysData.value = recommendations
    } else {
      lastForecastData.value = { date: dateStr, data: recommendations }
    }

    updateUI(recommendations)
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to load soil moisture data. Please try again.'
  } finally {
    loading.value = false
  }
}

// Handle date selection
const handleDateSelection = async () => {
  if (!selectedDate.value) return
  await fetchData(new Date(selectedDate.value))
}

// Retry fetch on error
const retryFetch = async () => {
  if (activeTab.value === 'today') {
    await fetchData(new Date())
  } else if (selectedDate.value) {
    await fetchData(new Date(selectedDate.value))
  }
}

// Format date helper
const formatDate = (d: Date) => d.toISOString().split('T')[0]

// Watch for tab changes
watch(activeTab, (newTab) => {
  error.value = '' // Clear any existing errors

  if (newTab === 'today' && todaysData.value) {
    updateUI(todaysData.value)
  } else if (newTab === 'forecast' && lastForecastData.value) {
    selectedDate.value = lastForecastData.value.date
    updateUI(lastForecastData.value.data)
  } else if (newTab === 'today') {
    fetchData(new Date())
  }
})

// Initialize component
onMounted(async () => {
  await fetchData(new Date())
})
</script>

<style scoped></style>
