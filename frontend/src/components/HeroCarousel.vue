<template>
  <section 
    class="relative h-screen overflow-hidden"
    @mouseenter="isAutoScrollPaused = true"
    @mouseleave="isAutoScrollPaused = false"
  >
    <!-- Carousel Images -->
    <div class="relative w-full h-full">
      <div
        v-for="(image, index) in carouselImages"
        :key="index"
        :class="['absolute inset-0 transition-opacity duration-1000', index === currentSlide ? 'opacity-100 z-10' : 'opacity-0 z-0']"
      >
        <img 
          :src="image.url" 
          :alt="`${image.title} - Advanced agricultural satellite monitoring technology`" 
          class="w-full h-full object-cover" 
        />
        <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-black/10 to-black/40"></div>
      </div>
    </div>
    <!-- Content Overlay -->
    <div class="absolute inset-0 z-20 flex items-center justify-center">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="space-y-6 sm:space-y-8">
          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight animate-fade-in-up">
            {{ carouselImages[currentSlide].title }}
          </h1>
          <p class="text-lg sm:text-xl md:text-2xl lg:text-3xl text-white/90 font-medium max-w-4xl mx-auto animate-fade-in-up delay-200">
            {{ carouselImages[currentSlide].subtitle }}
          </p>
          <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center items-center animate-fade-in-up delay-400">
            <router-link to="/pricing">
              <button 
                class="bg-[hsl(var(--bright-yellow))] text-black px-6 sm:px-8 py-3 sm:py-4 rounded-full text-base sm:text-lg font-bold hover:scale-105 hover:shadow-xl transition-all duration-300 animate-glow w-full sm:w-auto"
              >
                {{ carouselImages[currentSlide].cta }}
              </button>
            </router-link>
            <button class="text-white text-base sm:text-lg font-semibold hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 relative group w-full sm:w-auto">
              <span class="inline mr-2">▶</span>
              Watch Demo
              <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-[hsl(var(--bright-yellow))] transition-all duration-300 group-hover:w-full"></span>
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Navigation Controls -->
    <button
      @click="prevSlide"
      class="absolute left-4 sm:left-8 top-1/2 transform -translate-y-1/2 z-30 bg-white/20 backdrop-blur-sm rounded-full p-2 sm:p-3 text-white hover:bg-white/30 hover:scale-110 transition-all duration-300"
    >
      <span class="h-5 w-5 sm:h-6 sm:w-6">&#8592;</span>
    </button>
    <button
      @click="nextSlide"
      class="absolute right-4 sm:right-8 top-1/2 transform -translate-y-1/2 z-30 bg-white/20 backdrop-blur-sm rounded-full p-2 sm:p-3 text-white hover:bg-white/30 hover:scale-110 transition-all duration-300"
    >
      <span class="h-5 w-5 sm:h-6 sm:w-6">&#8594;</span>
    </button>
    <!-- Dots Indicator -->
    <div class="absolute bottom-6 sm:bottom-8 left-1/2 transform -translate-x-1/2 z-30 flex space-x-2 sm:space-x-3">
      <button
        v-for="(_, index) in carouselImages"
        :key="index"
        @click="goToSlide(index)"
        :class="['w-2 h-2 sm:w-3 sm:h-3 rounded-full transition-all duration-300', index === currentSlide ? 'bg-[hsl(var(--bright-yellow))] scale-125' : 'bg-white/50 hover:bg-white/70']"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
const carouselImages = [
  {
    url: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Transform Agriculture with Satellite Intelligence',
    subtitle: 'Precision farming powered by Sentinel satellite data and AI technology',
    cta: 'Discover EcoSystem+'
  },
  {
    url: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Crop Classification Technology',
    subtitle: 'Identify crop types with precision using multispectral satellite imagery',
    cta: 'Explore Classification'
  },
  {
    url: 'https://images.unsplash.com/photo-1546026423-cc4642628d2b?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Real-Time Crop Monitoring',
    subtitle: 'Track crop health with NDVI analysis and stress detection',
    cta: 'Monitor Crops'
  },
  {
    url: 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Carbon Modeling & Sequestration',
    subtitle: 'Measure carbon storage and environmental impact with precision',
    cta: 'Carbon Insights'
  },
  {
    url: 'https://images.unsplash.com/photo-1500595046743-cd271d694d30?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Predict Future Yields',
    subtitle: 'Machine learning models for accurate harvest forecasting',
    cta: 'View Predictions'
  },
  {
    url: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160',
    title: 'Monitor Forest Conservation',
    subtitle: 'Detect deforestation and track environmental changes',
    cta: 'Forest Insights'
  }
]
const currentSlide = ref(0)
const isAutoScrollPaused = ref(false)
let intervalId: number | undefined

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % carouselImages.length
}
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + carouselImages.length) % carouselImages.length
}
const goToSlide = (index: number) => {
  currentSlide.value = index
}
onMounted(() => {
  intervalId = window.setInterval(() => {
    if (!isAutoScrollPaused.value) {
      nextSlide()
    }
  }, 8000)
})
onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
watch(isAutoScrollPaused, (paused) => {
  // Optionally handle pause/resume logic
})
</script>

<style scoped>
/* Add your styles here or use Tailwind CSS as in the original */
</style>
