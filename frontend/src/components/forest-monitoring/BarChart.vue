<template>
  <div class="w-full h-full">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  props: {
    data: Array
  },
  setup(props) {
    const chart = ref(null)
    let chartInstance = null

    const renderChart = () => {
      if (chartInstance) chartInstance.destroy()
      if (!chart.value) return

      const ctx = chart.value.getContext('2d')
      
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: props.data[0].values.map((_, i) => `Year ${i+1}`),
          datasets: props.data.map(dataset => ({
            label: dataset.name,
            data: dataset.values.map(v => v.y),
            backgroundColor: dataset.color,
            borderColor: dataset.color,
            borderWidth: 1
          }))
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom' } },
          scales: { y: { beginAtZero: true } }
        }
      })
    }

    onMounted(renderChart)
    watch(() => props.data, renderChart, { deep: true })

    return { chart }
  }
}
</script>