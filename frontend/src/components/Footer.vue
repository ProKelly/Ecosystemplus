<template>
  <footer class="bg-[hsl(var(--forest-green))] text-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Main Footer Content -->
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
        <!-- Company Info -->
        <div class="lg:col-span-2">
          <div class="flex items-center space-x-2 mb-6">
            <span class="text-[hsl(var(--bright-yellow))] text-3xl">🌿</span>
            <span class="text-3xl font-bold">EcoSystem+</span>
          </div>
          <p class="text-green-100 leading-relaxed mb-6 max-w-md">
            Revolutionizing agriculture across Africa with cutting-edge satellite technology, AI-powered insights, and sustainable farming solutions.
          </p>
          <div class="flex space-x-4">
            <a href="#" class="w-10 h-10 bg-[hsl(var(--bright-yellow))] rounded-full flex items-center justify-center text-black hover:scale-110 transition-transform duration-300">
              <span class="h-5 w-5">📘</span>
            </a>
            <a href="#" class="w-10 h-10 bg-[hsl(var(--bright-yellow))] rounded-full flex items-center justify-center text-black hover:scale-110 transition-transform duration-300">
              <span class="h-5 w-5">🐦</span>
            </a>
            <a href="#" class="w-10 h-10 bg-[hsl(var(--bright-yellow))] rounded-full flex items-center justify-center text-black hover:scale-110 transition-transform duration-300">
              <span class="h-5 w-5">💼</span>
            </a>
            <a href="#" class="w-10 h-10 bg-[hsl(var(--bright-yellow))] rounded-full flex items-center justify-center text-black hover:scale-110 transition-transform duration-300">
              <span class="h-5 w-5">📸</span>
            </a>
          </div>
        </div>
        <!-- Features -->
        <div>
          <h3 class="text-xl font-bold mb-6 text-[hsl(var(--bright-yellow))]">Features</h3>
          <ul class="space-y-3">
            <li><router-link to="/module/crop-classification"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Crop Classification</span></router-link></li>
            <li><router-link to="/module/crop-monitoring"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Crop Monitoring</span></router-link></li>
            <li><router-link to="/module/yield-prediction"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Yield Prediction</span></router-link></li>
            <li><router-link to="/module/soil-moisture"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Soil Moisture Analysis</span></router-link></li>
            <li><router-link to="/module/forest-monitoring"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Forest Monitoring</span></router-link></li>
            <li><router-link to="/module/carbon-modeling"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Carbon Modeling</span></router-link></li>
          </ul>
        </div>
        <!-- Support -->
        <div>
          <h3 class="text-xl font-bold mb-6 text-[hsl(var(--bright-yellow))]">Support</h3>
          <ul class="space-y-3">
            <li><a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Help Center</a></li>
            <li><a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Documentation</a></li>
            <li><a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">API Reference</a></li>
            <li><a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Training Videos</a></li>
            <li><a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Community Forum</a></li>
            <li><router-link to="/contact"><span class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 cursor-pointer">Contact Support</span></router-link></li>
          </ul>
        </div>
      </div>
      <!-- Bottom Footer -->
      <div class="border-t border-green-600 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-green-100 text-sm mb-4 md:mb-0">
          © 2024 EcoSystem+. All rights reserved. | Powered by Sentinel Satellite Data
        </p>
        <div class="flex space-x-6 text-sm">
          <a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Privacy Policy</a>
          <a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Terms of Service</a>
          <a href="#" class="text-green-100 hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200">Cookie Policy</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<style scoped>
/* Add your styles here or use Tailwind CSS as in the original */
</style>
