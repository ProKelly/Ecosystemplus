<template>
  <div class="w-full h-full">
    <div class="flex justify-between items-center mb-2">
      <h4 class="text-sm font-medium text-black">{{ title }}</h4>
      <div class="flex items-center text-xs space-x-3">
        <span class="flex items-center">
          <span class="w-3 h-3 rounded-full mr-1" :style="`background-color: ${color}`"></span>
          Current: {{ currentValue.toFixed(2) }}
        </span>
        <span v-if="previousValue !== undefined" class="flex items-center">
          <span class="w-3 h-3 rounded-full mr-1 bg-gray-400"></span>
          Previous: {{ previousValue.toFixed(2) }}
        </span>
      </div>
    </div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  props: {
    title: String,
    data: Array,
    currentValue: Number,
    previousValue: Number,
    color: {
      type: String,
      default: '#10b981'
    },
    inverted: Boolean
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null

    const createChart = () => {
      if (chartInstance) {
        chartInstance.destroy()
      }

      if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d')
        
        // Adjust values if inverted (for metrics where lower is better)
        const adjustedData = props.inverted 
          ? props.data.map(item => ({ ...item, y: 100 - item.y }))
          : props.data
        
        chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: adjustedData.map(item => {
              const date = new Date(item.x)
              return date.toLocaleDateString('default', { month: 'short' })
            }),
            datasets: [{
              label: props.title,
              data: adjustedData.map(item => item.y),
              borderColor: props.color,
              backgroundColor: `${props.color}20`,
              borderWidth: 2,
              tension: 0.3,
              fill: true,
              pointRadius: 0
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    const value = props.inverted ? 100 - context.raw : context.raw
                    return `${props.title}: ${value.toFixed(2)}`
                  }
                }
              }
            },
            scales: {
              x: { grid: { display: false } },
              y: { 
                grid: { color: '#e5e7eb' },
                beginAtZero: props.inverted ? false : true
              }
            }
          }
        })
      }
    }

    onMounted(createChart)
    watch(() => props.data, createChart, { deep: true })

    return {
      chartCanvas
    }
  }
}
</script>