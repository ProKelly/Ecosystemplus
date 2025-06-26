<template>
  <div class="relative w-full h-72 bg-gradient-to-br from-green-100 to-green-50 rounded-xl overflow-hidden shadow">
    <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
      <rect width="400" height="200" fill="url(#g)" />
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#d1fae5" />
          <stop offset="100%" stop-color="#f0fdf4" />
        </linearGradient>
      </defs>
    </svg>
    <div v-for="pt in points" :key="pt.id" class="absolute">
      <div :style="style(pt)" class="animate-ping rounded-full bg-emerald-500 opacity-60"></div>
      <div :style="style(pt)" class="rounded-full bg-emerald-600 w-2 h-2"></div>
    </div>
  </div>
</template>
<script setup>
const props=defineProps({points:{type:Array,default:()=>[{x:120,y:60},{x:300,y:140},{x:200,y:100}]} });
function style(pt){return`left:${pt.x}px;top:${pt.y}px;width:6px;height:6px;`} 
</script>
<style scoped></style> 