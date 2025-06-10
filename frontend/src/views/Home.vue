<template>
  <div class="min-h-screen bg-white">
    <Navigation />
    <HeroCarousel />
    <ModulesGrid />
    <TestimonialsSection />
    <ContactSection />
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navigation from '@/components/Navigation.vue'
import HeroCarousel from '@/components/HeroCarousel.vue'
import ModulesGrid from '@/components/ModulesGrid.vue'
import TestimonialsSection from '@/components/TestimonialsSection.vue'
import ContactSection from '@/components/ContactSection.vue'
import Footer from '@/components/Footer.vue'
</script>
