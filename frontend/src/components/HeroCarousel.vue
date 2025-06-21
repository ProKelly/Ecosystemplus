<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'

const slides = [
  {
    id: 1,
    title: "Field Boundary Detection",
    description: "Precision agriculture starts with accurate field mapping. Our AI-powered boundary detection creates digital twins of your fields with centimeter-level accuracy.",
    bgImage: "bg-[url('@/assets/images/field-detection.webp')]",
    cta: "Map Your Fields",
    route: "/field-detection"
  },
  {
    id: 2,
    title: "Crop Classification",
    description: "Automatically identify and classify crop types across your entire operation with our advanced computer vision models trained on millions of acres.",
    bgImage: "bg-[url('@/assets/images/crop-classification.webp')]",
    cta: "Classify Crops",
    route: "/classification"
  },
  {
    id: 3,
    title: "Advanced Crop Monitoring",
    description: "Real-time vegetation indices and growth stage tracking with satellite and drone imagery, alerting you to potential issues before they impact yield.",
    bgImage: "bg-[url('@/assets/images/crop-monitoring.jpg')]",
    cta: "Monitor Fields",
    route: "/monitoring"
  },
  {
    id: 4,
    title: "Soil Moisture Analysis",
    description: "Hyper-local soil moisture mapping combining satellite data, weather patterns, and ground sensors for optimal irrigation planning.",
    bgImage: "bg-[url('@/assets/images/soil-analysis.jpg')]",
    cta: "Analyze Soil",
    route: "/soil-moisture"
  },
  {
    id: 5,
    title: "Yield Prediction",
    description: "Accurate yield forecasts using machine learning models",
    bgImage: "bg-[url('@/assets/images/yield-grid.jpg')]",
    cta: "Predict Yield",
    route: "/monitoring" // fallback or create a new route if needed
  },
  {
    id: 6,
    title: "Carbon Modeling",
    description: "Measure and optimize your carbon footprint",
    bgImage: "bg-[url('@/assets/images/carbon-grid-2.jpeg')]",
    cta: "Model Carbon",
    route: "/monitoring" // fallback or create a new route if needed
  },
  {
    id: 7,
    title: "Forest Monitoring",
    description: "Track tree health and deforestation risks",
    bgImage: "bg-[url('@/assets/images/forest-grid.jpeg')]",
    cta: "Monitor Forest",
    route: "/forest-monitoring"
  },
  {
    id: 8,
    title: "Personalized Recommendations",
    description: "AI-driven insights tailored to your operation",
    bgImage: "bg-[url('@/assets/images/personalized-recommendation.jpeg')]",
    cta: "Get Recommendations",
    route: "/personalized-recommendations"
  }
]

const currentSlide = ref(0)
const interval = ref<any>()

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % slides.length
  resetInterval()
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + slides.length) % slides.length
  resetInterval()
}

const goToSlide = (index: number) => {
  currentSlide.value = index
  resetInterval()
}

const resetInterval = () => {
  clearInterval(interval.value)
  startInterval()
}

const startInterval = () => {
  interval.value = setInterval(() => {
    nextSlide()
  }, 7000)
}

onMounted(() => {
  startInterval()
  return () => clearInterval(interval.value)
})
</script>

<template>
  <div class="relative w-full overflow-hidden rounded-2xl shadow-xl h-[400px] sm:h-[500px] md:h-[600px]">
    <!-- Slides -->
    <div 
      class="flex h-full transition-transform duration-1000 ease-in-out"
      :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
    >
      <div 
        v-for="(slide, index) in slides"
        :key="slide.id"
        class="relative flex-shrink-0 w-full h-full"
      >
        <!-- Background Image with Overlay -->
        <div 
          class="absolute inset-0 bg-cover bg-center transition-opacity duration-1000"
          :class="[slide.bgImage, currentSlide === index ? 'opacity-100' : 'opacity-0']"
        >
          <div class="absolute inset-0 bg-black/40 backdrop-blur-[1px]"></div>
        </div>
        <!-- Content -->
        <div class="relative h-full flex flex-col justify-center items-center px-4 sm:px-8 text-white">
          <div 
            class="w-full max-w-xl space-y-4 sm:space-y-6 transform transition-all duration-1000 text-center"
            :class="currentSlide === index ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
          >
            <h2 class="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-bold leading-tight">
              {{ slide.title }}
            </h2>
            <p class="text-base xs:text-lg sm:text-xl md:text-2xl leading-relaxed">
              {{ slide.description }}
            </p>
            <router-link
              :to="slide.route"
              class="w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 bg-white/20 backdrop-blur-md rounded-full border border-white/30 hover:bg-emerald-600/80 hover:border-emerald-600 transition-all duration-300 font-medium inline-block"
            >
              {{ slide.cta }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <!-- Controls -->
    <button 
      @click="prevSlide"
      class="absolute left-2 sm:left-6 top-1/2 -translate-y-1/2 p-2 sm:p-3 mt-4 rounded-full bg-white/20 backdrop-blur-md hover:bg-emerald-600/80 transition-colors duration-200"
      aria-label="Previous slide"
    >
      <ChevronLeftIcon class="h-5 w-5 sm:h-6 sm:w-6 text-white" />
    </button>
    <button 
      @click="nextSlide"
      class="absolute right-2 sm:right-6 top-1/2 -translate-y-1/2 p-2 sm:p-3 rounded-full bg-white/20 backdrop-blur-md hover:bg-emerald-600/80 transition-colors duration-200"
      aria-label="Next slide"
    >
      <ChevronRightIcon class="h-5 w-5 sm:h-6 sm:w-6 text-white" />
    </button>
    <!-- Indicators -->
    <div class="absolute bottom-4 sm:bottom-8 left-1/2 -translate-x-1/2 flex space-x-2">
      <button
        v-for="(slide, index) in slides"
        :key="slide.id"
        @click="goToSlide(index)"
        class="h-2 w-6 sm:h-3 sm:w-8 rounded-full transition-all duration-300"
        :class="currentSlide === index ? 'bg-emerald-400' : 'bg-white/50 hover:bg-white/80'"
        aria-label="Go to slide"
      />
    </div>
  </div>
</template>