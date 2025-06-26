<template>
  <header class="w-full flex items-center justify-between px-4 py-2 backdrop-blur-md bg-white/30 shadow-sm sticky top-0 z-30">
    <div class="text-sm text-green-700 font-medium">Climate Sync Active</div>
    <div class="text-xs text-gray-600">{{ time }}</div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const time = ref('');
function update() {
  time.value = new Date().toLocaleString();
}
onMounted(() => {
  update();
  setInterval(update, 60000);
});
</script>

<style scoped>
</style> 