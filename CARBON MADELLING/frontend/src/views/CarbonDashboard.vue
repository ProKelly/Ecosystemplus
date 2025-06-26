<template>
  <div class="w-full max-w-5xl space-y-8">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <KPIWidget label="Fertilizer" :value="report.fertilizer_emissions" />
      <KPIWidget label="Livestock" :value="report.livestock_emissions" />
      <KPIWidget label="Fuel" :value="report.fuel_emissions" />
      <KPIWidget label="Total" :value="report.total_emissions" highlight />
    </div>
    <EmissionChart :report="report" />
    <MapWidget class="mt-6" />
    <div class="flex justify-center gap-4">
      <button @click="$emit('back')" class="px-6 py-2 rounded-full bg-green-600 text-white shadow hover:bg-green-700 transition">Back</button>
      <button @click="downloadJSON" class="px-6 py-2 rounded-full bg-emerald-500 text-white shadow hover:bg-emerald-600 transition">Download JSON</button>
    </div>
  </div>
</template>

<script setup>
import KPIWidget from '../components/KPIWidget.vue';
import EmissionChart from '../components/EmissionChart.vue';
import MapWidget from '../components/MapWidget.vue';
const props=defineProps({report:Object});
function downloadJSON(){
  const blob=new Blob([JSON.stringify(props.report,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download='carbon_report.json';a.click();URL.revokeObjectURL(url);
}
</script>

<style scoped></style> 