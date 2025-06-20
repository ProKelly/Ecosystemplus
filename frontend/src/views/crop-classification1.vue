<script setup>
import LocationSelector from '@/components/crop-classification/location-selector.vue'
import SectionDivider from '@/components/ui/section-divider.vue'
import SoilWeatherAnalysis from '@/components/crop-classification/soil-weather-analysis.vue'
import CropRecommendation from '@/components/crop-classification/crop-recommendation.vue'
</script>
<template>
  <div class="p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 pt-20">
    <LocationSelector />
    <SectionDivider />

    <SoilWeatherAnalysis />
    <SectionDivider />
    <CropRecommendation />
  </div>
</template>
