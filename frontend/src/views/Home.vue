<script setup lang="ts">
import HeroCarousel from '@/components/HeroCarousel.vue'
import ModuleGrid from '@/components/ModuleGrid.vue'
</script>

<template class="w-full">
  <div class="min-h-screen flex flex-col justify-between bg-white">
    <div class="flex-1 space-y-16 md:space-y-24 pb-20">
      <!-- Hero Section -->
      <section class="pt-4 md:pt-8 max-w-7xl mx-auto">
        <HeroCarousel />
      </section>

      <!-- Modules Grid Section -->
      <section class="relative max-w-7xl mx-auto px-6 mt-16 mb-16 flex flex-col items-center">
        <!-- Decorative background shapes -->
        <div class="absolute -top-16 left-1/2 -translate-x-1/2 w-56 h-56 bg-emerald-100 rounded-full blur-3xl opacity-40 pointer-events-none z-0"></div>
        <div class="absolute top-10 right-10 w-24 h-24 bg-gradient-to-br from-green-200 to-emerald-100 rounded-full blur-2xl opacity-30 pointer-events-none z-0"></div>
        <div class="absolute bottom-0 left-0 w-20 h-20 bg-green-50 rounded-full blur-xl opacity-30 pointer-events-none z-0"></div>
        <div class="w-full space-y-10 md:space-y-16 z-10">
          <div class="flex flex-col items-center text-center relative">
           
            <span class="inline-flex items-center gap-2 mb-4 px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold tracking-widest uppercase shadow-sm">
              <svg class='h-4 w-4 text-emerald-400' fill='currentColor' viewBox='0 0 20 20'><path d='M10 2a1 1 0 01.894.553l2.382 4.824 5.326.774a1 1 0 01.554 1.707l-3.853 3.755.91 5.308a1 1 0 01-1.451 1.054L10 16.347l-4.77 2.504A1 1 0 013.78 17.8l.91-5.308L.837 8.737a1 1 0 01.554-1.707l5.326-.774L9.1 2.553A1 1 0 0110 2z'/></svg>
              Precision Agriculture Suite 
            </span>
             <svg class="h-8 w-8 md:h-10 md:w-10 text-emerald-400 inline-block animate-bounce" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" /></svg>
          </div>
          <div class="w-full flex flex-col items-center">
            <ModuleGrid />
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="max-w-7xl mx-auto px-6">
        <div class="bg-gray-50 rounded-2xl p-8 md:p-12 border border-gray-100">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div v-for="stat in [
              { value: '10+', label: 'Active Farms' },
              { value: '92%', label: 'Accuracy Rate' },
              { value: '24/7', label: 'Monitoring' },
              { value: '10x', label: 'ROI Average' }
            ]" :key="stat.label" class="space-y-2">
              <p class="text-3xl md:text-4xl font-bold text-emerald-600 font-display">
                {{ stat.value }}
              </p>
              <p class="text-sm md:text-base font-medium text-gray-500 uppercase tracking-wider">
                {{ stat.label }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Redesigned Testimonial Section -->
      <section class="max-w-5xl mx-auto px-6 mt-12">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Testimonial 1 -->
          <div class="relative bg-white rounded-2xl shadow-xl p-8 md:p-10 flex flex-col items-center text-center overflow-hidden border border-gray-100 transition-transform duration-300 hover:scale-[1.025] hover:shadow-2xl">
            <div class="absolute -top-8 left-1/2 -translate-x-1/2">
              <div class="bg-emerald-100 rounded-full p-2 shadow-md">
                <svg class="h-10 w-10 text-amber-400" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z" />
                </svg>
              </div>
            </div>
            <div class="mt-8">
              <blockquote class="text-2xl md:text-2xl font-semibold text-gray-800 leading-relaxed max-w-xl mx-auto italic">
                “EcoSystem+ transformed our 5,000-acre operation. The yield prediction module alone increased our productivity by 22% in the first season.”
              </blockquote>
            </div>
            <div class="flex flex-col items-center mt-8">
              <img src="https://randomuser.me/api/portraits/women/89.jpg" alt="Sarah Johnson" class="w-16 h-16 rounded-full border-4 border-emerald-200 shadow-md mb-2">
              <p class="text-lg font-bold text-gray-900">Sarah Johnson</p>
              <p class="text-gray-500 text-sm">Farm Director, Green Valley Agribusiness</p>
            </div>
          </div>
          <!-- Testimonial 2 -->
          <div class="relative bg-white rounded-2xl shadow-xl p-8 md:p-10 flex flex-col items-center text-center overflow-hidden border border-gray-100 transition-transform duration-300 hover:scale-[1.025] hover:shadow-2xl">
            <div class="absolute -top-8 left-1/2 -translate-x-1/2">
              <div class="bg-emerald-100 rounded-full p-2 shadow-md">
                <svg class="h-10 w-10 text-amber-400" fill="currentColor" viewBox="0 0 32 32">
                  <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z" />
                </svg>
              </div>
            </div>
            <div class="mt-8">
              <blockquote class="text-2xl md:text-2xl font-semibold text-gray-800 leading-relaxed max-w-xl mx-auto italic">
                “With EcoSystem+, our soil analysis and crop monitoring are now seamless. The insights are actionable and the support team is fantastic!”
              </blockquote>
            </div>
            <div class="flex flex-col items-center mt-8">
              <img src="https://randomuser.me/api/portraits/men/59.jpg" alt="James Lee" class="w-16 h-16 rounded-full border-4 border-emerald-200 shadow-md mb-2">
              <p class="text-lg font-bold text-gray-900">James Lee</p>
              <p class="text-gray-500 text-sm">Operations Manager, Sunrise Farms</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="max-w-7xl mx-auto px-6 flex flex-col items-center justify-center">
        <div class="relative bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl p-8 md:p-12 text-white overflow-hidden w-full flex flex-col items-center justify-center">
          <div class="absolute inset-0 opacity-10">
            <div class="absolute inset-0 bg-[url('@/assets/pattern.svg')] bg-repeat"></div>
          </div>
          <div class="relative max-w-3xl mx-auto text-center flex flex-col items-center justify-center">
            <h2 class="text-3xl md:text-4xl font-bold mb-4 font-display leading-tight">
              Ready to transform your agricultural operations?
            </h2>
            <p class="text-lg md:text-xl mb-8 opacity-90 leading-relaxed">
              Join thousands of farmers and agribusinesses leveraging AI to make data-driven decisions.
            </p>
            <div class="flex flex-col sm:flex-row justify-center items-center gap-4">
              <button class="px-8 py-3.5 bg-white text-emerald-600 rounded-full font-semibold hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl">
                Get Started
              </button>
              <button class="px-8 py-3.5 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 hover:bg-white/20 transition-all duration-300 font-semibold hover:shadow-lg">
                Request Demo
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

.font-display {
  font-family: 'Playfair Display', serif;
}

body {
  font-family: 'Inter', sans-serif;
}

/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}

/* Custom pattern for CTA section */
.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
</style>