<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import type { ChartConfiguration, ChartType } from 'chart.js'

Chart.register(...registerables)

const props = defineProps<{
  data: number[]
  label: string
  type: ChartType
}>()

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const getChartConfig = (): ChartConfiguration => {
  const colors = {
    temperature: '#ef4444',
    humidity: '#3b82f6',
    rainfall: '#6366f1',
    evapotranspiration: '#eab308',
  }

  const units = {
    temperature: '°C',
    humidity: '%',
    rainfall: 'mm',
    evapotranspiration: 'mm',
  }

  return {
    type: props.type,
    data: {
      labels: months,
      datasets: [
        {
          label: `${props.label} (${units[props.type as keyof typeof units]})`,
          data: props.data,
          borderColor: colors[props.type as keyof typeof colors],
          backgroundColor: colors[props.type as keyof typeof colors] + '20',
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: '#e5e7eb50',
          },
        },
        x: {
          grid: {
            color: '#e5e7eb50',
          },
        },
      },
    },
  } as Chart.ChartConfiguration
}

onMounted(() => {
  if (chartCanvas.value) {
    chart = new Chart(chartCanvas.value, getChartConfig())
  }
})

watch(
  () => [props.data, props.type],
  () => {
    if (chart) {
      chart.destroy()
    }
    if (chartCanvas.value) {
      chart = new Chart(chartCanvas.value, getChartConfig())
    }
  },
  { deep: true },
)

onUnmounted(() => {
  if (chart) {
    chart.destroy()
  }
})
</script>

<template>
  <canvas ref="chartCanvas" class="w-full h-full"></canvas>
</template>
