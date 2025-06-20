<script setup lang="ts">
import { ref, onMounted } from 'vue'

const impacts = [
  {
    id: 1,
    module: "Field Boundary Detection",
    impact: "Enabled 100+ farmers to digitally map their fields, reducing manual errors by 95% and saving 20+ hours per season.",
    profitability: "Saves FCFA 5,000-10,000 per acre annually in labor costs",
    image: "@/assets/images/field-detection.webp"
  },
  {
    id: 2,
    module: "Crop Classification",
    impact: "Automated crop type identification across 10,000+ acres, improving planning and resource allocation.",
    profitability: "Reduces input costs by 15-20% through optimized planting",
    image: "@/assets/images/crop-classification.webp"
  },
  {
    id: 3,
    module: "Crop Monitoring",
    impact: "Real-time alerts helped prevent yield loss on 500+ fields, increasing average ROI by 10x.",
    profitability: "Prevents 10-15% yield loss from pests/diseases",
    image: "@/assets/images/crop-monitoring.jpg"
  },
  {
    id: 4,
    module: "Soil Moisture Analysis",
    impact: "Optimized irrigation schedules, saving up to 30% water usage for participating farms.",
    profitability: "Saves FCFA 3,000-5,000 per acre in water/pumping costs",
    image: "@/assets/images/soil-analysis.jpg"
  },
  {
    id: 5,
    module: "Yield Prediction",
    impact: "Delivered 92% accurate yield forecasts, empowering better market and logistics decisions.",
    profitability: "Increases sales prices by 8-12% through better timing",
    image: "@/assets/images/yield-grid.jpg"
  },
  {
    id: 6,
    module: "Personalized Recommendations",
    impact: "AI-driven insights led to a 22% productivity boost in the first season for early adopters.",
    profitability: "Boosts profits by FCFA 15,000-25,000 per acre annually",
    image: "@/assets/images/personalized-recommendation.jpeg"
  }
]

const current = ref(0)
const interval = ref<any>()

const next = () => {
  current.value = (current.value + 1) % impacts.length
  resetInterval()
}
const prev = () => {
  current.value = (current.value - 1 + impacts.length) % impacts.length
  resetInterval()
}
const goTo = (i: number) => {
  current.value = i
  resetInterval()
}
const resetInterval = () => {
  clearInterval(interval.value)
  startInterval()
}
const startInterval = () => {
  interval.value = setInterval(() => {
    next()
  }, 8000) // Increased interval for better readability
}
onMounted(() => {
  startInterval()
  return () => clearInterval(interval.value)
})

function getImageUrl(path: string) {
  return new URL(path, import.meta.url).href;
}
</script>

<template>
  <div class="relative w-full overflow-hidden rounded-2xl shadow-xl h-[400px] md:h-[480px] bg-gradient-to-br from-white to-emerald-50 border border-emerald-100">
    <!-- Slide indicators at top -->
    <div class="absolute top-4 left-1/2 -translate-x-1/2 flex space-x-2 z-10">
      <button 
        v-for="(item, idx) in impacts" 
        :key="item.id" 
        @click="goTo(idx)" 
        class="h-2 w-6 rounded-full transition-all duration-300 hover:bg-emerald-300" 
        :class="current === idx ? 'bg-emerald-600 w-8' : 'bg-emerald-200'" 
        aria-label="Go to slide" 
      />
    </div>
    
    <!-- Slides container -->
    <div class="flex h-full transition-transform duration-700 ease-in-out" :style="{ transform: `translateX(-${current * 100}%)` }">
      <div 
        v-for="(item, idx) in impacts" 
        :key="item.id" 
        class="relative flex-shrink-0 w-full h-full flex flex-col md:flex-row items-center justify-center p-8 md:p-12 gap-8"
      >
        <!-- Image with decorative border -->
        <div class="relative">
          <div class="absolute -inset-2 bg-emerald-100 rounded-xl transform rotate-1"></div>
          <img 
            :src="getImageUrl(item.image)" 
            :alt="item.module" 
            class="relative w-40 h-40 md:w-56 md:h-56 object-cover rounded-xl shadow-lg z-10 border-4 border-white" 
          />
        </div>
        
        <!-- Content with better typography -->
        <div class="flex-1 text-center md:text-left max-w-2xl">
          <span class="inline-block px-3 py-1 mb-3 text-xs font-semibold tracking-wider text-emerald-700 uppercase bg-emerald-100 rounded-full">
            Module {{ idx + 1 }}
          </span>
          <h3 class="text-2xl md:text-3xl font-bold text-gray-800 mb-3 leading-tight">
            {{ item.module }}
          </h3>
          <p class="text-lg md:text-xl text-gray-600 mb-4 leading-relaxed">
            {{ item.impact }}
          </p>
          <div class="inline-flex items-center px-4 py-2 bg-emerald-50 rounded-lg border border-emerald-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
            </svg>
            <span class="font-medium text-emerald-700">{{ item.profitability }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Navigation buttons -->
    <!-- <button 
      @click="prev" 
      class="absolute left-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-white hover:bg-emerald-50 transition-all shadow-lg border border-gray-100 hover:border-emerald-200 z-10" 
      aria-label="Previous"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <button 
      @click="next" 
      class="absolute right-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-white hover:bg-emerald-50 transition-all shadow-lg border border-gray-100 hover:border-emerald-200 z-10" 
      aria-label="Next"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button> -->
  </div>
</template>