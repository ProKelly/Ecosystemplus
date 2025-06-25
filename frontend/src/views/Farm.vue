<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { MapPinIcon, PlusIcon, PencilIcon, EyeIcon } from '@heroicons/vue/24/outline'

// Router for navigation
const router = useRouter()

// Farm data state
const farms = ref([
  { id: 1, name: 'Main Field', location: 'Nairobi', size: 4.2, date: '2023-10-15' },
  { id: 2, name: 'North Plot', location: 'Kiambu', size: 2.8, date: '2023-09-22' },
  { id: 3, name: 'River Side', location: 'Machakos', size: 3.5, date: '2023-11-05' }
])
const isLoading = ref(false)
const showAddForm = ref(false)
const showEditForm = ref(false)
const newFarm = ref({ name: '', location: '' })
const editFarm = ref({ id: 0, name: '', location: '' })

// Fetch farms (replace with API call)
onMounted(async () => {
  isLoading.value = true
  // TODO: Replace with actual API call
  // const response = await axios.get('/api/farms')
  // farms.value = response.data
  isLoading.value = false
})

// Add new farm
async function addFarm() {
  if (!newFarm.value.name || !newFarm.value.location) return
  isLoading.value = true

  // Simulate API call
  const newFarmData = {
    id: farms.value.length + 1,
    name: newFarm.value.name,
    location: newFarm.value.location,
    size: 0, // Size will be updated after boundary drawing
    date: new Date().toISOString().split('T')[0]
  }

  // TODO: Replace with actual API call
  // const response = await axios.post('/api/farms', newFarmData)
  // farms.value.push(response.data)

  farms.value.push(newFarmData)
  showAddForm.value = false
  newFarm.value = { name: '', location: '' }

  // Redirect to map for drawing boundaries
  router.push(`/map?farmId=${newFarmData.id}`)
  isLoading.value = false
}

// Edit farm
async function editFarmData() {
  if (!editFarm.value.name || !editFarm.value.location) return
  isLoading.value = true

  // Simulate API call
  const updatedFarm = {
    id: editFarm.value.id,
    name: editFarm.value.name,
    location: editFarm.value.location,
    size: farms.value.find(f => f.id === editFarm.value.id)?.size || 0,
    date: farms.value.find(f => f.id === editFarm.value.id)?.date || ''
  }

  // TODO: Replace with actual API call
  // await axios.put(`/api/farms/${editFarm.value.id}`, updatedFarm)

  farms.value = farms.value.map(f => f.id === editFarm.value.id ? updatedFarm : f)
  showEditForm.value = false
  editFarm.value = { id: 0, name: '', location: '' }
  isLoading.value = false
}

// Open edit form
function openEditForm(farm: any) {
  editFarm.value = { id: farm.id, name: farm.name, location: farm.location }
  showEditForm.value = true
}

// View farm on map
function viewFarm(farmId: number) {
  router.push(`/map?farmId=${farmId}`)
}
</script>

<template>
  <div class="flex flex-col min-h-screen p-4 md:p-6 bg-gray-50">
    <h1 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
      <MapPinIcon class="h-6 w-6 mr-2 text-emerald-600" />
      Farm Management
    </h1>

    <!-- Add Farm Button -->
    <button 
      class="mb-6 flex items-center px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors w-full md:w-auto"
      @click="showAddForm = true"
      :disabled="isLoading"
    >
      <PlusIcon class="h-5 w-5 mr-2" />
      Add New Farm
    </button>

    <!-- Farm List -->
    <div v-if="isLoading" class="text-center text-gray-500">Loading farms...</div>
    <div v-else-if="farms.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="farm in farms" 
        :key="farm.id"
        class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-emerald-300 hover:bg-emerald-50 transition-colors"
      >
        <h3 class="font-semibold text-gray-800">{{ farm.name }}</h3>
        <p class="text-sm text-gray-600">{{ farm.location }} • {{ farm.size }} ha</p>
        <p class="text-xs text-gray-500 mt-1">Added: {{ farm.date }}</p>
        <div class="mt-3 flex gap-2">
          <button 
            class="flex-1 px-3 py-1 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600 transition-colors"
            @click="viewFarm(farm.id)"
          >
            <EyeIcon class="h-4 w-4 inline mr-1" />
            View on Map
          </button>
          <button 
            class="flex-1 px-3 py-1 bg-gray-500 text-white rounded-md text-sm hover:bg-gray-600 transition-colors"
            @click="openEditForm(farm)"
          >
            <PencilIcon class="h-4 w-4 inline mr-1" />
            Edit
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-gray-500">No farms registered yet.</div>

    <!-- Add Farm Modal -->
    <div v-if="showAddForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg w-full max-w-md">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Add New Farm</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Farm Name</label>
            <input 
              v-model="newFarm.name"
              type="text"
              class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="Enter farm name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Location</label>
            <input 
              v-model="newFarm.location"
              type="text"
              class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="Enter location"
            />
          </div>
        </div>
        <div class="mt-6 flex gap-2">
          <button 
            class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            @click="addFarm"
            :disabled="isLoading"
          >
            Add Farm
          </button>
          <button 
            class="flex-1 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            @click="showAddForm = false"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Farm Modal -->
    <div v-if="showEditForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg w-full max-w-md">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Edit Farm</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Farm Name</label>
            <input 
              v-model="editFarm.name"
              type="text"
              class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="Enter farm name"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Location</label>
            <input 
              v-model="editFarm.location"
              type="text"
              class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="Enter location"
            />
          </div>
        </div>
        <div class="mt-6 flex gap-2">
          <button 
            class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            @click="editFarmData"
            :disabled="isLoading"
          >
            Save Changes
          </button>
          <button 
            class="flex-1 px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
            @click="showEditForm = false"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Responsive grid adjustments */
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>