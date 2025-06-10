<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Navigation from '@/components/Navigation.vue'
import { MODULES } from '@/constants/modules'
</script>

<template>
  <!-- Main app content rendered by route -->
  <RouterView />
</template>

<style scoped>

</style>
