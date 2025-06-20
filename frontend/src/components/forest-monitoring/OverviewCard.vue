<template>
  <div class="bg-white rounded-lg shadow p-4">
    <div class="flex items-center">
      <div class="p-3 rounded-full" :class="iconBgColor">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="iconColor" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path v-if="icon === 'leaf'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 12h1v3h-1v-3zm-1-6h1v5h-1V6zm7 8a9 9 0 11-18 0 9 9 0 0118 0zm-9-5a1 1 0 100-2 1 1 0 000 2z" />
          <path v-if="icon === 'water'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
          <path v-if="icon === 'sun'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          <path v-if="icon === 'fire'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
        </svg>
      </div>
      <div class="ml-4">
        <p class="text-sm font-medium text-gray-500">{{ title }}</p>
        <p class="text-2xl font-semibold text-gray-900">{{ formattedValue }} <span class="text-sm font-normal">{{ unit }}</span></p>
      </div>
    </div>
    <div class="mt-3">
      <div class="flex items-center justify-between text-sm">
        <span :class="changeColor" class="flex items-center">
          <svg v-if="hasChange" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" :class="changeDirection === 'up' ? 'text-green-500' : 'text-red-500'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="changeDirection === 'up' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
          </svg>
          {{ changeText }}
        </span>
        <span class="text-gray-500">vs previous</span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  props: {
    title: String,
    value: Number,
    previousValue: Number,
    unit: String,
    icon: {
      type: String,
      default: 'leaf',
      validator: (val) => ['leaf', 'water', 'sun', 'fire'].includes(val)
    },
    inverted: Boolean,
    goodThreshold: Number
  },
  setup(props) {
    const hasChange = computed(() => props.previousValue !== undefined && props.previousValue !== null)
    const changeValue = computed(() => {
      if (!hasChange.value) return 0
      return props.value - props.previousValue
    })
    const changePercentage = computed(() => {
      if (!hasChange.value || props.previousValue === 0) return 0
      return (changeValue.value / props.previousValue) * 100
    })
    const changeDirection = computed(() => {
      if (!hasChange.value) return 'neutral'
      const effectiveChange = props.inverted ? -changeValue.value : changeValue.value
      return effectiveChange >= 0 ? 'up' : 'down'
    })
    const changeText = computed(() => {
      if (!hasChange.value) return 'No previous data'
      
      const absValue = Math.abs(changeValue.value)
      const absPercentage = Math.abs(changePercentage.value)
      const formattedValue = absValue.toFixed(absValue < 1 ? 2 : 1)
      const formattedPercentage = absPercentage.toFixed(1)
      
      return `${formattedValue} (${formattedPercentage}%)`
    })
    const changeColor = computed(() => {
      if (!hasChange.value) return 'text-gray-500'
      return changeDirection.value === 'up' ? 
        (props.inverted ? 'text-red-600' : 'text-green-600') : 
        (props.inverted ? 'text-green-600' : 'text-red-600')
    })
    const formattedValue = computed(() => {
      return props.value.toFixed(2)
    })
    const iconColor = computed(() => {
      const effectiveValue = props.inverted ? 100 - props.value : props.value
      if (props.goodThreshold === undefined) return 'text-gray-600'
      return effectiveValue >= props.goodThreshold ? 'text-green-600' : 'text-red-600'
    })
    const iconBgColor = computed(() => {
      const effectiveValue = props.inverted ? 100 - props.value : props.value
      if (props.goodThreshold === undefined) return 'bg-gray-100'
      return effectiveValue >= props.goodThreshold ? 'bg-green-100' : 'bg-red-100'
    })

    return {
      hasChange,
      changeValue,
      changePercentage,
      changeDirection,
      changeText,
      changeColor,
      formattedValue,
      iconColor,
      iconBgColor
    }
  }
}
</script>