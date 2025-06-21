<<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  history: {
    type: Array as PropType<Field[]>,
    required: true,
    default: () => []
  },
  progress: {
    type: Number,
    required: true
  },
  estimatedTime: {
    type: String,
    required: true
  }
})

// Computed property for progress bar width
const progressWidth = computed(() => `${Math.min(Math.max(props.progress, 0), 100)}%`)

// Computed property for progress text
const progressText = computed(() => {
  if (props.progress < 10) return 'Initializing detection...'
  if (props.progress < 30) return 'Analyzing satellite imagery...'
  if (props.progress < 60) return 'Processing field boundaries...'
  if (props.progress < 90) return 'Validating results...'
  return 'Finalizing detection...'
})
</script>

<template>
  <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20">
    <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium text-gray-900">Processing Field Detection</h3>
        <svg class="animate-spin h-5 w-5 text-emerald-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div 
            class="bg-emerald-600 h-2.5 rounded-full transition-all duration-300 ease-in-out"
            :style="{ width: progressWidth }"
          ></div>
        </div>
      </div>

      <!-- Status and Estimated Time -->
      <div class="text-center">
        <p class="text-sm font-medium text-gray-700 mb-2">{{ progressText }}</p>
        <p class="text-sm text-gray-500">
          Estimated time remaining: <span class="font-medium">{{ estimatedTime }}</span>
        </p>
      </div>

      <!-- Additional Information -->
      <div class="mt-4 pt-4 border-t border-gray-200">
        <p class="text-xs text-gray-500 text-center">
          Processing may take a few moments. Please don't close this window.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Ensure the progress bar transition is smooth */
.transition-all {
  transition-property: width;
}

/* Optional: Add a subtle pulse animation to the processing container */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

.bg-white {
  animation: pulse 2s ease-in-out infinite;
}
</style>>