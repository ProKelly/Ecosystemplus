<template>
  <div>
    <label class="block text-sm font-medium mb-1 text-green-900 flex items-center gap-1">
      {{ label }}
      <span v-if="help" class="relative group cursor-pointer text-green-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 18h.01"/></svg>
        <span class="absolute left-1/2 -translate-x-1/2 top-6 w-max max-w-xs bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition pointer-events-none z-10 whitespace-pre-line">{{ help }}</span>
      </span>
    </label>
    <div class="relative">
      <select
        v-model="model"
        @focus="open = true"
        @blur="open = false"
        class="w-full appearance-none bg-white/70 backdrop-blur border border-green-300 rounded-lg px-3 py-2 pr-10 text-sm text-green-900 shadow transition duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 hover:bg-white/90 hover:shadow-lg"
        :class="open ? 'shadow-lg scale-[1.03]' : ''"
      >
        <option disabled value="">Select…</option>
        <option v-for="o in options" :key="o.value" :value="o.value" class="text-gray-800">{{ o.label }}</option>
      </select>
      <!-- custom arrow icon -->
      <svg class="pointer-events-none absolute top-1/2 right-3 h-4 w-4 text-green-700 -translate-y-1/2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
const props=defineProps({label:String,modelValue:String,options:Array,help:String});
const emit=defineEmits(['update:modelValue']);
const open=ref(false);
const model=computed({
  get(){return props.modelValue;},
  set(v){emit('update:modelValue',v);}
});
</script>

<style scoped></style> 