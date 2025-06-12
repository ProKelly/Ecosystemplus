<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

const mobileMenuOpen = ref(false)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-green-50 to-white flex flex-col">
    <!-- Navigation Bar -->
    <header class="fixed w-full z-50 bg-white/90 backdrop-blur-lg border-b border-green-100 shadow-lg">
      <nav class="mx-auto max-w-7xl px-6 py-3">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <RouterLink to="/" class="flex items-center space-x-3 group">
            <span class="text-3xl font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent tracking-tight group-hover:scale-105 transition-transform duration-200 no-underline">
              🌿EcoSystem+
            </span>
          </RouterLink>

          <!-- Desktop Navigation -->
          <div class="hidden lg:flex items-center space-x-10 relative">
            <!-- Modules Dropdown -->
            <div class="group relative">
              <button class="flex items-center gap-1 text-base font-semibold text-gray-700 hover:text-emerald-600 transition-colors duration-200 px-2 py-1 focus:outline-none">
                Modules
                <svg class="h-4 w-4 ml-1 text-emerald-400 group-hover:rotate-180 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>
              </button>
              <!-- Dropdown -->
              <div class="absolute left-0 top-full mt-2 w-60 bg-white rounded-xl shadow-xl border border-green-100 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-all duration-200 z-30 py-2">
                <RouterLink to="/field-detection" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Field Detection</RouterLink>
                <RouterLink to="/classification" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Crop Classification</RouterLink>
                <RouterLink to="/monitoring" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Crop Monitoring</RouterLink>
                <RouterLink to="/soil-analysis" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Soil Analysis</RouterLink>
                <RouterLink to="/yield-prediction" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Yield Prediction</RouterLink>
                <RouterLink to="/carbon-model" class="block px-5 py-3 text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150 text-base font-semibold">Carbon Model</RouterLink>
              </div>
            </div>
            <!-- About Link -->
            <RouterLink to="/about" class="text-base font-semibold text-gray-700 hover:text-emerald-600 transition-colors duration-200 px-2 py-1">About</RouterLink>
            <!-- Dashboard Button -->
            <RouterLink 
              to="/dashboard" 
              class="ml-6 px-5 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-base font-bold rounded-xl shadow-md hover:shadow-lg hover:scale-105 transition-all duration-200"
            >
              Login
            </RouterLink>
          </div>

          <!-- Mobile menu button -->
          <div class="lg:hidden">
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="p-2 text-gray-700 hover:text-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-400 rounded-lg"
            >
              <Bars3Icon v-if="!mobileMenuOpen" class="h-7 w-7" />
              <XMarkIcon v-else class="h-7 w-7" />
            </button>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <transition name="fade">
          <div 
            v-show="mobileMenuOpen"
            class="lg:hidden mt-4 pb-4 space-y-3 bg-white/95 rounded-xl shadow-lg px-4 pt-4"
          >
            <RouterLink 
              v-for="link in [
                { name: 'Field Detection', path: '/field-detection' },
                { name: 'Crop Classification', path: '/classification' },
                { name: 'Crop Monitoring', path: '/monitoring' },
                { name: 'Soil Analysis', path: '/soil-analysis' },
                { name: 'Yield Prediction', path: '/yield-prediction' },
                { name: 'Carbon Model', path: '/carbon-model' },
              ]"
              :key="link.path"
              :to="link.path"
              @click="mobileMenuOpen = false"
              class="block px-3 py-2 rounded-lg text-lg font-semibold text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150"
              active-class="bg-green-50 text-emerald-600 font-bold"
            >
              {{ link.name }}
            </RouterLink>
            <RouterLink 
              to="/dashboard" 
              @click="mobileMenuOpen = false"
              class="block mt-4 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-lg font-bold rounded-xl text-center shadow-md hover:scale-105 transition-transform duration-150"
            >
              My Dashboard
            </RouterLink>
          </div>
        </transition>
      </nav>
    </header>

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-green-100 py-10 mt-10 shadow-inner">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="flex items-center space-x-3 mb-4 md:mb-0">
            <span class="text-xl font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent tracking-tight">
              🌿EcoSystem+
            </span>
          </div>
          <div class="flex space-x-8">
            <a href="#" class="text-gray-500 hover:text-emerald-600 transition-colors duration-150">
              <span class="sr-only">Twitter</span>
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
            <a href="#" class="text-gray-500 hover:text-emerald-600 transition-colors duration-150">
              <span class="sr-only">GitHub</span>
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
              </svg>
            </a>
          </div>
        </div>
        <p class="mt-8 text-center text-base text-gray-500 font-medium">
          &copy; 2023 EcoSystem+. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}

/* Remove underline from logo/name */
.group .no-underline, .group .no-underline:after, .group .no-underline:before {
  text-decoration: none !important;
  box-shadow: none !important;
}

/* Router link transitions */
.router-link-active {
  position: relative;
}

.router-link-active:not(.dashboard-link):not(.group)::-after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #16a34a, #10b981);
  border-radius: 2px;
}

/* Page transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>