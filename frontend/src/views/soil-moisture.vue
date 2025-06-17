<script setup>
import SoilMoistureDescription from '@/components/soil-moisture/soil-moisture-description.vue'
import SectionDivider from '@/components/ui/section-divider.vue'
import SoilMoistureGraphs from '@/components/soil-moisture/soil-moisture-graphs.vue'
import SoilMoistureRecommendation from '@/components/soil-moisture/soil-moisture-recommendation.vue'
</script>
<template>
  <div class="p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 pt-20">
    <!-- Section A, description -->
    <SoilMoistureDescription />
    <SectionDivider />
    <SoilMoistureGraphs />
    <SectionDivider />
    <SoilMoistureRecommendation />
    <SectionDivider />
  </div>
</template>
