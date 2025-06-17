<template>
  <section class="bg-white py-10 px-6 md:px-16 lg:px-24 text-gray-800">
    <h2 class="text-2xl md:text-3xl font-bold text-green-700 mb-6">Soil Moisture Monitoring</h2>

    <!-- User Selection -->
    <div class="mb-6 space-y-4" style="margin-bottom: 5px">
      <div class="flex gap-4">
        <label class="block font-semibold">View Soil Moisture for:</label>
        <select v-model="viewType" class="p-2 rounded border">
          <option disabled value="">Select Period</option>
          <option value="specific">A Specific Month</option>
          <option value="forecast">Next 7 Days</option>
        </select>
      </div>

      <!-- Specific Month/Year Selector -->
      <div v-if="viewType === 'specific'" class="flex gap-4" style="margin-bottom: 10px">
        <div>
          <label class="block mb-2">Month:</label>
          <select v-model="selectedMonth" class="p-2 rounded border">
            <option v-for="(month, index) in months" :key="index" :value="index + 1">
              {{ month }}
            </option>
          </select>
        </div>
        <div>
          <label class="block mb-2">Year:</label>
          <select v-model="selectedYear" class="p-2 rounded border">
            <option v-for="year in years" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        <div style="display: flex; align-items: flex-end; justify-content: center">
          <button
            @click="fetchData"
            class="bg-green-600 text-white px-2 py-2 rounded hover:bg-green-700"
          >
            Load Data
          </button>
        </div>
      </div>
    </div>

    <!-- Loading Bar -->
    <div v-if="isLoading" class="mb-6">
      <div class="w-full h-2 bg-gray-200 rounded">
        <div
          class="h-full bg-green-600 rounded transition-all duration-500"
          :style="{ width: `${loadingProgress}%` }"
        ></div>
      </div>
    </div>

    <!-- Chart Section -->
    <div
      v-if="chartData.length"
      class="bg-green-50 rounded-lg shadow p-4 mb-8 border border-green-500"
    >
      <h3 class="text-lg font-semibold text-green-700 mb-4 text-center">
        {{ chartTitle }}
      </h3>
      <LineChart
        :chart-data="{
          labels: labels,
          datasets: [
            {
              label: 'Soil Moisture',
              data: chartData,
              fill: false,
              borderColor: '#16a34a',
              tension: 0.1,
            },
          ],
        }"
      />
    </div>

    <!-- Dry Periods Section -->
    <div class="space-y-4">
      <div class="flex justify-between items-center" style="margin-top: 10px; margin-bottom: 10px">
        <h3 class="text-xl font-semibold text-green-700">Dry Periods Analysis</h3>
        <div class="space-x-2">
          <button
            @click="
              () => {
                showDefaultTable = true
                showComparison = false
              }
            "
            class="text-sm px-3 py-1 rounded"
            :class="showDefaultTable ? 'bg-green-600 text-white' : 'bg-gray-200'"
            style="margin-right: 3px"
          >
            Show Current Year
          </button>
          <button
            @click="() => (showComparison = true)"
            class="text-sm px-3 py-1 rounded"
            :class="showComparison ? 'bg-green-600 text-white' : 'bg-gray-200'"
          >
            Compare Results
          </button>
        </div>
      </div>

      <!-- Current Period Table -->
      <div
        v-if="!showDefaultTable || showComparison"
        class="bg-red-50 border border-red-400 rounded p-4"
      >
        <h4 class="text-md font-bold text-red-700 mb-3">
          Dry Periods for {{ tableTitleForSelected }}
        </h4>
        <div v-if="dryPeriods.length" class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-sm text-gray-600">
                <th class="py-1 px-2">Date</th>
                <th class="py-1 px-2">Soil Moisture</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in dryPeriods" :key="entry.date">
                <td class="py-1 px-2">{{ formatDate(entry.date) }}</td>
                <td class="py-1 px-2">{{ entry.moisture.toFixed(3) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-center text-gray-600">No dry periods found for this timeframe</p>
      </div>

      <!-- Current Year Table -->
      <div
        v-if="showDefaultTable || showComparison"
        class="bg-red-50 border border-red-400 rounded p-4"
      >
        <h4 class="text-md font-bold text-red-700 mb-3">
          Dry Periods for Current Year ({{ new Date().getFullYear() }})
        </h4>
        <div v-if="currentYearDryPeriods.length" class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-sm text-gray-600">
                <th class="py-1 px-2">Date</th>
                <th class="py-1 px-2">Soil Moisture</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in currentYearDryPeriods" :key="entry.date">
                <td class="py-1 px-2">{{ formatDate(entry.date) }}</td>
                <td class="py-1 px-2">{{ entry.moisture.toFixed(3) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-center text-gray-600">No dry periods found for this year</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import LineChart from '@/components/LineChart.vue'

// Constants for location coordinates
const LAT = 6.5
const LON = 11.5

// State Management
const viewType = ref('') // Controls view mode: 'specific' or 'forecast'
const selectedMonth = ref(new Date().getMonth() + 1) // Current month for specific view
const selectedYear = ref(new Date().getFullYear()) // Current year for specific view
const labels = ref([]) // X-axis labels for the chart
const chartData = ref([]) // Y-axis data for the chart
const dryPeriods = ref([]) // Stores dry periods for selected timeframe
const currentYearDryPeriods = ref([]) // Stores dry periods for current year
const isLoading = ref(false) // Controls loading state
const loadingProgress = ref(0) // Controls loading progress bar
const showDefaultTable = ref(true) // Controls visibility of default table
const showComparison = ref(false) // Controls visibility of comparison view

// Month names for display
const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

// Computed Properties
const years = computed(() => {
  // Generate last 5 years for selection
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => currentYear - i)
})

const chartTitle = computed(() => {
  // Dynamic chart title based on view type
  if (viewType.value === 'specific') {
    return `Soil Moisture for ${months[selectedMonth.value - 1]} ${selectedYear.value}`
  }
  return 'Soil Moisture Forecast (Next 7 Days)'
})

const tableTitleForSelected = computed(() => {
  // Dynamic table title based on view type
  if (viewType.value === 'specific') {
    return `${months[selectedMonth.value - 1]} ${selectedYear.value}`
  }
  return 'Next 7 Days'
})

// Utility Functions
function formatDate(dateStr) {
  // Format date string to readable format
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

// Loading Animation Control
async function startLoading() {
  isLoading.value = true
  loadingProgress.value = 0
  // Simulate progress with intervals
  const interval = setInterval(() => {
    loadingProgress.value += 10
    if (loadingProgress.value >= 90) clearInterval(interval)
  }, 100)
  return interval
}

// Data Fetching Functions
async function fetchData() {
  const loadingInterval = await startLoading()

  try {
    let url
    if (viewType.value === 'specific') {
      // Calculate date range for specific month view
      const startDate = `${selectedYear.value}-${String(selectedMonth.value).padStart(2, '0')}-01`
      const endDate = new Date(selectedYear.value, selectedMonth.value, 0)
        .toISOString()
        .split('T')[0]
      url = `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`
    } else {
      // Calculate date range for 7-day forecast
      const today = new Date()
      const startDate = today.toISOString().split('T')[0]
      const sevenDaysLater = new Date()
      sevenDaysLater.setDate(today.getDate() + 6)
      const endDate = sevenDaysLater.toISOString().split('T')[0]
      url = `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`
    }

    // Fetch and process data
    const response = await fetch(url)
    if (!response.ok) throw new Error('Network response was not ok')

    const data = await response.json()

    // Update chart data
    labels.value = data.daily.time
    chartData.value = data.daily.soil_moisture_0_to_10cm_mean

    // Filter dry periods (moisture < 0.2)
    dryPeriods.value = data.daily.time
      .map((date, i) => ({ date, moisture: data.daily.soil_moisture_0_to_10cm_mean[i] }))
      .filter((entry) => entry.moisture < 0.2)
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    // Clean up loading state
    clearInterval(loadingInterval)
    loadingProgress.value = 100
    setTimeout(() => {
      isLoading.value = false
      loadingProgress.value = 0
    }, 500)
  }
}

async function fetchCurrentYearData() {
  // Fetch entire current year's data
  const currentYear = new Date().getFullYear()
  const startDate = `${currentYear}-01-01`
  const endDate = `${currentYear}-12-31`

  try {
    const response = await fetch(
      `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`,
    )

    if (!response.ok) throw new Error('Network response was not ok')

    const data = await response.json()
    // Filter dry periods for current year
    currentYearDryPeriods.value = data.daily.time
      .map((date, i) => ({ date, moisture: data.daily.soil_moisture_0_to_10cm_mean[i] }))
      .filter((entry) => entry.moisture < 0.2)
  } catch (error) {
    console.error('Error fetching current year data:', error)
  }
}

// Lifecycle Hooks
onMounted(() => {
  // Initialize data on component mount
  fetchCurrentYearData()
  viewType.value = 'forecast'
  fetchCurrentYearData()
})

// Watchers
watch(viewType, (newVal) => {
  // Fetch new data when view type changes
  if (newVal) fetchData()
})
</script>
