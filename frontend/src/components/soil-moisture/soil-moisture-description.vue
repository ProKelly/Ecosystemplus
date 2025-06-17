<template>
  <section
    class="min-h-screen bg-white px-6 md:px-16 lg:px-24 py-10 text-gray-800 flex items-center shadow-md"
  >
    <div class="w-full max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
      <!-- Text Section (Left on desktop) -->
      <div class="space-y-6 order-2 md:order-1">
        <h2 class="text-3xl md:text-4xl font-bold text-green-700 text-center md:text-left">
          {{ moduleInfo.name }}
        </h2>

        <p class="text-lg leading-relaxed text-center md:text-left">
          {{ moduleInfo.mainDescription }}
        </p>

        <!-- Details Section -->
        <transition name="fade-slide">
          <div
            v-if="isDesktop || showDetails"
            class="bg-green-50 p-4 rounded-lg shadow-inner transition-all duration-300"
          >
            <ul class="list-disc list-inside space-y-3 text-left text-green-800">
              <li v-for="(detail, index) in moduleInfo.descriptionDetails" :key="index">
                {{ detail }}
              </li>
            </ul>
          </div>
        </transition>

        <!-- See More Button (Mobile only) -->
        <div v-if="!isDesktop" class="text-center">
          <button
            @click="toggleDetails"
            class="mt-4 text-green-700 font-semibold underline focus:outline-none"
          >
            {{ showDetails ? 'See Less' : 'See More' }}
          </button>
        </div>

        <p class="text-md text-gray-600 text-center md:text-left">
          Empower your farm with intelligent monitoring and proactive decision-making.
        </p>
      </div>

      <!-- Image Section (Right on desktop) -->
      <div class="order-1 md:order-2 space-y-4 flex flex-col items-center">
        <img
          src="@/assets/images/soil-analysis/soil-analysis.png"
          alt="Drone monitoring crops from above"
          class="w-full h-auto rounded-xl shadow-lg object-cover max-h-[400px]"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const moduleInfo = {
  name: 'Soil Moisture Analysis',
  mainDescription:
    'This module optimizes irrigation management by measuring soil moisture at various depths and  providing tailored recommendations',
  descriptionDetails: [
    'Provides graphs showing the water moisture distribution over selected periods of time ',
    'Emergency Notifications: Instantly notifies users of water threats to crops.',
    'Smart Recommendations: Recommends farmers the periods when irrigation practices should be intensified.',
    'Disease Detection: Displays tables showing previous and forecasts of dry periods.',
  ],
}

const showDetails = ref(false)
const isDesktop = ref(window.innerWidth >= 768)

const handleResize = () => {
  isDesktop.value = window.innerWidth >= 768
  if (isDesktop.value) showDetails.value = true
  else showDetails.value = false
}

const toggleDetails = () => {
  showDetails.value = !showDetails.value
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
