<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import FarmMapDrawer from './FarmMapDrawer.vue'
import { PencilIcon, ArrowLeftIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const authStore = useAuthStore()
const router = useRouter()
const farm = ref<any>(null)
const isLoading = ref(true)
const mapLoading = ref(true)

const formattedDate = computed(() => {
  if (!farm.value?.created_at) return ''
  return new Date(farm.value.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const fetchFarm = async () => {
  isLoading.value = true
  try {
    const token = authStore.token || ''
    const farmId = route.query.farmId
    if (!farmId) return
    // Fetch all farms and find the one with the matching uuid
    const response = await api.fetchFarms(token)
    farm.value = response.data.find((f: any) => f.uuid === farmId)
  } catch (error) {
    console.error('Error fetching farm:', error)
  } finally {
    isLoading.value = false
  }
}

const handleMapLoaded = () => {
  mapLoading.value = false
}

onMounted(fetchFarm)

const goToEdit = () => {
  if (farm.value) {
    router.push(`/farm?editId=${farm.value.uuid}`)
  }
}

const goBack = () => {
  router.go(-1)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header Section -->
      <div class="flex items-center justify-between mb-6">
        <button 
          @click="goBack"
          class="flex items-center text-emerald-600 hover:text-emerald-800 transition-colors"
        >
          <ArrowLeftIcon class="h-5 w-5 mr-1" />
          <span class="font-medium">Back</span>
        </button>
        
        <h1 class="text-2xl md:text-3xl font-bold text-gray-800 flex items-center">
          <span class="hidden md:inline mr-2">Farm</span> Map View
        </h1>
        
        <div class="w-8"></div> <!-- Spacer for alignment -->
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
      </div>

      <!-- Farm Content -->
      <div v-else-if="farm" class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-200">
        <!-- Map Container -->
        <div class="relative h-[400px] md:h-[500px] w-full bg-gray-100">
          <div v-if="mapLoading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
            <div class="text-center">
              <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mx-auto mb-2"></div>
              <p class="text-gray-600">Loading map...</p>
            </div>
          </div>
          <FarmMapDrawer 
            :initialGeojson="farm.coordinates" 
            @loaded="handleMapLoaded"
            class="h-full w-full"
          />
        </div>

        <!-- Farm Details -->
        <div class="p-4 md:p-6 border-t border-gray-100">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h2 class="text-xl md:text-2xl font-semibold text-gray-800">{{ farm.name }}</h2>
              <p class="text-gray-500 mt-1 flex items-center">
                <span class="hidden md:inline">Created on</span>
                {{ formattedDate }}
              </p>
            </div>
            
            <div class="flex gap-3">
              <button 
                @click="goToEdit"
                class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors flex items-center"
              >
                <PencilIcon class="h-5 w-5 mr-2" />
                <span>Edit Farm</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Not Found State -->
      <div v-else class="bg-white rounded-xl shadow-sm p-8 text-center border border-gray-200">
        <div class="mx-auto w-24 h-24 text-gray-300 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-700 mb-2">Farm not found</h3>
        <p class="text-gray-500 mb-6">The farm you're looking for doesn't exist or you don't have permission to view it.</p>
        <button 
          @click="goBack"
          class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors inline-flex items-center"
        >
          <ArrowLeftIcon class="h-5 w-5 mr-2" />
          Return to Farms
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions for the map loading state */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .map-container {
    height: 350px;
  }
}
</style>