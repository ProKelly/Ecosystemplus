<script setup lang="ts">
import { computed } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  score: {
    type: Number as PropType<number>,
    required: true,
    validator: (value: number) => value >= 0 && value <= 100
  }
})

// Computed properties for gauge styling
const gaugeColor = computed(() => {
  if (props.score >= 80) return 'bg-emerald-500'
  if (props.score >= 60) return 'bg-yellow-400'
  return 'bg-red-500'
})

const gaugeWidth = computed(() => `${props.score}%`)

const accuracyLabel = computed(() => {
  if (props.score >= 80) return 'High Accuracy'
  if (props.score >= 60) return 'Moderate Accuracy'
  return 'Low Accuracy'
})
</script>

<template>
  <div class="bg-white rounded-lg shadow p-4">
    <!-- Header -->
    <h3 class="text-sm font-medium text-gray-900 mb-3">Accuracy Meter</h3>

    <!-- Gauge -->
    <div class="relative w-full h-4 bg-gray-200 rounded-full overflow-hidden">
      <div
        :class="['h-full transition-all duration-500 ease-in-out', gaugeColor]"
        :style="{ width: gaugeWidth }"
      ></div>
    </div>

    <!-- Score and Label -->
    <div class="mt-2 flex justify-between items-center">
      <span class="text-sm font-medium text-gray-700">{{ score }}%</span>
      <span class="text-xs text-gray-500">{{ accuracyLabel }}</span>
    </div>

    <!-- Feedback Text -->
    <p class="mt-2 text-xs text-gray-500">
      {{ score >= 80 ? 'Excellent boundary detection. Ready for use.' : 
         score >= 60 ? 'Good detection, but review for minor adjustments.' : 
         'Low confidence. Consider manual adjustments or re-running detection.' }}
    </p>
  </div>
</template>

<style scoped>
/* Ensure smooth transitions for gauge */
.transition-all {
  transition-property: width, background-color;
}
</style>