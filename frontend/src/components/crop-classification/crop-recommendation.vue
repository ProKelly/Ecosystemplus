<template>
  <div class="p-6 bg-white rounded shadow-md">
    <h2 class="text-2xl font-semibold mb-4 text-green-700">
      Recommended Crops for {{ soilData.soilType }} Soil
    </h2>

    <!-- Crop Checkboxes -->
    <div class="space-y-2 mb-6">
      <label
        v-for="crop in soilData.recommendedCrops"
        :key="crop.name"
        class="flex items-center space-x-2 p-2 hover:bg-green-50 rounded-md transition-colors cursor-pointer"
      >
        <input type="checkbox" :value="crop.name" v-model="selectedCrops" />
        <span class="text-gray-700">{{ crop.name }}</span>
      </label>
    </div>

    <!-- Animated Crop Calendar Tables -->
    <TransitionGroup name="calendar" tag="div" class="space-y-8">
      <div
        v-for="crop in filteredSelectedCrops"
        :key="crop.name"
        class="border-t pt-4 calendar-item"
      >
        <h3 class="text-xl font-bold mb-4 text-green-700">{{ crop.name }} Agricultural Calendar</h3>

        <div class="overflow-x-auto">
          <table class="table-auto w-full text-left border border-gray-200">
            <thead class="bg-green-100 text-sm text-gray-700">
              <tr>
                <th class="px-4 py-2 border">Land Preparation</th>
                <th class="px-4 py-2 border">Planting</th>
                <th class="px-4 py-2 border">Germination</th>
                <th class="px-4 py-2 border">Vegetative Phase</th>
                <th class="px-4 py-2 border">Flowering</th>
                <th class="px-4 py-2 border">Bearing</th>
                <th class="px-4 py-2 border">Harvesting</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-sm text-gray-800">
                <td
                  v-for="(value, key) in crop.calendar"
                  :key="key"
                  class="px-4 py-2 border calendar-cell"
                >
                  {{ value }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-3 p-3 bg-green-50 rounded-md text-sm text-gray-700 recommendation-box">
          <strong>Recommendation:</strong> {{ crop.recommendation }}
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface CropCalendar {
  landPreparation: string
  planting: string
  germination: string
  vegetative: string
  flowering: string
  bearing: string
  harvesting: string
}

interface Crop {
  name: string
  calendar: CropCalendar
  recommendation: string
}

interface SoilData {
  soilType: string
  recommendedCrops: Crop[]
}

// Mock data object
const soilData = ref<SoilData>({
  soilType: 'Loamy',
  recommendedCrops: [
    {
      name: 'Maize',
      calendar: {
        landPreparation: 'Jan - Feb',
        planting: 'Mar',
        germination: 'Mar - Apr',
        vegetative: 'Apr - May',
        flowering: 'May - Jun',
        bearing: 'Jun',
        harvesting: 'Jul',
      },
      recommendation: 'Use nitrogen-rich fertilizer during vegetative phase.',
    },
    {
      name: 'Tomato',
      calendar: {
        landPreparation: 'Feb',
        planting: 'Mar',
        germination: 'Late Mar',
        vegetative: 'Apr',
        flowering: 'May',
        bearing: 'Late May - Jun',
        harvesting: 'Jul',
      },
      recommendation: 'Stake plants early to support growth and prevent rot.',
    },
  ],
})

const selectedCrops = ref<string[]>([])

const filteredSelectedCrops = computed<Crop[]>(() => {
  return soilData.value.recommendedCrops.filter((crop) => selectedCrops.value.includes(crop.name))
})

// Add this to set dynamic animation delays for cells
onMounted(() => {
  const cells = document.querySelectorAll('.calendar-cell')
  cells.forEach((cell, index) => {
    cell.style.setProperty('--cell-index', index.toString())
  })
})
</script>

<style scoped>
input[type='checkbox'] {
  accent-color: #38a169; /* Tailwind green-600 */
}

/* Animation styles */
.calendar-enter-active,
.calendar-leave-active {
  transition: all 0.5s ease;
}

.calendar-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.calendar-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* Calendar cell animations */
.calendar-item {
  animation: slideDown 0.5s ease-out;
}

.calendar-cell {
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
  animation-delay: calc(var(--cell-index, 0) * 0.1s);
}

.recommendation-box {
  animation: fadeInScale 0.5s ease-out 0.3s forwards;
  opacity: 0;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
