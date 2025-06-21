<script setup lang="ts">
import { ref, computed } from 'vue'
const emit = defineEmits(['close'])

// Tutorial steps
interface TutorialStep {
  title: string
  description: string
  tip?: string
}

const steps: TutorialStep[] = [
  {
    title: 'Welcome to Field Boundary Detection',
    description: 'This tutorial will guide you through the key features of the application. You can navigate, draw boundaries, and analyze fields with ease.',
    tip: 'Click "Next" to continue or "Skip" to exit the tutorial.'
  },
  {
    title: 'Map Navigation',
    description: 'Use the map to view and interact with your fields. Zoom in/out with the mouse wheel or pinch gestures, and pan by clicking and dragging.',
    tip: 'Try switching between 2D and 3D views using the toolbar button.'
  },
  {
    title: 'Drawing Boundaries',
    description: 'In the "Detect" tab, use the Manual Draw tool to create field boundaries by clicking points on the map to form a polygon.',
    tip: 'Ensure polygons don’t intersect for accurate area calculations.'
  },
  {
    title: 'Auto-Detection',
    description: 'Click the "Auto-Detect" button to let the system analyze satellite imagery and detect field boundaries automatically.',
    tip: 'Adjust the sensitivity slider to fine-tune detection accuracy.'
  },
  {
    title: 'Editing Fields',
    description: 'Switch to the "Edit" tab to modify existing boundaries. You can split, merge, or adjust vertices of detected fields.',
    tip: 'Use the edit controls to refine boundaries for precision.'
  },
  {
    title: 'Analyzing Results',
    description: 'The "Analyze" tab shows accuracy scores and highlights problem areas. Compare with historical data to track changes.',
    tip: 'Check the Detection History panel for past results.'
  },
  {
    title: 'Collaboration',
    description: 'Invite collaborators to work on field boundaries together in real-time using the "Collaborate" button.',
    tip: 'Active collaborators are shown in the map toolbar.'
  },
  {
    title: 'Data Management',
    description: 'Import or export field data in formats like GeoJSON, Shapefile, or KML using the Data Management controls.',
    tip: 'Always save your work before exporting.'
  }
]

// State for current step
const currentStep = ref(0)

// Navigation methods
const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const skipTutorial = () => {
  emit('close')
}

// Progress percentage
const progress = computed(() => {
  return ((currentStep.value + 1) / steps.length) * 100
})
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-30">
    <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium text-gray-900">{{ steps[currentStep].title }}</h3>
        <button 
          @click="skipTutorial"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="mb-6">
        <p class="text-sm text-gray-700">{{ steps[currentStep].description }}</p>
        <p v-if="steps[currentStep].tip" class="mt-2 text-xs text-gray-500 italic">
          Tip: {{ steps[currentStep].tip }}
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-6">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="bg-emerald-600 h-2 rounded-full transition-all duration-300 ease-in-out"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <p class="text-xs text-gray-500 mt-2 text-center">
          Step {{ currentStep + 1 }} of {{ steps.length }}
        </p>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between">
        <button
          v-if="currentStep > 0"
          @click="prevStep"
          class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
        >
          Previous
        </button>
        <div v-else class="flex-1"></div>
        <div class="flex space-x-2">
          <button
            @click="skipTutorial"
            class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
          >
            Skip
          </button>
          <button
            v-if="currentStep < steps.length - 1"
            @click="nextStep"
            class="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700"
          >
            Next
          </button>
          <button
            v-else
            @click="skipTutorial"
            class="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700"
          >
            Finish
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transition for progress bar */
.transition-all {
  transition-property: width;
}

/* Subtle animation for modal appearance */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.bg-white {
  animation: fadeIn 0.3s ease-out;
}
</style>