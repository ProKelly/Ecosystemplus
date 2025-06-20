<template>
  <div class="min-h-screen bg-gray-50 py-20">
    <main class="max-w-7xl mx-auto px-3 py-3 sm:px-4 sm:py-4 lg:px-6">
      <!-- Forest Selection - Compact on mobile -->
      <div class="bg-white rounded-lg shadow p-3 mb-4 sm:mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Select Forest</label>
            <div class="flex flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0">
              <select 
                v-model="selectedForestId" 
                @change="loadForestData"
                class="flex-1 p-2 border border-gray-300 rounded-md text-sm focus:ring-green-500 focus:border-green-500"
              >
                <option value="">Choose a forest</option>
                <option v-for="forest in userForests" :key="forest.id" :value="forest.id">
                  {{ forest.name }} ({{ formatArea(forest.area) }})
                </option>
              </select>
              <router-link 
                to="/register-forest"
                class="px-3 py-2 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 flex items-center justify-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                <span class="hidden sm:inline">Register New</span>
                <span class="sm:hidden">New</span>
              </router-link>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Time Range</label>
            <select 
              v-model="timeRange" 
              @change="fetchAnalysisData"
              class="w-full p-2 border border-gray-300 rounded-md text-sm focus:ring-green-500 focus:border-green-500"
            >
              <option value="7">7 days</option>
              <option value="30">30 days</option>
              <option value="90">3 months</option>
              <option value="365">1 year</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Dashboard Content -->
      <div v-if="selectedForest" class="space-y-3 sm:space-y-4">
        <!-- Overview Cards - Stack on small screens -->
        <div class="grid grid-cols-2 gap-2 sm:grid-cols-4 sm:gap-3">
          <OverviewCard 
            title="Vegetation" 
            :value="currentAnalysis.ndvi" 
            :previousValue="previousAnalysis.ndvi"
            unit="NDVI"
            icon="leaf"
            :goodThreshold="0.6"
            class="h-full"
          />
          <OverviewCard 
            title="Moisture" 
            :value="currentAnalysis.ndmi" 
            :previousValue="previousAnalysis.ndmi"
            unit="NDMI"
            icon="water"
            :goodThreshold="0.4"
            class="h-full"
          />
          <OverviewCard 
            title="Drought" 
            :value="currentAnalysis.spi" 
            :previousValue="previousAnalysis.spi"
            unit="SPI"
            icon="sun"
            :inverted="true"
            :goodThreshold="-1"
            class="h-full"
          />
          <OverviewCard 
            title="Fire Risk" 
            :value="fireRiskScore" 
            :previousValue="previousFireRisk"
            unit="Index"
            icon="fire"
            :goodThreshold="30"
            :inverted="true"
            class="h-full"
          />
        </div>

        <!-- Map and Trends - Stack on mobile -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 sm:gap-4">
          <!-- Map Container -->
          <div class="lg:col-span-2 bg-white rounded-lg shadow overflow-hidden">
            <div id="map" class="h-60 sm:h-72 md:h-80 w-full"></div>
            <div class="p-2 bg-gray-50 border-t border-gray-200">
              <p class="text-xs sm:text-sm text-gray-700 truncate">
                <span class="font-medium">{{ selectedForest.name }}</span>
                <span class="mx-1">•</span>
                <span>{{ formatArea(selectedForest.area) }}</span>
                <span class="mx-1">•</span>
                <span>Updated: {{ lastAnalyzedDate }}</span>
              </p>
            </div>
          </div>

          <!-- Changes Summary -->
          <div class="space-y-3">
            <div class="bg-white rounded-lg shadow p-3">
              <h3 class="text-sm font-semibold text-gray-900 mb-2">Recent Changes</h3>
              <div class="space-y-2">
                <ChangeIndicator 
                  v-for="change in significantChanges"
                  :key="change.id"
                  :type="change.type"
                  :value="change.value"
                  :description="change.description"
                  :severity="change.severity"
                />
              </div>
            </div>

            <div class="bg-white rounded-lg shadow p-3">
              <h3 class="text-sm font-semibold text-gray-900 mb-2">Actions</h3>
              <button 
                @click="showReportModal = true"
                class="w-full flex items-center justify-center px-3 py-1.5 bg-green-600 text-white rounded-md text-xs sm:text-sm hover:bg-green-700 mb-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Generate Report
              </button>
              <button 
                @click="analyzeCurrentForest"
                class="w-full flex items-center justify-center px-3 py-1.5 bg-blue-600 text-white rounded-md text-xs sm:text-sm hover:bg-blue-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Analyze Now
              </button>
            </div>
          </div>
        </div>

        <!-- Detailed Analysis -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="border-b border-gray-200 overflow-x-auto">
            <nav class="flex whitespace-nowrap">
              <button 
                v-for="tab in analysisTabs" 
                :key="tab.id" 
                @click="activeTab = tab.id"
                :class="{'border-green-600 text-green-700': activeTab === tab.id}" 
                class="px-3 py-2 border-b-2 font-medium text-xs sm:text-sm border-transparent text-gray-500 hover:text-gray-700"
              >
                {{ tab.label }}
              </button>
            </nav>
          </div>
          
          <div class="p-3">
            <!-- Health Trends -->
            <div v-if="activeTab === 'health'">
              <h3 class="text-sm font-semibold text-gray-900 mb-2 sm:mb-3">Health Trends</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
                <div class="h-40 sm:h-48 md:h-56">
                  <LineChart 
                    title="Vegetation (NDVI)" 
                    :data="ndviHistory" 
                    :currentValue="currentAnalysis.ndvi"
                    :previousValue="previousAnalysis.ndvi"
                    color="#10b981"
                  />
                </div>
                <div class="h-40 sm:h-48 md:h-56">
                  <LineChart 
                    title="Moisture (NDMI)" 
                    :data="ndmiHistory" 
                    :currentValue="currentAnalysis.ndmi"
                    :previousValue="previousAnalysis.ndmi"
                    color="#3b82f6"
                  />
                </div>
              </div>
            </div>

            <!-- Threats Analysis -->
            <div v-if="activeTab === 'threats'">
              <h3 class="text-sm font-semibold text-gray-900 mb-2 sm:mb-3">Threat Analysis</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
                <div class="h-40 sm:h-48 md:h-56">
                  <LineChart 
                    title="Drought (SPI)" 
                    :data="spiHistory" 
                    :currentValue="currentAnalysis.spi"
                    :previousValue="previousAnalysis.spi"
                    color="#f59e0b"
                    :inverted="true"
                  />
                </div>
                <div class="h-40 sm:h-48 md:h-56">
                  <LineChart 
                    title="Fire Risk" 
                    :data="fireRiskHistory" 
                    :currentValue="fireRiskScore"
                    :previousValue="previousFireRisk"
                    color="#ef4444"
                    :inverted="true"
                  />
                </div>
              </div>
            </div>

            <!-- Change Detection -->
            <div v-if="activeTab === 'changes'">
              <h3 class="text-sm font-semibold text-gray-900 mb-2 sm:mb-3">Change Detection</h3>
              <div class="h-40 sm:h-56 md:h-64 bg-gray-50 rounded-lg flex items-center justify-center border border-gray-200">
                <p class="text-gray-500 text-xs sm:text-sm">Change detection map visualization</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State - Compact on mobile -->
      <div v-else class="bg-white rounded-lg shadow p-4 sm:p-6 text-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 sm:h-10 w-8 sm:w-10 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
        </svg>
        <h3 class="mt-2 text-base sm:text-lg font-medium text-gray-900">No forest selected</h3>
        <p class="mt-1 text-xs sm:text-sm text-gray-500">Choose or register a forest to begin monitoring</p>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import OverviewCard from '../components/forest-monitoring/OverviewCard.vue'
import ChangeIndicator from '../components/forest-monitoring/ChangeIndicator.vue'
import LineChart from '../components/forest-monitoring/LineChart.vue'
import { useRouter } from 'vue-router'

export default {
  components: { OverviewCard, ChangeIndicator, LineChart },
  setup() {
    const router = useRouter()
    let map = null
    let drawnItems = null

    // State
    const selectedForestId = ref('')
    const selectedForest = ref(null)
    const timeRange = ref('30')
    const activeTab = ref('health')
    const showReportModal = ref(false)
    const isLoading = ref(false)

    // Forest data
    const userForests = ref([
      { id: '1', name: 'Bamenda Conservation Zone', area: 1245.3, coordinates: [[5.9631, 10.1591], [5.9831, 10.1791], [5.9531, 10.1791]] },
      { id: '2', name: 'Korup National Park', area: 1259.7, coordinates: [[5.2631, 9.8591], [5.2831, 9.8791], [5.2531, 9.8791]] }
    ])

    // Analysis data
    const currentAnalysis = ref({
      ndvi: 0,
      ndmi: 0,
      spi: 0,
      date: null
    })

    const previousAnalysis = ref({
      ndvi: 0,
      ndmi: 0,
      spi: 0,
      date: null
    })

    const analysisTabs = ref([
      { id: 'health', label: 'Health Trends' },
      { id: 'threats', label: 'Threat Analysis' },
      { id: 'changes', label: 'Change Detection' }
    ])

    // Chart data
    const ndviHistory = ref(generateHistoryData(12, 0.3, 0.9))
    const ndmiHistory = ref(generateHistoryData(12, 0.2, 0.8))
    const spiHistory = ref(generateHistoryData(12, -2.5, 2.5))
    const fireRiskHistory = ref(generateHistoryData(12, 0, 100))

    // Computed properties
    const fireRiskScore = computed(() => {
      const moistureFactor = 1 - (currentAnalysis.value.ndmi || 0.5)
      const vegetationFactor = currentAnalysis.value.ndvi || 0.6
      return Math.min(100, Math.round(moistureFactor * 70 + vegetationFactor * 30))
    })

    const previousFireRisk = computed(() => {
      const moistureFactor = 1 - (previousAnalysis.value.ndmi || 0.5)
      const vegetationFactor = previousAnalysis.value.ndvi || 0.6
      return Math.min(100, Math.round(moistureFactor * 70 + vegetationFactor * 30))
    })

    const lastAnalyzedDate = computed(() => {
      return currentAnalysis.value.date ? new Date(currentAnalysis.value.date).toLocaleDateString() : 'Never'
    })

    const significantChanges = computed(() => {
      const changes = []
      
      // Vegetation change
      const ndviChange = currentAnalysis.value.ndvi - previousAnalysis.value.ndvi
      if (Math.abs(ndviChange) > 0.1) {
        changes.push({
          id: 'ndvi-change',
          type: 'vegetation',
          value: ndviChange,
          description: ndviChange > 0 ? 'Vegetation improvement' : 'Vegetation decline',
          severity: Math.abs(ndviChange) > 0.2 ? 'high' : 'medium'
        })
      }
      
      // Moisture change
      const ndmiChange = currentAnalysis.value.ndmi - previousAnalysis.value.ndmi
      if (Math.abs(ndmiChange) > 0.1) {
        changes.push({
          id: 'ndmi-change',
          type: 'moisture',
          value: ndmiChange,
          description: ndmiChange > 0 ? 'Increased moisture' : 'Decreased moisture',
          severity: Math.abs(ndmiChange) > 0.15 ? 'high' : 'medium'
        })
      }
      
      // Fire risk change
      const fireRiskChange = fireRiskScore.value - previousFireRisk.value
      if (Math.abs(fireRiskChange) > 15) {
        changes.push({
          id: 'fire-risk-change',
          type: 'fire',
          value: fireRiskChange,
          description: fireRiskChange > 0 ? 'Increased fire risk' : 'Decreased fire risk',
          severity: Math.abs(fireRiskChange) > 25 ? 'high' : 'medium'
        })
      }
      
      return changes
    })

    // Initialize main map
    const initMainMap = () => {
      map = L.map('map').setView([5.9631, 10.1591], 10)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map)
      
      drawnItems = new L.FeatureGroup()
      map.addLayer(drawnItems)
    }

    const loadForestData = async () => {
      if (!selectedForestId.value) {
        selectedForest.value = null
        return
      }
      
      isLoading.value = true
      
      const forest = userForests.value.find(f => f.id === selectedForestId.value)
      if (!forest) return
      
      selectedForest.value = forest
      
      drawnItems.clearLayers()
      const polygon = L.polygon(forest.coordinates, {
        color: '#10b981',
        fillColor: '#10b981',
        fillOpacity: 0.2
      }).addTo(drawnItems)
      map.fitBounds(polygon.getBounds())
      
      await fetchAnalysisData()
      
      isLoading.value = false
    }

    const fetchAnalysisData = async () => {
      if (!selectedForest.value) return
      
      try {
        currentAnalysis.value = {
          ndvi: 0.72,
          ndmi: 0.45,
          spi: -0.8,
          date: new Date().toISOString()
        }
        
        previousAnalysis.value = {
          ndvi: 0.68,
          ndmi: 0.52,
          spi: -0.3,
          date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()
        }
        
        ndviHistory.value = generateHistoryData(12, 0.3, 0.9)
        ndmiHistory.value = generateHistoryData(12, 0.2, 0.8)
        spiHistory.value = generateHistoryData(12, -2.5, 2.5)
        fireRiskHistory.value = generateHistoryData(12, 0, 100)
      } catch (error) {
        console.error('Error fetching analysis data:', error)
      }
    }

    const analyzeCurrentForest = async () => {
      if (!selectedForest.value) return
      
      isLoading.value = true
      
      try {
        currentAnalysis.value = {
          ndvi: +(currentAnalysis.value.ndvi + (Math.random() * 0.1 - 0.05)).toFixed(2),
          ndmi: +(currentAnalysis.value.ndmi + (Math.random() * 0.1 - 0.05)).toFixed(2),
          spi: +(currentAnalysis.value.spi + (Math.random() * 0.5 - 0.25)).toFixed(2),
          date: new Date().toISOString()
        }
        
        await fetchAnalysisData()
      } catch (error) {
        console.error('Error analyzing forest:', error)
      } finally {
        isLoading.value = false
      }
    }

    const generateReport = () => {
      alert('Report generation started. You will receive it shortly.')
      showReportModal.value = false
    }

    const refreshData = () => {
      if (selectedForest.value) {
        fetchAnalysisData()
      }
    }

    const formatArea = (area) => {
      return area >= 100 ? `${(area / 100).toFixed(1)} hectares` : `${area.toFixed(1)} acres`
    }

    function generateHistoryData(count, min, max) {
      return Array.from({ length: count }, (_, i) => ({
        x: new Date(Date.now() - (count - i - 1) * 30 * 24 * 60 * 60 * 1000),
        y: +(min + Math.random() * (max - min)).toFixed(2)
      }))
    }

    watch(selectedForest, (newVal) => {
      if (newVal && !map) {
        nextTick(() => {
          initMainMap()
        })
      }
    })

    return {
      selectedForestId,
      selectedForest,
      timeRange,
      activeTab,
      showReportModal,
      isLoading,
      userForests,
      currentAnalysis,
      previousAnalysis,
      analysisTabs,
      ndviHistory,
      ndmiHistory,
      spiHistory,
      fireRiskHistory,
      fireRiskScore,
      previousFireRisk,
      lastAnalyzedDate,
      significantChanges,
      loadForestData,
      analyzeCurrentForest,
      generateReport,
      refreshData,
      formatArea
    }
  }
}
</script>

<style>
#map {
  z-index: 0;
}

@media (max-width: 640px) {
  #map {
    height: 250px;
  }
}
</style>