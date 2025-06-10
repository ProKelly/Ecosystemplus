<template>
  <div class="accordion-item" :class="[$attrs.class]">
    <slot />
  </div>
</template>
<script setup lang="ts">
import { defineProps } from 'vue';
defineProps<{ value?: string }>();
</script>
