<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4 sm:p-8 relative overflow-hidden">
    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl animate-pulse-gentle"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-green-500/10 rounded-full blur-3xl animate-pulse-gentle" style="animation-delay: 2s;"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-lime-500/5 rounded-full blur-3xl animate-pulse-gentle" style="animation-delay: 4s;"></div>
    </div>

    <!-- Main Dashboard Container -->
    <div class="container-dashboard w-full flex-1 flex flex-col items-center justify-center relative z-10">
      
      <!-- Header Section -->
      <header class="text-center mb-8 animate-slide-up">
        <div class="flex items-center justify-center gap-4 mb-4">
          <div class="w-16 h-16 bg-gradient-to-br from-emerald-500 to-green-500 rounded-2xl flex items-center justify-center shadow-2xl animate-bounce-gentle">
            <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              <path d="M19 15L19.5 17L22 17.5L19.5 18L19 20L18.5 18L16 17.5L18.5 17L19 15Z" fill="currentColor"/>
              <path d="M5 15L5.5 17L8 17.5L5.5 18L5 20L4.5 18L2 17.5L4.5 17L5 15Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold gradient-text">
            EcoSystem<span class="text-emerald-600">+</span>
          </h1>
        </div>
        <p class="text-lg sm:text-xl text-gray-600 font-medium max-w-2xl mx-auto leading-relaxed mb-4">
          Next-generation AI-powered agricultural yield prediction platform
        </p>
        <div class="inline-flex items-center gap-2 bg-emerald-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>360+ Communes • 50+ Crops</span>
        </div>
      </header>

      <!-- Prediction Results Card (if exists) - NOW AT THE TOP -->
      <transition
        enter-active-class="transition-all duration-700 ease-out"
        enter-from-class="opacity-0 transform translate-y-12 scale-95"
        enter-to-class="opacity-100 transform translate-y-0 scale-100"
        leave-active-class="transition-all duration-500 ease-in"
        leave-from-class="opacity-100 transform translate-y-0 scale-100"
        leave-to-class="opacity-0 transform translate-y-12 scale-95"
      >
        <div v-if="predictionResult" class="w-full mb-8 animate-scale-in">
          <div class="mb-8 bg-gradient-to-r from-emerald-500/10 to-green-500/10 backdrop-blur-lg p-6 rounded-3xl border border-emerald-200 animate-fade-in">
            <!-- Header -->
            <div class="flex items-center gap-3 mb-4">
              <svg class="w-8 h-8 text-emerald-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h3 class="text-2xl font-bold text-emerald-800">Prediction Results</h3>
              <div class="ml-auto text-sm text-emerald-600">
                ID: {{ predictionResult.prediction_id }}
              </div>
            </div>
            
            <!-- Main Metrics Grid - 2x2 Layout -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <!-- Primary Yield Result -->
              <div class="bg-white/70 rounded-2xl p-4 border border-emerald-200">
                <p class="text-sm text-gray-600 mb-1">Estimated Yield / Hectare</p>
                <p class="text-3xl font-bold text-emerald-700">
                  {{ (predictionResult.predicted_yield).toLocaleString() }} 
                  <span class="text-lg ml-1">{{ predictionResult.yield_unit || 't/ha' }}</span>
                </p>
                <p v-if="predictionResult.predicted_yield_total" class="text-xs text-gray-500 mt-1">
                  Total Forecast: <strong>{{ predictionResult.predicted_yield_total }} {{ predictionResult.yield_unit_total || 'Tons' }}</strong>
                </p>
                <p v-if="predictionResult.confidence_level" class="text-xs text-emerald-600 mt-1">
                  {{ Math.round((predictionResult.confidence_level || 0.8) * 100) }}% confidence
                </p>
              </div>
              
              <!-- Crop Information -->
              <div class="bg-white/70 rounded-2xl p-4 border border-emerald-200">
                <p class="text-sm text-gray-600 mb-1">Crop Type</p>
                <p class="text-xl font-semibold text-gray-800">
                  {{ formatCropName(predictionResult.crop_type || predictionResult.formData?.cropName) }}
                </p>
                <p class="text-sm text-gray-500 mt-1">
                  {{ predictionResult.farm_size || predictionResult.formData?.farmSize }} hectares
                </p>
              </div>
              
              <!-- Location -->
              <div class="bg-white/70 rounded-2xl p-4 border border-emerald-200">
                <p class="text-sm text-gray-600 mb-1">Location</p>
                <p class="text-xl font-semibold text-gray-800">
                  {{ formatTownName(predictionResult.town || predictionResult.formData?.commune) }}
                </p>
              </div>
              
              <!-- Prediction Date -->
              <div class="bg-white/70 rounded-2xl p-4 border border-emerald-200">
                <p class="text-sm text-gray-600 mb-1">Prediction Date</p>
                <p class="text-xl font-semibold text-gray-800">
                  {{ formatDate(predictionResult.prediction_date || predictionResult.timestamp || new Date()) }}
                </p>
              </div>
            </div>
            
            <!-- Additional Information - Expandable -->
            <div v-if="predictionResult.factors || predictionResult.recommendations" class="border-t border-emerald-200 pt-4">
              <button 
                @click="showDetails = !showDetails"
                class="flex items-center gap-2 text-emerald-700 font-medium mb-3"
              >
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13 16H12V12H11M12 4H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                View Analysis Details
                <svg class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': showDetails }" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="opacity-0 transform -translate-y-4"
                enter-to-class="opacity-100 transform translate-y-0"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="opacity-100 transform translate-y-0"
                leave-to-class="opacity-0 transform -translate-y-4"
              >
                <div v-if="showDetails" class="space-y-4 animate-fade-in">
                  <!-- Factors -->
                  <div v-if="predictionResult.factors && predictionResult.factors.length > 0">
                    <h4 class="font-semibold text-gray-800 mb-2">Key Factors</h4>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      <div v-for="(factor, index) in predictionResult.factors" :key="index" class="bg-emerald-50 rounded-lg p-3">
                        <div class="flex justify-between items-center">
                          <span class="font-medium text-gray-800">{{ typeof factor === 'string' ? factor : factor.name }}</span>
                          <span v-if="factor.impact" class="text-sm px-2 py-1 rounded" :class="{
                            'bg-green-200 text-green-800': factor.impact === 'Positive',
                            'bg-red-200 text-red-800': factor.impact === 'Negative',
                            'bg-gray-200 text-gray-800': !['Positive', 'Negative'].includes(factor.impact)
                          }">
                            {{ factor.impact }}
                          </span>
                        </div>
                        <p v-if="factor.value" class="text-sm text-gray-600 mt-1">{{ factor.value }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Recommendations -->
                  <div v-if="predictionResult.recommendations && predictionResult.recommendations.length > 0">
                    <h4 class="font-semibold text-gray-800 mb-2">Recommendations</h4>
                    <ul class="space-y-2">
                      <li v-for="(rec, index) in predictionResult.recommendations" :key="index" class="flex items-start gap-2">
                        <svg class="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="text-gray-700">{{ rec }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Email Notification -->
            <div class="bg-emerald-50/80 border border-emerald-200 rounded-2xl p-4 mt-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-emerald-500/20 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-emerald-600" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 8L10.89 13.26C11.2187 13.4793 11.6049 13.5963 12 13.5963C12.3951 13.5963 12.7813 13.4793 13.11 13.26L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p class="text-gray-700 text-sm sm:text-base">
                  Full prediction report has been sent to <strong class="text-emerald-600">{{ predictionResult.contact || predictionResult.formData?.email }}</strong>
                </p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-3 mt-6">
              <button @click="resetForm" class="px-6 py-3 bg-emerald-600 text-white font-semibold rounded-2xl transition-all duration-300 hover:bg-emerald-700 hover:scale-105 flex items-center gap-3 justify-center group">
                <svg class="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 4V10H7M23 20V14H17M20.49 9A9 9 0 0 0 5.64 5.64L1 10M23 14L18.36 18.36A9 9 0 0 1 3.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>New Prediction</span>
              </button>
              
              <button @click="downloadReport" class="px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-2xl transition-all duration-300 hover:bg-gray-200 hover:scale-105 flex items-center gap-3 justify-center group">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M7 10L12 15M12 15L17 10M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Download Report</span>
              </button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Main Form Card (also hosts Actual Yield Feedback) -->
      <main class="w-full flex-1 flex items-center justify-center relative z-10 animate-fade-in">
        <YieldPredictionForm 
          @prediction-complete="handlePredictionComplete"
          @form-reset="handleFormReset"
          ref="formComponent"
        />
      </main>

      <!-- Footer Info Card -->
      <footer class="text-center mt-8 animate-slide-up">
        <div class="glass-card-light p-6">
          <div class="flex items-center justify-center gap-3 mb-2">
            <div class="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              </svg>
            </div>
            <h3 class="text-lg font-bold text-emerald-700">ECOSYSTEM +</h3>
          </div>
          <p class="text-sm text-gray-500">Empowering sustainable agriculture through advanced technology</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YieldPredictionForm from './components/YieldPredictionForm.vue'

// Reactive data
const predictionResult = ref(null)
const formData = ref({})
const formComponent = ref(null)
const showDetails = ref(false)

// Methods
const handlePredictionComplete = (result) => {
  console.log('Prediction complete event received:', result)
  predictionResult.value = result
  formData.value = result.formData || {}
  showDetails.value = false // Reset details view
}

const handleFormReset = () => {
  predictionResult.value = null
  formData.value = {}
  showDetails.value = false
}

const resetForm = () => {
  predictionResult.value = null
  formData.value = {}
  showDetails.value = false
  if (formComponent.value) {
    formComponent.value.resetForm()
  }
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatCropName = (cropName) => {
  if (!cropName) return 'Unknown Crop'
  // Convert from normalized format back to readable format
  return cropName
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const formatTownName = (townName) => {
  if (!townName) return 'Unknown Location'
  // Convert from normalized format back to readable format
  return townName
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const downloadReport = () => {
  if (!predictionResult.value) return
  
  // Create a simple text report
  const report = `
ECOSYSTEM+ Yield Prediction Report
=====================================

Prediction ID: ${predictionResult.value.prediction_id}
Date: ${formatDate(predictionResult.value.prediction_date || new Date())}

PREDICTION RESULTS:
- Predicted Yield: ${predictionResult.value.predicted_yield} ${predictionResult.value.yield_unit}
- Confidence Level: ${Math.round((predictionResult.value.confidence_level || 0.8) * 100)}%
- Crop Type: ${formatCropName(predictionResult.value.crop_type)}
- Location: ${formatTownName(predictionResult.value.town)}
- Farm Size: ${predictionResult.value.farm_size} hectares

${predictionResult.value.factors && predictionResult.value.factors.length > 0 ? `
KEY FACTORS:
${predictionResult.value.factors.map(factor => `- ${typeof factor === 'string' ? factor : factor.name}`).join('\n')}
` : ''}

${predictionResult.value.recommendations && predictionResult.value.recommendations.length > 0 ? `
RECOMMENDATIONS:
${predictionResult.value.recommendations.map(rec => `- ${rec}`).join('\n')}
` : ''}

Generated by EcoSystem+ AI Platform
  `.trim()
  
  // Create and download the file
  const blob = new Blob([report], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `yield-prediction-${predictionResult.value.prediction_id}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  gap: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 1rem;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.logo-icon {
  width: 3rem;
  height: 3rem;
  color: var(--primary-green);
  animation: leaf-spin 4s ease-in-out infinite;
}

.logo-text {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.text-accent {
  color: var(--accent-yellow);
  font-weight: 800;
}

.tagline {
  font-size: 1.125rem;
  color: var(--gray-600);
  font-weight: 400;
  margin: 0;
}

.main-content {
  width: 100%;
  max-width: 600px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer {
  text-align: center;
  color: var(--gray-500);
  font-size: 0.875rem;
  margin-top: 2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .app-container {
    padding: 1rem 0.5rem;
    gap: 1.5rem;
  }

  .logo-text {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1rem;
  }

  .main-content {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .logo-text {
    font-size: 1.75rem;
  }

  .logo-icon {
    width: 2.5rem;
    height: 2.5rem;
  }
}
</style> 