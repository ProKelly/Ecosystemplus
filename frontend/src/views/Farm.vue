<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { MapPinIcon, PlusIcon, PencilIcon, EyeIcon, TrashIcon } from '@heroicons/vue/24/outline'
import FarmMapDrawer from '@/components/farm/FarmMapDrawer.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

interface Farm {
  uuid: string
  name: string
  coordinates?: any
  created_at: string
  size?: number
  location?: string
}

const router = useRouter()
const authStore = useAuthStore()

// Farm data state
const farms = ref<Farm[]>([])
const isLoading = ref(false)
const showAddForm = ref(false)
const showEditForm = ref(false)
const newFarm = ref({
  name: '',
  coordinates: null as any
})
const editFarm = ref({
  uuid: '',
  name: '',
  coordinates: null as any
})
const mapDialog = ref(false)
const mapKey = ref(0) // Used to force re-render map
const mapComponent = ref() // Template ref for FarmMapDrawer

// Fetch farms from API
const fetchFarms = async () => {
  isLoading.value = true
  try {
    const token = authStore.token
    const response = await api.fetchFarms(token)
    farms.value = response.data.map((farm: Farm) => ({
      ...farm,
      // Calculate size in hectares if coordinates exist
      size: farm.coordinates ? calculateArea(farm.coordinates) : 0,
      // Extract location from coordinates if needed
      location: farm.coordinates ? 'Custom Boundary' : 'Location not set'
    }))
  } catch (error) {
    console.error('Error fetching farms:', error)
  } finally {
    isLoading.value = false
  }
}

// Calculate area in hectares from GeoJSON coordinates
const calculateArea = (coordinates: any) => {
  if (!coordinates || !coordinates.coordinates) return 0
  
  // Simple approximation - in a real app, use proper geodesic calculation
  const polygon = coordinates.coordinates[0]
  let area = 0
  const n = polygon.length
  
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n
    const xi = polygon[i][0]
    const yi = polygon[i][1]
    const xj = polygon[j][0]
    const yj = polygon[j][1]
    
    area += xi * yj - xj * yi
  }
  
  area = Math.abs(area) / 2
  // Convert to hectares (very rough approximation)
  return (area * 10000).toFixed(2)
}

onMounted(fetchFarms)

// Add new farm
const addFarm = async () => {
  if (!newFarm.value.name) return
  isLoading.value = true
  try {
    const token = authStore.token
    const response = await api.addFarm({
      name: newFarm.value.name,
      coordinates: getPolygonGeometry(newFarm.value.coordinates)
    }, token)
    farms.value.push({
      ...response.data,
      size: response.data.coordinates ? calculateArea(response.data.coordinates) : 0,
      location: response.data.coordinates ? 'Custom Boundary' : 'Location not set'
    })
    showAddForm.value = false
    newFarm.value = { name: '', coordinates: null }
  } catch (error) {
    console.error('Error adding farm:', error)
  } finally {
    isLoading.value = false
  }
}

// Edit farm
const editFarmData = async () => {
  if (!editFarm.value.name) return
  isLoading.value = true
  try {
    const token = authStore.token
    const response = await api.updateFarm(editFarm.value.uuid, {
      name: editFarm.value.name,
      coordinates: getPolygonGeometry(editFarm.value.coordinates)
    }, token)
    farms.value = farms.value.map(f =>
      f.uuid === editFarm.value.uuid
        ? {
          ...response.data,
          size: response.data.coordinates ? calculateArea(response.data.coordinates) : 0,
          location: response.data.coordinates ? 'Custom Boundary' : 'Location not set'
        }
        : f
    )
    showEditForm.value = false
    editFarm.value = { uuid: '', name: '', coordinates: null }
  } catch (error) {
    console.error('Error updating farm:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete farm
const deleteFarm = async (farmId: string) => {
  if (!confirm('Are you sure you want to delete this farm?')) return
  isLoading.value = true
  try {
    const token = authStore.token
    await api.deleteFarm(farmId, token)
    farms.value = farms.value.filter(f => f.uuid !== farmId)
  } catch (error) {
    console.error('Error deleting farm:', error)
  } finally {
    isLoading.value = false
  }
}

// Open edit form
const openEditForm = (farm: Farm) => {
  editFarm.value = {
    uuid: farm.uuid,
    name: farm.name,
    coordinates: farm.coordinates || null
  }
  showEditForm.value = true
}

// View farm on map
const viewFarm = (farmId: string) => {
  router.push(`/map?farmId=${farmId}`)
}

// Handle map drawing complete
const handleMapComplete = (geojson: any) => {
  if (showAddForm.value) {
    newFarm.value.coordinates = geojson
  } else if (showEditForm.value) {
    editFarm.value.coordinates = geojson
  }
  mapDialog.value = false
  mapKey.value++ // Force map re-render
}

// Format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Ensure map resizes when dialog opens
watch(mapDialog, async (val) => {
  if (val) {
    await nextTick()
    // Wait for DOM to render, then invalidate map size
    if (
      mapComponent.value &&
      mapComponent.value.mapContainer &&
      mapComponent.value.mapContainer.value &&
      mapComponent.value.map
    ) {
      setTimeout(() => {
        mapComponent.value.map.invalidateSize()
      }, 200)
    }
  }
})

// Helper to extract geometry from GeoJSON Feature
function getPolygonGeometry(geojson: any) {
  // If it's a Feature, return its geometry, else return as is
  if (geojson && geojson.type === 'Feature' && geojson.geometry) {
    return geojson.geometry;
  }
  return geojson;
}
</script>

<template>
  <div class="flex flex-col min-h-screen p-4 md:p-6 bg-gray-50">
    <div class="max-w-7xl mx-auto w-full">
      <h1 class="text-2xl md:text-3xl font-bold text-gray-800 mb-6 flex items-center">
        <MapPinIcon class="h-6 w-6 mr-2 text-emerald-600" />
        Farm Management
      </h1>

      <!-- Add Farm Button -->
      <button 
        class="mb-6 flex items-center px-4 py-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors shadow-sm w-full md:w-auto justify-center"
        @click="showAddForm = true"
        :disabled="isLoading"
      >
        <PlusIcon class="h-5 w-5 mr-2" />
        Add New Farm
      </button>

      <!-- Farm List -->
      <div v-if="isLoading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
      </div>
      
      <div v-else-if="farms.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 py-3">
        <div 
          v-for="farm in farms" 
          :key="farm.uuid"
          class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-emerald-300 hover:shadow-md transition-all"
        >
          <div class="flex justify-between items-start">
            <h3 class="font-semibold text-lg text-gray-800">{{ farm.name }}</h3>
            <button 
              @click="deleteFarm(farm.uuid)"
              class="text-gray-400 hover:text-red-500 transition-colors"
              title="Delete farm"
            >
              <TrashIcon class="h-5 w-5" />
            </button>
          </div>
          
          <div class="mt-2 flex items-center text-sm text-gray-600">
            <MapPinIcon class="h-4 w-4 mr-1" />
            {{ farm.location }}
          </div>
          
          <div v-if="farm.size" class="mt-1 text-sm text-gray-600">
            <span class="font-medium">{{ farm.size }} ha</span>
          </div>
          
          <p class="text-xs text-gray-500 mt-2">Created: {{ formatDate(farm.created_at) }}</p>
          
          <div class="mt-4 flex gap-2">
            <button 
              class="flex-1 px-3 py-1.5 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 transition-colors flex items-center justify-center"
              @click="viewFarm(farm.uuid)"
              title="View"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-12">
        <div class="mx-auto w-24 h-24 text-gray-300 mb-4">
          <MapPinIcon class="opacity-50" />
        </div>
        <h3 class="text-lg font-medium text-gray-700">No farms registered yet</h3>
        <p class="mt-1 text-gray-500">Get started by adding your first farm</p>
        <button 
          class="mt-4 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors inline-flex items-center"
          @click="showAddForm = true"
        >
          <PlusIcon class="h-5 w-5 mr-2" />
          Add Farm
        </button>
      </div>

      <!-- Add Farm Modal -->
      <div v-if="showAddForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Add New Farm</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Farm Name *</label>
              <input 
                v-model="newFarm.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                placeholder="My Farm"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Farm Boundary</label>
              <button
                @click="mapDialog = true"
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-left text-gray-600 hover:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                {{ newFarm.coordinates ? 'Boundary set (click to edit)' : 'Click to draw farm boundary on map' }}
              </button>
              <p class="text-xs text-gray-500 mt-1">Draw your farm's shape on the map</p>
            </div>
          </div>
          
          <div class="mt-6 flex gap-3">
            <button 
              class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50"
              @click="addFarm"
              :disabled="isLoading || !newFarm.name"
            >
              {{ isLoading ? 'Saving...' : 'Add Farm' }}
            </button>
            <button 
              class="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
              @click="showAddForm = false"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>

      <!-- Edit Farm Modal -->
      <div v-if="showEditForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white p-6 rounded-lg w-full max-w-md">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Edit Farm</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Farm Name *</label>
              <input 
                v-model="editFarm.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                placeholder="My Farm"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Farm Boundary</label>
              <button
                @click="mapDialog = true"
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-left text-gray-600 hover:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                {{ editFarm.coordinates ? 'Boundary set (click to edit)' : 'Click to draw farm boundary on map' }}
              </button>
              <p class="text-xs text-gray-500 mt-1">Update your farm's shape on the map</p>
            </div>
          </div>
          
          <div class="mt-6 flex gap-3">
            <button 
              class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50"
              @click="editFarmData"
              :disabled="isLoading || !editFarm.name"
            >
              {{ isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
            <button 
              class="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
              @click="showEditForm = false"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>

      <!-- Map Dialog for Drawing Boundaries -->
      <div v-if="mapDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] flex flex-col">
          <div class="p-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-800">
              {{ showAddForm ? 'Draw Farm Boundary' : 'Edit Farm Boundary' }}
            </h2>
          </div>
          
          <div class="flex-1 overflow-hidden min-h-[400px]">
            <!-- Map Component -->
            <FarmMapDrawer
              ref="mapComponent"
              :key="mapKey"
              :initialGeojson="showAddForm ? newFarm.coordinates : editFarm.coordinates"
              @complete="handleMapComplete"
              @cancel="mapDialog = false"
              class="h-full min-h-[400px]"
            />
          </div>
          
          <div class="p-4 border-t border-gray-200 bg-gray-50">
            <div class="flex justify-end gap-3">
              <button
                @click="mapDialog = false"
                class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
              <button
                @click="$refs.mapComponent.saveDrawing()"
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors"
              >
                Save Boundary
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions for modals */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-content-enter-active,
.modal-content-leave-active {
  transition: all 0.3s ease;
}

.modal-content-enter-from,
.modal-content-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>