<template>
  <section class="bg-gray-50 py-10 px-6 md:px-16 lg:px-24 text-gray-800 shadow-md">
    <h2 class="text-2xl md:text-3xl font-bold text-green-700 mb-6">Crop Activity Planner</h2>

    <!-- Crop Selection and Date Input -->
    <form @submit.prevent="registerCrop" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <select v-model="selectedCrop" class="p-2 rounded border">
        <option disabled value="">Select Crop</option>
        <option v-for="(data, name) in crops" :key="name" :value="name">
          {{ name }}
        </option>
      </select>
      <input type="date" v-model="plantingDate" class="p-2 rounded border" />
      <button type="submit" class="bg-green-600 text-white rounded px-4 py-2 hover:bg-green-700">
        Add Crop
      </button>
    </form>

    <!-- Registered Crops -->
    <div
      v-if="registeredCrops.length === 0"
      class="text-center py-16 text-xl text-gray-700 font-semibold"
    >
      🌱 Please remember to add the crops you have planted so you can get a schedule from planting
      to harvest.
    </div>
    <div
      v-for="(entry, index) in registeredCrops"
      :key="index"
      class="mb-12 bg-white p-6 rounded-lg shadow-md"
    >
      <!-- Header with Edit/Delete -->
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-semibold text-green-700">
          {{ entry.crop }} - Planted on {{ formatDate(entry.date) }}
        </h3>
        <div class="flex justify-between">
          <button
            style="margin-right: 4px"
            @click="editEntry(index)"
            class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 mx-2 rounded flex items-center"
          >
            <!-- <i class="fas fa-edit mr-2"></i> -->
            <font-awesome-icon icon="pen" />
          </button>
          <button
            @click="deleteEntry(index)"
            class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 ml-4 rounded flex items-center"
          >
            <!-- <i class="fas fa-trash-alt"></i> -->
            <font-awesome-icon icon="trash" />
          </button>
        </div>
      </div>

      <!-- Activity Table -->
      <h4 class="font-semibold mb-2 font-bold text-xl">Crop Activities</h4>
      <table class="w-full text-left border mb-6">
        <thead class="bg-green-100">
          <tr>
            <th class="p-2">Activity</th>
            <th class="p-2">Date/Range</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(activity, idx) in crops[entry.crop].activities" :key="idx">
            <td class="p-2 border-t">{{ activity.name }}</td>
            <td class="p-2 border-t">{{ calculateDate(entry.date, activity.offset) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Disease Table -->
      <h4 class="font-semibold mb-2 font-bold text-xl">Potential Diseases</h4>
      <table class="w-full text-left border">
        <thead class="bg-red-100">
          <tr>
            <th class="p-2">Disease</th>
            <th class="p-2">Cause</th>
            <th class="p-2">Image</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(disease, dIndex) in cropDiseases[entry.crop] || []" :key="dIndex">
            <td class="p-2 border-t">{{ disease.name }}</td>
            <td class="p-2 border-t">{{ disease.cause }}</td>
            <td class="p-2 border-t">
              <img :src="disease.image" alt="Disease" class="h-16 w-auto rounded" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const crops = {
  Maize: {
    activities: [
      { name: 'Germination', offset: 7 },
      { name: 'Weeding', offset: 21 },
      { name: 'Fertilizing', offset: 30 },
      { name: 'Harvesting', offset: 90 },
    ],
  },
  Cassava: {
    activities: [
      { name: 'Sprouting', offset: 14 },
      { name: 'Weeding', offset: 30 },
      { name: 'Mulching', offset: 45 },
      { name: 'Harvesting', offset: 240 },
    ],
  },
  Tomato: {
    activities: [
      { name: 'Germination', offset: 5 },
      { name: 'Staking', offset: 25 },
      { name: 'Spraying', offset: 35 },
      { name: 'Harvesting', offset: 75 },
    ],
  },
}

const cropDiseases = {
  Maize: [
    {
      name: 'Maize Streak Virus',
      cause: 'Transmitted by leafhoppers',
      solution: 'Plant resistant varieties and control vectors',
      image: 'https://upload.wikimedia.org/wikipedia/commons/9/91/Maize_streak_virus_symptoms.jpg',
    },
    {
      name: 'Northern Leaf Blight',
      cause: 'Fungal spores in humid conditions',
      solution: 'Apply fungicides and ensure crop rotation',
      image:
        'https://www.agric.wa.gov.au/sites/gateway/files/styles/original/public/Northern%20leaf%20blight%20on%20maize%20.jpg',
    },
  ],
  Cassava: [
    {
      name: 'Cassava Mosaic Disease',
      cause: 'Spread by whiteflies',
      solution: 'Use virus-free cuttings and control whiteflies',
      image: 'https://www.rtb.cgiar.org/wp-content/uploads/sites/2/2016/01/1-2-3-Mosaic.jpg',
    },
  ],
  Tomato: [
    {
      name: 'Early Blight',
      cause: 'Caused by Alternaria fungus',
      solution: 'Apply fungicides and practice crop rotation',
      image: 'https://cdn.britannica.com/20/206920-050-7B09D0D2/Early-blight-tomato-leaves.jpg',
    },
  ],
}

const selectedCrop = ref('')
const plantingDate = ref('')
const registeredCrops = ref([])

function registerCrop() {
  if (selectedCrop.value && plantingDate.value) {
    registeredCrops.value.push({ crop: selectedCrop.value, date: plantingDate.value })
    selectedCrop.value = ''
    plantingDate.value = ''
  }
}

function deleteEntry(index) {
  registeredCrops.value.splice(index, 1)
}

function editEntry(index) {
  const item = registeredCrops.value[index]
  selectedCrop.value = item.crop
  plantingDate.value = item.date
  deleteEntry(index)
}

function calculateDate(startDate, offsetDays) {
  const date = new Date(startDate)
  date.setDate(date.getDate() + offsetDays)
  return date.toDateString()
}

function formatDate(date) {
  return new Date(date).toDateString()
}
</script>

<style scoped>
/* Custom styling if needed */
</style>
