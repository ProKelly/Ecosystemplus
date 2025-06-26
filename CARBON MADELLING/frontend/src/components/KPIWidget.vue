<template>
  <div :class="['glass p-4 rounded-xl text-center shadow', highlight?'bg-green-50':'' ]">
    <p class="text-sm text-green-900 mb-1">{{ label }}</p>
    <p class="text-2xl font-bold text-green-700">{{ display }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({ label: String, value: Number, highlight: Boolean });

const display = ref('0 kg');

function fmt(val) {
  if (val >= 1000) {
    return (val / 1000).toFixed(2) + ' t';
  }
  return val.toFixed(2) + ' kg';
}

watch(
  () => props.value,
  (nv) => {
    const duration = 800; // ms
    const fps = 60;
    const totalSteps = Math.round((duration / 1000) * fps);
    let step = 0;
    const start = 0;
    const timer = setInterval(() => {
      step++;
      const curr = start + ((nv - start) * step) / totalSteps;
      display.value = fmt(curr);
      if (step >= totalSteps) {
        display.value = fmt(nv);
        clearInterval(timer);
      }
    }, 1000 / fps);
  },
  { immediate: true }
);
</script>

<style scoped>
</style> 