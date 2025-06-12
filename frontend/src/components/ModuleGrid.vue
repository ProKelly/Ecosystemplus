<script setup lang="ts">
import { ArrowRightIcon } from '@heroicons/vue/24/outline'

const modules = [
{
    id: 1,
    title: "Yield Prediction",
    description: "Accurate yield forecasts using machine learning models",
    image: "bg-[url('@/assets/images/yield-grid.jpg')]",
    path: "/yield-prediction"
  },
  {
    id: 2,
    title: "Crop Classification",
    description: "AI-powered identification of crop types and varieties",
    image: "bg-[url('@/assets/images/crop-classification.webp')]",
    path: "/classification"
  },
{
    id: 3,
    title: "Field Boundary",
    description: "Precision mapping and digital twinning of agricultural fields",
    image: "bg-[url('@/assets/images/field-detection.webp')]",
    path: "/field-detection"
  },
   {
    id: 4,
    title: "Soil Analysis",
    description: "Advanced soil moisture and nutrient level mapping",
    image: "bg-[url('@/assets/images/soil-analysis.jpg')]",
    path: "/soil-analysis"
  },
  {
    id: 5,
    title: "Crop Monitoring",
    description: "Real-time vegetation health and growth stage tracking",
    image: "bg-[url('@/assets/images/crop-monitoring.jpg')]",
    path: "/monitoring"
  },
  {
    id: 6,
    title: "Carbon Modeling",
    description: "Measure and optimize your carbon footprint",
    image: "bg-[url('@/assets/images/carbon-grid.jpeg')]",
    path: "/carbon-model"
  },
  {
    id: 7,
    title: "Forest Monitoring",
    description: "Track tree health and deforestation risks",
    image: "bg-[url('@/assets/images/forest-grid.jpeg')]",
    path: "/forest-monitoring"
  },
  {
    id: 8,
    title: "Personalized Recommendations",
    description: "AI-driven insights tailored to your operation",
    image: "bg-[url('@/assets/images/personalized-recommendation.jpeg')]",
    path: "/recommendations"
  }
]
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
    <RouterLink
      v-for="module in modules"
      :key="module.id"
      :to="module.path"
      class="group relative h-72 rounded-3xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-emerald-300"
    >
      <!-- Background Image with Overlay -->
      <div 
        class="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105"
        :class="module.image"
      >
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent group-hover:from-emerald-900/60 transition-colors duration-300"></div>
      </div>
      
      <!-- Content -->
      <div class="relative h-full flex flex-col justify-end p-7 text-white z-10">
        <div class="transform transition-all duration-500 group-hover:-translate-y-3">
          <h3 class="text-2xl md:text-3xl font-extrabold mb-2 tracking-tight drop-shadow-lg">
            {{ module.title }}
          </h3>
          <p class="text-base md:text-lg opacity-90 mb-5 font-medium drop-shadow">
            {{ module.description }}
          </p>
          <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <span class="text-sm font-semibold tracking-wide uppercase">Explore</span>
            <ArrowRightIcon class="h-5 w-5 text-emerald-300 group-hover:text-white transition-colors duration-200" />
          </div>
        </div>
      </div>
      
      <!-- Hover Effect Border -->
      <div class="absolute inset-0 border-2 border-transparent group-hover:border-emerald-400/70 rounded-3xl transition-all duration-300 pointer-events-none"></div>
    </RouterLink>
  </div>
</template>