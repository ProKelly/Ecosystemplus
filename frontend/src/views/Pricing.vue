<template>
  <div class="min-h-screen bg-white">
    <Navigation />
    <div class="pt-24">
      <PricingSection />
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navigation from '../components/Navigation.vue';
import PricingSection from '../components/PricingSection.vue';
import Footer from '../components/Footer.vue';
</script>
