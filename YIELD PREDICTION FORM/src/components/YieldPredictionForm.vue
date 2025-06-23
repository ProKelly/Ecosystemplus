<template>
  <div class="w-full">
    <!-- Main Form Card -->
    <div class="glass-card p-6 sm:p-8 relative">
      <!-- Loading Overlay -->
      <transition
        enter-active-class="transition-all duration-500 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-modal">
            <div class="w-16 h-16 bg-gradient-to-br from-emerald-500 to-green-500 rounded-2xl flex items-center justify-center mx-auto mb-6 animate-pulse-gentle">
              <svg class="w-8 h-8 text-white animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Processing Your Data</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">Our advanced AI is analyzing your farm conditions and environmental factors...</p>
            
            <!-- Progress Bar -->
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressWidth + '%' }"></div>
            </div>
            
            <div class="flex justify-center gap-2 mt-4">
              <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse-gentle"></div>
              <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse-gentle" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse-gentle" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Actual Yield Flow (conditional) -->
      <div v-if="showActualYieldFlow" class="glass-card-blue p-6 mb-8">
        <h3 class="text-lg font-bold text-blue-600 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C13.1046 2 14 2.89543 14 4V6H10V4C10 2.89543 10.8954 2 12 2Z" fill="currentColor"/>
            <path d="M5 8C5 6.89543 5.89543 6 7 6H17C18.1046 6 19 6.89543 19 8V20C19 21.1046 18.1046 22 17 22H7C5.89543 22 5 21.1046 5 20V8Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          Accuracy Feedback
        </h3>
        <p class="text-gray-600 mb-4">Help us improve our predictions by providing your actual harvest results.</p>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-bold text-emerald-700 mb-2">Was the predicted yield what you actually harvested?</label>
            <div class="flex gap-4">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="actualYield.harvested" :value="true" class="text-emerald-500">
                <span class="text-gray-700">Yes, prediction was accurate</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="actualYield.harvested" :value="false" class="text-emerald-500">
                <span class="text-gray-700">No, I got a different yield</span>
              </label>
            </div>
          </div>
          
          <div v-if="actualYield.harvested === false">
            <label for="actualYieldValue" class="block text-sm font-bold text-emerald-700 mb-2">Actual Yield Value</label>
            <input
              id="actualYieldValue"
              v-model.number="actualYield.value"
              type="number"
              min="0"
              step="0.01"
              class="form-field-base form-field-focus mb-3"
              placeholder="Enter numeric yield value"
            />
            <label for="actualYieldUnit" class="block text-sm font-bold text-emerald-700 mb-2">Unit</label>
            <input
              id="actualYieldUnit"
              v-model="actualYield.unit"
              type="text"
              class="form-field-base form-field-focus"
              placeholder="e.g. tons/ha, kg/ha"
            />
          </div>
        </div>
        <!-- Submit Button -->
        <button
          @click="submitActualYield"
          class="mt-6 btn-primary flex items-center justify-center gap-2 group"
          type="button"
          :disabled="isLoading"
        >
          <span v-if="!isLoading" class="flex items-center gap-2">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 12H19M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Submit Actual Yield</span>
          </span>
          <span v-else class="flex items-center gap-2">
            <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            </svg>
            <span>Submitting...</span>
          </span>
        </button>
      </div>

      <!-- Form Header -->
      <div v-if="!showActualYieldFlow" class="text-center mb-8">
        <h2 class="text-3xl sm:text-4xl font-bold gradient-text mb-4">
          Yield Prediction
        </h2>
        <p class="text-lg text-gray-600 leading-relaxed">
          Enter your farm details to get AI-powered yield predictions with advanced analytics
        </p>
      </div>

      <!-- Form -->
      <form v-if="!showActualYieldFlow" @submit.prevent="submitForm" class="form-spacing">
        <!-- Commune Field -->
        <div class="field-spacing">
          <label for="commune" class="block text-sm font-bold text-emerald-700 flex items-center gap-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 13C13.6569 13 15 11.6569 15 10C15 8.34315 13.6569 7 12 7C10.3431 7 9 8.34315 9 10C9 11.6569 10.3431 13 12 13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Commune <span class="text-red-500">*</span>
          </label>
          
          <!-- Searchable Select -->
          <div class="relative">
            <div 
              class="dropdown-trigger"
              :class="{ 'form-field-valid': formData.commune && !errors.commune, 'form-field-error': errors.commune }"
              @click="toggleCommuneDropdown"
            >
              <span :class="formData.commune ? 'text-gray-900' : 'text-gray-500'">
                {{ formData.commune || 'Search for your commune...' }}
              </span>
              <div class="flex items-center gap-2">
                <svg v-if="formData.commune" class="w-4 h-4 text-green-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg class="w-4 h-4 text-green-500 transition-transform duration-300" :class="{ 'rotate-180': communeDropdownOpen }" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </div>
            
            <!-- Dropdown Menu -->
            <transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="opacity-0 transform -translate-y-4 scale-95"
              enter-to-class="opacity-100 transform translate-y-0 scale-100"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="opacity-100 transform translate-y-0 scale-100"
              leave-to-class="opacity-0 transform -translate-y-4 scale-95"
            >
              <div v-if="communeDropdownOpen" class="dropdown-menu">
                <!-- Search Header -->
                <div class="dropdown-search">
                  <div class="relative">
                    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-green-500" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <input
                      v-model="communeSearchQuery"
                      type="text"
                      class="dropdown-search-input"
                      placeholder="Search communes..."
                      @input="filterCommunes"
                    />
                  </div>
                </div>
                
                <!-- Options List -->
                <div class="dropdown-options">
                  <div
                    v-for="commune in filteredCommunes"
                    :key="commune"
                    class="dropdown-option"
                    :class="{ 'dropdown-option-selected': formData.commune === commune }"
                    @click="selectCommune(commune)"
                  >
                    <span class="font-medium">{{ commune }}</span>
                    <svg v-if="formData.commune === commune" class="w-4 h-4 text-green-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  
                  <!-- No Results -->
                  <div v-if="filteredCommunes.length === 0" class="px-4 py-6 text-center text-gray-500">
                    <div class="text-2xl mb-2">🔍</div>
                    <p>No communes found</p>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          
          <span v-if="errors.commune" class="text-red-600 text-sm font-medium flex items-center gap-2 animate-fade-in">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
            </svg>
            {{ errors.commune }}
          </span>
        </div>

        <!-- Crop Name Field -->
        <div class="field-spacing">
          <label for="crop" class="block text-sm font-bold text-emerald-700 flex items-center gap-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
            </svg>
            Crop Name <span class="text-red-500">*</span>
          </label>
          
          <!-- Searchable Select -->
          <div class="relative">
            <div 
              class="dropdown-trigger"
              :class="{ 'form-field-valid': formData.cropName && !errors.cropName, 'form-field-error': errors.cropName }"
              @click="toggleCropDropdown"
            >
              <span :class="formData.cropName ? 'text-gray-900' : 'text-gray-500'">
                {{ formData.cropName || 'Search for your crop...' }}
              </span>
              <div class="flex items-center gap-2">
                <svg v-if="formData.cropName" class="w-4 h-4 text-green-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg class="w-4 h-4 text-green-500 transition-transform duration-300" :class="{ 'rotate-180': cropDropdownOpen }" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </div>
            
            <!-- Dropdown Menu -->
            <transition
              enter-active-class="transition-all duration-300 ease-out"
              enter-from-class="opacity-0 transform -translate-y-4 scale-95"
              enter-to-class="opacity-100 transform translate-y-0 scale-100"
              leave-active-class="transition-all duration-200 ease-in"
              leave-from-class="opacity-100 transform translate-y-0 scale-100"
              leave-to-class="opacity-0 transform -translate-y-4 scale-95"
            >
              <div v-if="cropDropdownOpen" class="dropdown-menu">
                <!-- Search Header -->
                <div class="dropdown-search">
                  <div class="relative">
                    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-green-500" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <input
                      v-model="cropSearchQuery"
                      type="text"
                      class="dropdown-search-input"
                      placeholder="Search crops..."
                      @input="filterCrops"
                    />
                  </div>
                </div>
                
                <!-- Options List -->
                <div class="dropdown-options">
                  <div
                    v-for="crop in filteredCrops"
                    :key="crop.name"
                    class="dropdown-option"
                    :class="{ 'dropdown-option-selected': formData.cropName === crop.name }"
                    @click="selectCrop(crop)"
                  >
                    <div class="flex flex-col">
                      <span class="font-medium">{{ crop.name }}</span>
                      <span class="text-sm text-gray-500">{{ crop.local }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">{{ crop.category }}</span>
                      <svg v-if="formData.cropName === crop.name" class="w-4 h-4 text-green-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                  </div>
                  
                  <!-- No Results -->
                  <div v-if="filteredCrops.length === 0" class="px-4 py-6 text-center text-gray-500">
                    <div class="text-2xl mb-2">🌾</div>
                    <p>No crops found</p>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          
          <span v-if="errors.cropName" class="text-red-600 text-sm font-medium flex items-center gap-2 animate-fade-in">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
            </svg>
            {{ errors.cropName }}
          </span>
        </div>

        <!-- Email Field -->
        <div class="field-spacing">
          <label for="email" class="block text-sm font-bold text-emerald-700 flex items-center gap-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 8L10.89 13.26C11.2187 13.4793 11.6049 13.5963 12 13.5963C12.3951 13.5963 12.7813 13.4793 13.11 13.26L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Email Address <span class="text-red-500">*</span>
          </label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            class="form-field-base form-field-focus"
            :class="{ 'form-field-valid': formData.email && !errors.email, 'form-field-error': errors.email }"
            placeholder="Enter your email address"
            @input="validateEmail"
          />
          <span v-if="errors.email" class="text-red-600 text-sm font-medium flex items-center gap-2 animate-fade-in">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
            </svg>
            {{ errors.email }}
          </span>
        </div>

        <!-- Farm Size Field -->
        <div class="field-spacing">
          <label for="farmSize" class="block text-sm font-bold text-emerald-700 flex items-center gap-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3H21V21H3V3ZM5 5V19H19V5H5ZM7 7H17V9H7V7ZM7 11H17V13H7V11ZM7 15H17V17H7V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Farm Size (hectares) <span class="text-red-500">*</span>
          </label>
          <input
            id="farmSize"
            v-model="formData.farmSize"
            type="number"
            min="0.1"
            step="0.1"
            class="form-field-base form-field-focus"
            :class="{ 'form-field-valid': formData.farmSize && !errors.farmSize, 'form-field-error': errors.farmSize }"
            placeholder="Enter farm size in hectares"
            @input="validateFarmSize"
          />
          <span v-if="errors.farmSize" class="text-red-600 text-sm font-medium flex items-center gap-2 animate-fade-in">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
            </svg>
            {{ errors.farmSize }}
          </span>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn-primary flex items-center justify-center gap-3 group"
          :disabled="!isFormValid || isLoading"
        >
          <span v-if="!isLoading" class="flex items-center gap-3">
            <div class="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center group-hover:bg-white/30 transition-colors duration-300">
              <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 2H15C16.1046 2 17 2.89543 17 4V5H19C20.1046 5 21 5.89543 21 7V9H20V15H21V17C21 18.1046 20.1046 19 19 19H17V20C17 21.1046 16.1046 22 15 22H9C7.89543 22 7 21.1046 7 20V19H5C3.89543 19 3 18.1046 3 17V15H4V9H3V7C3 5.89543 3.89543 5 5 5H7V4C7 2.89543 7.89543 2 9 2ZM9 8C8.44772 8 8 8.44772 8 9V15C8 15.5523 8.44772 16 9 16H15C15.5523 16 16 15.5523 16 15V9C16 8.44772 15.5523 8 15 8H9Z" fill="currentColor"/>
              </svg>
            </div>
            <span>Get AI-Powered Prediction</span>
          </span>
          <span v-else class="flex items-center gap-3">
            <div class="w-6 h-6 animate-spin">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              </svg>
            </div>
            <span>Analyzing Data...</span>
          </span>
        </button>
      </form>

      <!-- Footer Branding -->
      <div class="border-t border-gray-200/50 mt-8 pt-6 text-center">
        <div class="flex items-center justify-center gap-2 mb-2">
          <div class="w-6 h-6 bg-gradient-to-br from-emerald-500 to-green-500 rounded-lg flex items-center justify-center">
            <svg class="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
            </svg>
          </div>
          <span class="text-lg font-bold text-emerald-700">ECOSYSTEM +</span>
        </div>
        <p class="text-sm text-gray-500">AI-Powered Agricultural Intelligence</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { communes } from '../data/communes.js'
import { crops } from '../data/crops.js'

// Props and Emits
const emit = defineEmits(['prediction-complete', 'form-reset'])

// Reactive data
const formData = reactive({
  commune: '',
  cropName: '',
  email: '',
  farmSize: ''
})

const errors = reactive({
  commune: '',
  cropName: '',
  email: '',
  farmSize: ''
})

const isLoading = ref(false)
const progressWidth = ref(0)
const communeDropdownOpen = ref(false)
const cropDropdownOpen = ref(false)
const communeSearchQuery = ref('')
const cropSearchQuery = ref('')
const filteredCommunes = ref([])
const filteredCrops = ref([])
const showActualYieldFlow = ref(false)

const actualYield = reactive({
  harvested: null,
  value: '',
  unit: ''
})

const predictionResult = ref(null)

// API Endpoints Configuration
const API_CONFIG = {
  PREDICTION_ENDPOINT: 'https://curious-narwhal-evident.ngrok-free.app/webhook-test/predict_yield',
  ACTUAL_YIELD_ENDPOINT: 'https://curious-narwhal-evident.ngrok-free.app/webhook-test/94cc7a69-6dfc-4ce5-8f61-4492dcc93757',
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
};

// --- Normalization helpers ---
function normalizeCommune(commune) {
  return commune.toLowerCase().replace(/\s+/g, '_').replace(/[’'`]/g, '').replace(/[^a-z0-9_]/g, '');
}
function normalizeCrop(crop) {
  return crop.toLowerCase().replace(/\s+/g, '_').replace(/[’'`]/g, '').replace(/[^a-z0-9_]/g, '');
}

// --- LocalStorage helpers ---
function storePrediction(predictionResult) {
  const storageData = {
    ...predictionResult,
    stored_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString() // 6 months
  };
  localStorage.setItem('previous_prediction', JSON.stringify(storageData));
}
function cleanExpiredPredictions() {
  const stored = localStorage.getItem('previous_prediction');
  if (stored) {
    try {
      const data = JSON.parse(stored);
      if (new Date(data.expires_at) < new Date()) {
        localStorage.removeItem('previous_prediction');
      }
    } catch (error) {
      localStorage.removeItem('previous_prediction');
    }
  }
}

// --- Error handling ---
function handleApiError(error, context) {
  console.error(`${context} error:`, error);
  // Network errors
  if (!navigator.onLine) {
    alert('No Internet Connection. Please check your internet connection and try again.');
    return;
  }
  // Timeout errors
  if (error.name === 'AbortError') {
    alert('Request Timeout. The request took too long. Please try again.');
    return;
  }
  // API-specific errors
  if (error.message && error.message.includes('prediction')) {
    alert('Prediction Error: ' + error.message);
  } else {
    alert('Something went wrong. Please try again in a few moments.');
  }
}

// Computed properties
const isFormValid = computed(() => {
  return formData.commune && 
         formData.cropName && 
         formData.email && 
         formData.farmSize && 
         !errors.commune && 
         !errors.cropName && 
         !errors.email && 
         !errors.farmSize
})

// Methods
const toggleCommuneDropdown = () => {
  communeDropdownOpen.value = !communeDropdownOpen.value
  if (communeDropdownOpen.value) {
    filteredCommunes.value = communes.slice(0, 20)
  }
}

const toggleCropDropdown = () => {
  cropDropdownOpen.value = !cropDropdownOpen.value
  if (cropDropdownOpen.value) {
    filteredCrops.value = crops.slice(0, 20)
  }
}

const filterCommunes = () => {
  const query = communeSearchQuery.value.toLowerCase()
  filteredCommunes.value = communes
    .filter(commune => commune.toLowerCase().includes(query))
    .slice(0, 20)
}

const filterCrops = () => {
  const query = cropSearchQuery.value.toLowerCase()
  filteredCrops.value = crops
    .filter(crop => 
      crop.name.toLowerCase().includes(query) ||
      crop.local.toLowerCase().includes(query)
    )
    .slice(0, 20)
}

const selectCommune = (commune) => {
  formData.commune = commune
  communeDropdownOpen.value = false
  communeSearchQuery.value = ''
  errors.commune = ''
}

const selectCrop = (crop) => {
  formData.cropName = crop.name
  cropDropdownOpen.value = false
  cropSearchQuery.value = ''
  errors.cropName = ''
}

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.email) {
    errors.email = 'Email is required'
  } else if (!emailRegex.test(formData.email)) {
    errors.email = 'Please enter a valid email address'
  } else {
    errors.email = ''
  }
}

const validateFarmSize = () => {
  const size = parseFloat(formData.farmSize)
  if (!formData.farmSize) {
    errors.farmSize = 'Farm size is required'
  } else if (isNaN(size) || size <= 0) {
    errors.farmSize = 'Please enter a valid farm size'
  } else if (size > 10000) {
    errors.farmSize = 'Farm size seems too large. Please verify.'
  } else {
    errors.farmSize = ''
  }
}

const startProgressAnimation = () => {
  progressWidth.value = 0
  const interval = setInterval(() => {
    if (progressWidth.value < 90) {
      progressWidth.value += Math.random() * 15
    }
  }, 500)
  return interval
}

const submitForm = async () => {
  // Require feedback on previous prediction before new submission
  if (showActualYieldFlow.value) {
    if (actualYield.harvested === null) {
      alert('Please confirm whether the previous prediction matched your actual yield.');
      return;
    }
    if (!actualYield.harvested && !actualYield.value) {
      alert('Please enter your actual yield value and unit.');
      return;
    }
  }
  if (!isFormValid.value) return;
  isLoading.value = true;
  const progressInterval = startProgressAnimation();
  setTimeout(() => { progressWidth.value = 10; }, 100);

  // 1. Validate form data locally (already done by computed)
  // 2. Prepare normalized payload
  const payload = {
    crop_type: normalizeCrop(formData.cropName),
    town: normalizeCommune(formData.commune),
    farm_size: parseFloat(formData.farmSize),
    contact: formData.email.trim()
  };

  try {
    // 3. Send POST request
    console.log('Sending payload to n8n:', payload);
    const response = await fetch(API_CONFIG.PREDICTION_ENDPOINT, {
      method: 'POST',
      headers: API_CONFIG.HEADERS,
      body: JSON.stringify(payload)
    });
    
    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));
    
    // 4. Handle response
    await handlePredictionResponse(response, payload);
  } catch (error) {
    handleApiError(error, 'Prediction');
  } finally {
    clearInterval(progressInterval);
    setTimeout(() => {
      isLoading.value = false;
      progressWidth.value = 0;
    }, 1000);
  }
};

const handlePredictionResponse = async (response, payload) => {
  try {
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({ message: 'Server returned a non-JSON error.' }));
      throw new Error(errorBody.message || `API request failed with status ${response.status}`);
    }

    let responseBody = await response.json();
    console.log('API Response Body:', responseBody);

    // n8n may wrap the body in several layers. Unwrap array and `response.body` if present
    if (Array.isArray(responseBody) && responseBody.length > 0) {
      responseBody = responseBody[0];
    }

    // If the structure is { response: { body: { ... } } }
    if (responseBody && responseBody.response && responseBody.response.body) {
      responseBody = responseBody.response.body;
    }

    // The backend now sends `predicted_yield_per_ha`.
    if (!responseBody.predicted_yield_per_ha) {
      throw new Error('Incomplete prediction data received from the server.');
    }

    const result = {
      // Map new response fields to legacy names that the UI expects
      predicted_yield: parseFloat(responseBody.predicted_yield_per_ha),
      yield_unit: responseBody.yield_unit_per_ha || 'Tons/ha',
      predicted_yield_total: responseBody.predicted_yield_total,
      yield_unit_total: responseBody.yield_unit_total,
      confidence_level: (responseBody.confidence_percent ?? 0) / 100,
      confidence_rating: responseBody.confidence_rating,
      prediction_id: responseBody.prediction_id || `pred_${Date.now()}`,
      // Add other fields from response or payload as needed
      ...payload,
      ...responseBody,
    };

    if (isNaN(result.predicted_yield)) {
      throw new Error('Invalid prediction value received from the server.');
    }

    // Store the result in the ref
    predictionResult.value = result;

    progressWidth.value = 100;
    
    // Emit the complete event to the parent
    emit('prediction-complete', result);

    // Store the successful prediction
    storePrediction(result);

    // Show the Accuracy Feedback flow so the user can submit actual yield
    showActualYieldFlow.value = true;

  } catch (error) {
    console.error('Failed to handle prediction response:', error);
    handleApiError(error, 'PredictionResponse');
  }
};

const resetForm = () => {
  formData.commune = '';
  formData.cropName = '';
  formData.email = '';
  formData.farmSize = '';
  
  errors.commune = '';
  errors.cropName = '';
  errors.email = '';
  errors.farmSize = '';
  
  showActualYieldFlow.value = false;
  actualYield.harvested = null;
  actualYield.value = '';
  actualYield.unit = '';
  
  emit('form-reset');
};

// Click outside to close dropdowns
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    communeDropdownOpen.value = false
    cropDropdownOpen.value = false
  }
}

// --- Actual Yield Flow Logic ---
function checkShowActualYieldFlow() {
  cleanExpiredPredictions();
  const previousPrediction = localStorage.getItem('previous_prediction');
  if (previousPrediction) {
    try {
      const storedPrediction = JSON.parse(previousPrediction);
      const predictionDate = new Date(storedPrediction.prediction_date);
      const now = new Date();
      const daysSincePrediction = (now - predictionDate) / (1000 * 60 * 60 * 24);
      if (daysSincePrediction >= 30) {
        showActualYieldFlow.value = true;
      }
    } catch (error) {
      localStorage.removeItem('previous_prediction');
    }
  }
}

// --- Actual Yield Submission ---
const submitActualYield = async () => {
  if (actualYield.harvested === null) {
    alert('Please indicate whether the prediction was accurate');
    return;
  }

  if (!actualYield.harvested && (!actualYield.value || !actualYield.unit)) {
    alert('Please enter your actual yield value and unit');
    return;
  }

  if (!predictionResult.value) {
    alert('No prediction data found. Please make a prediction first.');
    return;
  }

  isLoading.value = true;
  const progressInterval = startProgressAnimation();

  try {
    // Build payload with value & unit sent separately
    let actualYieldValue, actualYieldUnit;
    if (actualYield.harvested) {
      actualYieldValue = predictionResult.value.predicted_yield_total || predictionResult.value.predicted_yield;
      actualYieldUnit = predictionResult.value.yield_unit_total || predictionResult.value.yield_unit;
    } else {
      actualYieldValue = actualYield.value;
      actualYieldUnit = actualYield.unit;
    }

    const payload = {
      crop_type: normalizeCrop(formData.cropName || predictionResult.value.crop_type),
      commune: normalizeCommune(formData.commune || predictionResult.value.town),
      farm_size: parseFloat(formData.farmSize || predictionResult.value.farm_size),
      actual_yield: actualYieldValue,
      unit: actualYieldUnit,
      prediction_accurate: !!actualYield.harvested,
      prediction_id: predictionResult.value.prediction_id
    };

    const response = await fetch(API_CONFIG.ACTUAL_YIELD_ENDPOINT, {
      method: 'POST',
      headers: API_CONFIG.HEADERS,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({ message: 'Server returned a non-JSON error.' }));
      throw new Error(errorBody.message || `Actual yield submission failed with status ${response.status}`);
    }

    alert('Thank you! Your actual yield data helps us improve future predictions for all farmers.');
    showActualYieldFlow.value = false;
    actualYield.value = '';
    actualYield.unit = '';
    localStorage.removeItem('previous_prediction');
    predictionResult.value = null;
    emit('form-reset');

  } catch (error) {
    console.error('Failed to submit actual yield:', error);
    handleApiError(error, 'ActualYieldSubmission');
  } finally {
    clearInterval(progressInterval);
    setTimeout(() => {
      isLoading.value = false;
      progressWidth.value = 0;
    }, 1000);
  }
};

// Lifecycle
onMounted(() => {
  filteredCommunes.value = communes.slice(0, 20)
  filteredCrops.value = crops.slice(0, 20)
  document.addEventListener('click', handleClickOutside)
  checkShowActualYieldFlow()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Expose methods to parent component
defineExpose({
  resetForm
})
</script>

<style scoped>
.is-open .absolute.right-6 {
  transform: translateY(-50%) rotate(180deg);
}
</style> 