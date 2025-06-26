<template>
  <div>
    <label class="block text-sm font-medium mb-1 text-green-900">{{ label }}</label>
    <input :type="type" v-model="model" @focus="focus=true" @blur="focus=false"
      class="w-full px-3 py-2 border rounded-lg transition transform duration-200 focus:ring-2 focus:ring-green-500"
      :class="focus ? 'scale-[1.03] shadow-lg' : ''"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
const props=defineProps({label:String,modelValue:[String,Number],type:{type:String,default:'text'}});
const emit=defineEmits(['update:modelValue']);
const focus=ref(false);
const model=computed({
  get(){return props.modelValue;},
  set(v){emit('update:modelValue',v);}
});
</script>

<style scoped></style> 