<template>
  <div class="flex items-start p-3 rounded-lg border" :class="severityClasses">
    <div class="flex-shrink-0 mt-0.5">
      <div class="h-3 w-3 rounded-full" :class="severityDotColor"></div>
    </div>
    <div class="ml-3">
      <p class="text-sm font-medium text-black">{{ description }}</p>
      <p class="text-xs text-black/80 mt-1">
        <span v-if="type === 'vegetation'" class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 12h1v3h-1v-3zm-1-6h1v5h-1V6zm7 8a9 9 0 11-18 0 9 9 0 0118 0zm-9-5a1 1 0 100-2 1 1 0 000 2z" />
          </svg>
          Vegetation {{ value > 0 ? 'increase' : 'decrease' }}: {{ Math.abs(value).toFixed(2) }}
        </span>
        <span v-else-if="type === 'moisture'" class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
          </svg>
          Moisture {{ value > 0 ? 'increase' : 'decrease' }}: {{ Math.abs(value).toFixed(2) }}
        </span>
        <span v-else-if="type === 'fire'" class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
          </svg>
          Fire risk {{ value > 0 ? 'increase' : 'decrease' }}: {{ Math.abs(value) }} points
        </span>
      </p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  props: {
    type: {
      type: String,
      required: true,
      validator: (val) => ['vegetation', 'moisture', 'fire'].includes(val)
    },
    value: {
      type: Number,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    severity: {
      type: String,
      default: 'medium',
      validator: (val) => ['low', 'medium', 'high'].includes(val)
    }
  },
  setup(props) {
    const severityClasses = computed(() => {
      return {
        'low': 'border-blue-200 bg-blue-50',
        'medium': 'border-yellow-200 bg-yellow-50',
        'high': 'border-red-200 bg-red-50'
      }[props.severity]
    })
    
    const severityDotColor = computed(() => {
      return {
        'low': 'bg-blue-500',
        'medium': 'bg-yellow-500',
        'high': 'bg-red-500'
      }[props.severity]
    })

    return {
      severityClasses,
      severityDotColor
    }
  }
}
</script>