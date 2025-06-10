<template>
  <section class="relative h-screen overflow-hidden">
    <div class="absolute inset-0 z-0">
      <div 
        class="flex h-full transition-transform duration-1000 ease-in-out"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
        @mouseenter="isAutoScrollPaused = true"
        @mouseleave="isAutoScrollPaused = false"
      >
        <div v-for="module in modules" :key="module.id" class="flex-none w-full h-full relative">
          <img 
            :src="module.image" 
            :alt="`${module.title} - Satellite imagery showing agricultural monitoring capabilities`" 
            class="w-full h-full object-cover" 
          />
          <div class="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/60"></div>
          <!-- Content Overlay -->
          <div class="absolute inset-0 flex items-center justify-center text-center z-10">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
              <div class="glassmorphism rounded-3xl p-8 md:p-12 shadow-2xl">
                <div class="text-6xl md:text-8xl mb-6">{{ module.icon }}</div>
                <h1 class="text-3xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                  {{ module.title }}
                </h1>
                <p class="text-lg md:text-xl lg:text-2xl text-white/90 mb-8 max-w-2xl mx-auto leading-relaxed">
                  {{ module.description }}
                </p>
                <ul class="text-xs text-left pl-4 list-disc text-white/90 mb-8">
                  <li v-for="feature in module.features" :key="feature">{{ feature }}</li>
                </ul>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                  <router-link :to="`/module/${module.id}`">
                    <button 
                      class="bg-[hsl(var(--bright-yellow))] text-black px-8 py-4 rounded-full text-lg font-bold hover:scale-105 hover:shadow-xl transition-all duration-300 flex items-center justify-center"
                    >
                      <span class="mr-2">→</span>
                      Explore Module
                    </button>
                  </router-link>
                  <router-link to="/pricing">
                    <button 
                      class="border-white text-white hover:bg-white hover:text-black px-8 py-4 rounded-full text-lg font-bold hover:scale-105 transition-all duration-300"
                    >
                      Get Started
                    </button>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Navigation Controls -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-20">
      <div class="flex items-center space-x-6 glassmorphism rounded-full px-6 py-3">
        <button
          @click="prevSlide"
          class="text-white hover:text-[hsl(var(--bright-yellow))] hover:bg-white/20 rounded-full transition-all duration-300 p-2"
        >
          <span class="sr-only">Previous</span>
          <span class="h-6 w-6">&#8592;</span>
        </button>
        <div class="flex space-x-2">
          <button
            v-for="(_, index) in modules"
            :key="index"
            @click="goToSlide(index)"
            :class="`w-3 h-3 rounded-full transition-all duration-300 ${index === currentSlide ? 'bg-[hsl(var(--bright-yellow))] scale-125' : 'bg-white/50 hover:bg-white/80'}`"
          />
        </div>
        <button
          @click="nextSlide"
          class="text-white hover:text-[hsl(var(--bright-yellow))] hover:bg-white/20 rounded-full transition-all duration-300 p-2"
        >
          <span class="sr-only">Next</span>
          <span class="h-6 w-6">&#8594;</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { MODULES } from '@/constants/modules'
const modules = MODULES
const currentSlide = ref(0)
const isAutoScrollPaused = ref(false)
let intervalId: number | undefined

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % modules.length
}
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + modules.length) % modules.length
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
