<template>
  <section class="relative py-20 bg-gradient-to-b from-white to-[hsl(var(--light-gray))]/30">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5">
      <img 
        src="https://images.unsplash.com/photo-1518837695005-2083093ee35b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&h=1080" 
        alt="Satellite imagery data visualization patterns" 
        class="w-full h-full object-cover" 
      />
    </div>
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold text-[hsl(var(--forest-green))] mb-6 animate-fade-in">
          Comprehensive Agricultural Intelligence
        </h2>
        <p class="text-lg sm:text-xl text-black max-w-3xl mx-auto animate-fade-in">
          Eight powerful modules powered by Sentinel satellite data to transform farming across Africa
        </p>
      </div>
      <!-- Modules Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 lg:gap-8">
        <div v-for="(module, index) in modules" :key="module.id">
          <div 
            class="glassmorphism rounded-3xl p-6 shadow-xl hover:shadow-2xl hover:border-2 hover:border-[hsl(var(--bright-yellow))]/50 transition-all duration-300 hover:-translate-y-2 group h-full flex flex-col"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="aspect-video w-full mb-6 overflow-hidden rounded-2xl">
              <img 
                :src="module.image" 
                :alt="`${module.title} - Advanced satellite monitoring technology for precision agriculture`" 
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
              />
            </div>
            <div class="flex-1 flex flex-col space-y-4">
              <div class="flex items-center space-x-3">
                <span class="text-2xl flex-shrink-0">{{ module.icon }}</span>
                <h3 class="text-lg sm:text-xl font-bold text-[hsl(var(--forest-green))] group-hover:text-[hsl(var(--bright-yellow))] transition-colors duration-300 leading-tight">
                  {{ module.title }}
                </h3>
              </div>
              <p class="text-sm sm:text-base text-black leading-relaxed flex-1">
                {{ module.description }}
              </p>
              <ul class="text-xs text-left pl-4 list-disc">
                <li v-for="feature in module.features" :key="feature">{{ feature }}</li>
              </ul>
              <div class="pt-4">
                <router-link :to="`/module/${module.id}`">
                  <button 
                    class="w-full bg-[hsl(var(--bright-yellow))] text-black px-4 py-3 rounded-full font-semibold hover:scale-105 hover:shadow-lg transition-all duration-300 animate-glow text-sm sm:text-base flex items-center justify-center"
                  >
                    <span class="mr-2">→</span>
                    Explore Module
                  </button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Call to Action -->
      <div class="text-center mt-16">
        <p class="text-lg text-gray-600 mb-6">
          Ready to transform your agricultural operations?
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/pricing">
            <button 
              class="bg-[hsl(var(--bright-yellow))] text-black px-8 py-4 rounded-full text-lg font-bold hover:scale-105 hover:shadow-xl transition-all duration-300 animate-glow"
            >
              View Pricing Plans
            </button>
          </router-link>
          <router-link to="/contact">
            <button 
              class="border border-[hsl(var(--forest-green))] text-[hsl(var(--forest-green))] hover:bg-[hsl(var(--forest-green))] hover:text-white px-8 py-4 rounded-full text-lg font-bold hover:scale-105 transition-all duration-300"
            >
              Contact Sales
            </button>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { MODULES } from '@/constants/modules'
const modules = MODULES
</script>

<style scoped>
/* Add your styles here or use Tailwind CSS as in the original */
</style>
