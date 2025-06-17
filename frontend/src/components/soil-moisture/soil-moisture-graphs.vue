<template>
  <section class="bg-white py-10 px-6 md:px-16 lg:px-24 text-gray-800 shadow-md">
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

    <!-- Error Section -->
    <div v-if="error" class="text-center text-red-600 my-4">
      <p class="mb-2">{{ error }}</p>
      <button @click="retryFetch" class="bg-red-600 hover:bg-red-700 text-white py-1 px-4 rounded">
        Try Again
      </button>
    </div>
    <!-- Chart Section -->
    <div v-if="!error">
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
        <div
          class="flex justify-between items-center"
          style="margin-top: 10px; margin-bottom: 10px"
        >
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
              :class="
                showDefaultTable
                  ? 'bg-green-600 text-white'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              "
              style="margin-right: 3px"
            >
              Current Year Only
            </button>
            <button
              @click="() => (showComparison = true)"
              class="text-sm px-3 py-1 rounded"
              :class="
                showComparison
                  ? 'bg-green-600 text-white'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              "
            >
              Selected Period
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

        <!-- Current Year Table (Grouped by Month) -->
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
                  <th class="py-1 px-2">Start – End</th>
                  <th class="py-1 px-2">Average Moisture</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(entry, index) in currentYearDryPeriods" :key="index">
                  <td class="py-1 px-2">
                    {{ formatDate(entry.start) }} – {{ formatDate(entry.end) }}
                  </td>
                  <td class="py-1 px-2">{{ entry.avgMoisture }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else class="text-center text-gray-600">No dry periods found for this year</p>
        </div>
      </div>
    </div>
  </section>
</template>

<!-- CHANGES IN SCRIPT SECTION -->
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import LineChart from '@/components/LineChart.vue'

// Constants
const LAT = 6.5
const LON = 11.5

// State
const viewType = ref('')
const selectedMonth = ref(new Date().getMonth() + 1)
const selectedYear = ref(new Date().getFullYear())
const labels = ref([])
const chartData = ref([])
const dryPeriods = ref([])
const currentYearDryPeriodsRaw = ref([])
const currentYearDryPeriods = ref([])
const isLoading = ref(false)
const loadingProgress = ref(0)
const showDefaultTable = ref(true)
const showComparison = ref(false)

const error = ref('')

const lastFetchType = (ref < 'current') | 'forecast' | (null > null)

// Month labels
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

const years = computed(() => {
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => currentYear - i)
})

const chartTitle = computed(() => {
  if (viewType.value === 'specific') {
    return `Soil Moisture for ${months[selectedMonth.value - 1]} ${selectedYear.value}`
  }
  return 'Soil Moisture Forecast (Next 7 Days)'
})

const tableTitleForSelected = computed(() => {
  if (viewType.value === 'specific') {
    return `${months[selectedMonth.value - 1]} ${selectedYear.value}`
  }
  return 'Next 7 Days'
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

// Simulated loader
async function startLoading() {
  isLoading.value = true
  loadingProgress.value = 0
  const interval = setInterval(() => {
    loadingProgress.value += 10
    if (loadingProgress.value >= 90) clearInterval(interval)
  }, 100)
  return interval
}

// Group consecutive dry days for current year
function groupDryPeriodsByMonth(data) {
  const groups = []
  let currentGroup = []
  let currentMonth = null

  for (let i = 0; i < data.length; i++) {
    const entry = data[i]
    const date = new Date(entry.date)
    const month = date.getMonth()
    const moisture = entry.moisture

    if (moisture >= 0.2) {
      if (currentGroup.length > 0) {
        const start = currentGroup[0].date
        const end = currentGroup[currentGroup.length - 1].date
        const avgMoisture = (
          currentGroup.reduce((sum, e) => sum + e.moisture, 0) / currentGroup.length
        ).toFixed(3)
        groups.push({ start, end, avgMoisture })
        currentGroup = []
      }
    } else {
      if (currentMonth === null || currentMonth === month) {
        currentGroup.push(entry)
      } else {
        if (currentGroup.length > 0) {
          const start = currentGroup[0].date
          const end = currentGroup[currentGroup.length - 1].date
          const avgMoisture = (
            currentGroup.reduce((sum, e) => sum + e.moisture, 0) / currentGroup.length
          ).toFixed(3)
          groups.push({ start, end, avgMoisture })
          currentGroup = []
        }
        currentGroup.push(entry)
      }
      currentMonth = month
    }
  }

  if (currentGroup.length > 0) {
    const start = currentGroup[0].date
    const end = currentGroup[currentGroup.length - 1].date
    const avgMoisture = (
      currentGroup.reduce((sum, e) => sum + e.moisture, 0) / currentGroup.length
    ).toFixed(3)
    groups.push({ start, end, avgMoisture })
  }

  return groups
}

// Fetch data for selected month or forecast
async function fetchData() {
  const loadingInterval = await startLoading()
  error.value = '' // clear previous errors
  try {
    let url
    if (viewType.value === 'specific') {
      const startDate = `${selectedYear.value}-${String(selectedMonth.value).padStart(2, '0')}-01`
      const endDate = new Date(selectedYear.value, selectedMonth.value, 0)
        .toISOString()
        .split('T')[0]
      url = `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`
    } else {
      const today = new Date()
      const startDate = today.toISOString().split('T')[0]
      const endDate = new Date(today.setDate(today.getDate() + 6)).toISOString().split('T')[0]
      url = `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`
    }

    const response = await fetch(url)
    if (!response.ok) throw new Error('Network response was not ok')
    const data = await response.json()

    labels.value = data.daily.time
    chartData.value = data.daily.soil_moisture_0_to_10cm_mean

    dryPeriods.value = data.daily.time
      .map((date, i) => ({ date, moisture: data.daily.soil_moisture_0_to_10cm_mean[i] }))
      .filter((entry) => entry.moisture < 0.2)

    // If it's a specific month, auto-switch to second tab
    if (viewType.value === 'specific') {
      showComparison.value = true
      showDefaultTable.value = false
    }
  } catch (err) {
    console.error('Error fetching data:', err)
    error.value = 'Failed to fetch soil moisture data. Please check your internet and try again.'
  } finally {
    clearInterval(loadingInterval)
    loadingProgress.value = 100
    setTimeout(() => {
      isLoading.value = false
      loadingProgress.value = 0
    }, 500)
  }
}

// Fetch current year’s data and group
async function fetchCurrentYearData() {
  const currentYear = new Date().getFullYear()
  const startDate = `${currentYear}-01-01`
  const endDate = `${currentYear}-12-31`
  error.value = ''
  try {
    const response = await fetch(
      `https://climate-api.open-meteo.com/v1/climate?latitude=${LAT}&longitude=${LON}&start_date=${startDate}&end_date=${endDate}&daily=soil_moisture_0_to_10cm_mean&models=MRI_AGCM3_2_S`,
    )

    if (!response.ok) throw new Error('Network response was not ok')

    if (!response.ok) throw new Error('Network error')
    const data = await response.json()
    const entries = data.daily.time
      .map((date, i) => ({ date, moisture: data.daily.soil_moisture_0_to_10cm_mean[i] }))
      .filter((entry) => entry.moisture < 0.2)

    currentYearDryPeriodsRaw.value = entries
    currentYearDryPeriods.value = groupDryPeriodsByMonth(entries)
  } catch (err) {
    console.error('Error fetching current year data:', err)
    error.value = 'Failed to load dry periods for current year. Please try again.'
  }
}
async function retryFetch() {
  error.value = ''
  await fetchCurrentYearData()
  await fetchData()
}

onMounted(() => {
  fetchCurrentYearData()
  viewType.value = 'forecast'
  fetchData() // Initial fetch for forecast data
})

watch(viewType, (newVal) => {
  if (newVal) fetchData()
})

watch([selectedMonth, selectedYear], ([newMonth, newYear], [oldMonth, oldYear]) => {
  if (viewType.value === 'specific' && (newMonth !== oldMonth || newYear !== oldYear)) {
    fetchData() // Auto-fetch when month or year changes
  }
})
</script>
