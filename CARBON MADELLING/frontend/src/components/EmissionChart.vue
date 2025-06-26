<template>
  <div class="bg-white/40 backdrop-blur rounded-xl p-4 shadow">
    <canvas ref="canvas" class="w-full h-64"></canvas>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js';
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip);
const props=defineProps({report:Object});
const canvas=ref(null);let chart=null;
function render(){
  if(!canvas.value) return;
  if(chart) {chart.destroy();}
  chart=new Chart(canvas.value,{type:'bar',data:{labels:['Fertilizer','Livestock','Fuel'],datasets:[{data:[props.report.fertilizer_emissions,props.report.livestock_emissions,props.report.fuel_emissions],backgroundColor:['#34d399','#6ee7b7','#a7f3d0'],borderRadius:6}]},options:{responsive:true,plugins:{legend:{display:false}},animation:{duration:800,easing:'easeOutQuart'},scales:{y:{beginAtZero:true}}}});
}
 onMounted(render);
 watch(()=>props.report,render);
</script>
<style scoped></style> 