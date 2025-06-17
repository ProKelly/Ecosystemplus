<script setup>
import MonitrotingDescription from '@/components/monitoring/monitoring-description.vue'
import RealTimeMonitoring from '@/components/monitoring/real-time-monitoring.vue'
import DiseaseDetection from '@/components/monitoring/disease-detection.vue'
import SectionDivider from '@/components/ui/section-divider.vue'
</script>
<template class="w-full pt-16">
  <div class="p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 pt-20">
    <!-- Section A, description -->
    <MonitrotingDescription />

    <SectionDivider />
    <!-- Section B, real-time-monitoring -->

    <RealTimeMonitoring />
    <SectionDivider />

    <!-- Section C, disease detection -->
    <DiseaseDetection />
    <SectionDivider />
  </div>
  <section class="p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 pt-20"></section>
</template>
