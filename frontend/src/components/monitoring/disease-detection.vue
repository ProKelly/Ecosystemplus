<template>
  <section class="bg-white py-10 px-6 md:px-16 lg:px-24 text-gray-800 m shadow-md">
    <h2 class="text-2xl md:text-3xl font-bold text-green-700 mb-6">Crop Disease Detection</h2>

    <!-- Toggle Button -->
    <div class="text-center mb-4 bg-green-50">
      <button
        @click="showTutorial = !showTutorial"
        class="text-green-700 font-semibold underline hover:text-green-900 transition p-2"
      >
        View Tutorial (Highly recommended for accurate results)
      </button>
    </div>

    <!-- Video Tutorial Section with Transition -->
    <transition name="slide-fade">
      <div v-if="showTutorial" class="mb-10 flex justify-center bg-green-50 rounded-border">
        <div class="w-full max-w-3xl">
          <video controls class="w-full rounded shadow block mb-2">
            <source src="@/assets/video/monitoring-tutorial.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <p class="text-center text-sm text-gray-600 mb-6">
            Watch this short tutorial to learn how to snap accurate crop images for detection.
          </p>
        </div>
      </div>
    </transition>

    <!-- Step-by-Step Form -->
    <div class="grid grid-cols-1 gap-10 items-start">
      <!-- Input Form -->
      <div>
        <label for="crop" class="block mb-2 font-semibold">Select Crop</label>
        <select v-model="selectedCrop" id="crop" class="p-2 rounded border w-full mb-4">
          <option disabled value="">Choose a crop</option>
          <option v-for="(diseases, crop) in cropDiseaseData" :key="crop" :value="crop">
            {{ crop }}
          </option>
        </select>

        <label for="image-upload" class="block mb-2 font-semibold">Upload Image</label>
        <label
          for="image-upload"
          class="inline-block bg-green-600 hover:bg-green-700 text-white text-sm px-4 py-2 rounded cursor-pointer transition duration-300"
        >
          Choose or Snap Image
        </label>
        <input
          id="image-upload"
          type="file"
          accept="image/*"
          capture="environment"
          @change="handleImageUpload"
          class="hidden"
        />
      </div>
      <!-- Image & Result Card -->
      <div class="flex items-center justify-center">
        <div
          v-if="previewImage"
          class="bg-green-50 rounded-lg shadow px-6 pt-6 pb-4 mx-auto"
          style="min-width: 280px"
        >
          <!-- Image Section -->
          <div class="flex justify-center">
            <div class="bg-white border-2 border-green-500 rounded-md shadow-inner">
              <div class="w-64 h-64 overflow-hidden rounded">
                <img :src="previewImage" alt="Preview" class="w-full h-full object-cover" />
              </div>
            </div>
          </div>

          <!-- Result Section -->
          <div
            v-if="result"
            class="border border-green-600 rounded-md p-4 text-left mt-4"
            style="margin-top: 1rem"
          >
            <h3 class="text-lg font-semibold text-green-700 mb-2 text-center">Detection Result</h3>
            <p class="mb-1 text-red-600 font-semibold">
              <strong>Disease:</strong> {{ result.disease }}
            </p>
            <p class="font-bold"><strong>Treatment:</strong> {{ result.solution }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const selectedCrop = ref('')
const previewImage = ref(null)
const result = ref(null)
const showTutorial = ref(false)
const cropDiseaseData = {
  Maize: [
    {
      disease: 'Maize Streak Virus',
      solution: 'Use resistant varieties and control vectors with insecticides.',
    },
    {
      disease: 'Leaf Blight',
      solution: 'Apply fungicides and ensure good air circulation.',
    },
  ],
  Tomato: [
    {
      disease: 'Early Blight',
      solution: 'Remove affected leaves and use copper-based fungicide.',
    },
    {
      disease: 'Late Blight',
      solution: 'Spray with appropriate fungicide and avoid overhead irrigation.',
    },
  ],
  Cassava: [
    {
      disease: 'Cassava Mosaic Disease',
      solution: 'Use virus-free planting materials and control whiteflies.',
    },
    {
      disease: 'Bacterial Blight',
      solution: 'Apply bactericides and practice crop rotation.',
    },
  ],
}

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    previewImage.value = URL.createObjectURL(file)

    // Simulate detection
    setTimeout(() => {
      if (selectedCrop.value) {
        const diseases = cropDiseaseData[selectedCrop.value]
        const random = diseases[Math.floor(Math.random() * diseases.length)]
        result.value = random
      }
    }, 1000)
  }
}
</script>
<style>
.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
