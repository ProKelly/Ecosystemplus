<template>
  <!-- Toggle button -->
  <button @click="open = !open" class="fixed z-50 top-4 left-4 md:left-6 bg-gradient-to-r from-lime-500 to-emerald-600 text-white p-2 rounded-full shadow-lg focus:outline-none active:scale-95 transition-transform">
    <svg v-if="!open" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
  </button>

  <!-- Drawer -->
  <transition name="drawer">
    <aside v-if="open" class="fixed z-40 top-0 left-0 h-full w-72 bg-white/70 backdrop-blur-xl shadow-2xl p-6 overflow-y-auto flex flex-col">
      <h2 class="flex items-center gap-2 text-2xl font-bold text-green-800 mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-3.314 0-6 1.79-6 4s2.686 4 6 4 6-1.79 6-4-2.686-4-6-4z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c-3.314 0-6 1.79-6 4" /></svg>
        Farmer&nbsp;Tips
      </h2>

      <div v-for="(list, key) in tips" :key="key" class="mb-4">
        <!-- Category header -->
        <button @click="toggle(key)" class="w-full flex items-center justify-between text-green-700 font-medium capitalize py-2 hover:bg-white/60 rounded px-2 transition">
          <span class="flex items-center gap-2">
            <svg v-if="icons[key]" class="h-5 w-5 text-green-600" v-html="icons[key]"></svg>
            {{ key }}
          </span>
          <svg :class="['h-4 w-4 transition-transform', openSections.has(key) ? 'rotate-90' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
        <transition name="tip">
          <ul v-if="openSections.has(key)" class="pl-6 mt-1 space-y-1 text-sm text-gray-800">
            <li v-for="(tip,index) in list" :key="index" class="hover:pl-1 hover:text-green-900 transition">{{ tip }}</li>
          </ul>
        </transition>
      </div>
      <p class="mt-auto text-xs text-gray-600">&copy; 2024 EcoSystem+</p>
    </aside>
  </transition>
</template>

<script setup>
import { ref } from 'vue';

const open = ref(false);
const openSections = ref(new Set());

// Minimal handy tips for farmers (could come from API in future)
const tips = {
  fertilizer: [
    'Use compost or animal manure where possible',
    'Apply fertiliser at the start of rains for better absorption',
  ],
  livestock: [
    'Rotate grazing fields to avoid over-grazing',
    'Provide clean water to improve feed efficiency',
  ],
  fuel: [
    'Service tractors regularly to save fuel',
    'Consider solar pumps for irrigation',
  ],
};

// Simple inline SVG icons (for quick reference)
const icons = {
  fertilizer: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7l8 8 8-8" /></svg>`,
  livestock: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>`,
  fuel: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m2-4h.01M17 16h1a2 2 0 002-2v-5a2 2 0 00-2-2h-1.5" /></svg>`,
};

function toggle(key){
  const s=openSections.value;
  if(s.has(key)) s.delete(key); else s.add(key);
  // force reactivity
  openSections.value=new Set([...s]);
}
</script>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.4s ease-out;
}
.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.tip-enter-active,.tip-leave-active{transition:all .3s ease;}
.tip-enter-from,.tip-leave-to{opacity:0;transform:translateY(-4px);}
</style> 