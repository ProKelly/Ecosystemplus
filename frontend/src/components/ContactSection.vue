<template>
  <section class="relative py-20 bg-gradient-to-b from-[hsl(var(--light-gray))]/30 to-white">
    <div class="absolute inset-0 opacity-5">
      <img 
        src="https://images.unsplash.com/photo-1581092160562-40aa08e78837?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&h=1080" 
        alt="Modern agricultural technology center with satellite communication equipment" 
        class="w-full h-full object-cover" 
      />
    </div>
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-[hsl(var(--forest-green))] mb-6">
          Ready to Transform Your Farm?
        </h2>
        <p class="text-xl text-black max-w-3xl mx-auto">
          Get in touch with our experts and start your journey towards smarter, more sustainable farming
        </p>
      </div>
      <div class="grid lg:grid-cols-2 gap-12">
        <!-- Contact Form -->
        <div class="glassmorphism rounded-3xl p-8 shadow-xl">
          <h3 class="text-2xl font-bold text-[hsl(var(--forest-green))] mb-6">Send us a Message</h3>
          <form @submit="handleSubmit" class="space-y-6">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label for="firstName" class="text-black font-semibold mb-2 block">First Name</label>
                <input
                  id="firstName"
                  type="text"
                  placeholder="Enter your first name"
                  v-model="formData.firstName"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-[hsl(var(--forest-green))] focus:ring-2 focus:ring-[hsl(var(--forest-green))]/20 transition-colors duration-200"
                  required
                />
              </div>
              <div>
                <label for="lastName" class="text-black font-semibold mb-2 block">Last Name</label>
                <input
                  id="lastName"
                  type="text"
                  placeholder="Enter your last name"
                  v-model="formData.lastName"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-[hsl(var(--forest-green))] focus:ring-2 focus:ring-[hsl(var(--forest-green))]/20 transition-colors duration-200"
                  required
                />
              </div>
            </div>
            <div>
              <label for="email" class="text-black font-semibold mb-2 block">Email Address</label>
              <input
                id="email"
                type="email"
                placeholder="your.email@example.com"
                v-model="formData.email"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-[hsl(var(--forest-green))] focus:ring-2 focus:ring-[hsl(var(--forest-green))]/20 transition-colors duration-200"
                required
              />
            </div>
            <div>
              <label for="farmSize" class="text-black font-semibold mb-2 block">Farm Size (hectares)</label>
              <select
                id="farmSize"
                v-model="formData.farmSize"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-[hsl(var(--forest-green))] focus:ring-2 focus:ring-[hsl(var(--forest-green))]/20 transition-colors duration-200"
                required
              >
                <option value="" disabled>Select farm size</option>
                <option v-for="size in farmSizes" :key="size.value" :value="size.value">{{ size.label }}</option>
              </select>
            </div>
            <div>
              <label for="message" class="text-black font-semibold mb-2 block">Message</label>
              <textarea
                id="message"
                rows="4"
                placeholder="Tell us about your farming needs and how we can help..."
                v-model="formData.message"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:border-[hsl(var(--forest-green))] focus:ring-2 focus:ring-[hsl(var(--forest-green))]/20 transition-colors duration-200"
                required
              />
            </div>
            <button 
              type="submit" 
              :disabled="isSubmitting"
              class="w-full bg-[hsl(var(--bright-yellow))] text-black py-4 rounded-full font-bold hover:scale-105 hover:shadow-lg transition-all duration-300"
            >
              {{ isSubmitting ? 'Sending...' : 'Send Message' }}
            </button>
          </form>
        </div>
        <!-- Contact Information -->
        <div class="space-y-8">
          <div class="glassmorphism rounded-3xl p-8 shadow-xl">
            <h3 class="text-2xl font-bold text-[hsl(var(--forest-green))] mb-6">Get in Touch</h3>
            <div class="space-y-6">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-[hsl(var(--forest-green))]/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-[hsl(var(--forest-green))] h-5 w-5">📍</span>
                </div>
                <div>
                  <h4 class="font-semibold text-black mb-1">Office Location</h4>
                  <p class="text-gray-600">123 Agricultural Innovation Hub<br />Dakar, Senegal</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-[hsl(var(--forest-green))]/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-[hsl(var(--forest-green))] h-5 w-5">📞</span>
                </div>
                <div>
                  <h4 class="font-semibold text-black mb-1">Phone Number</h4>
                  <p class="text-gray-600">+221 33 123 4567</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-[hsl(var(--forest-green))]/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-[hsl(var(--forest-green))] h-5 w-5">✉️</span>
                </div>
                <div>
                  <h4 class="font-semibold text-black mb-1">Email Address</h4>
                  <p class="text-gray-600">contact@ecosystem-plus.com</p>
                </div>
              </div>
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-[hsl(var(--forest-green))]/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-[hsl(var(--forest-green))] h-5 w-5">⏰</span>
                </div>
                <div>
                  <h4 class="font-semibold text-black mb-1">Business Hours</h4>
                  <p class="text-gray-600">Monday - Friday: 8:00 AM - 6:00 PM<br />Saturday: 9:00 AM - 2:00 PM</p>
                </div>
              </div>
            </div>
          </div>
          <!-- Social Media -->
          <div class="glassmorphism rounded-3xl p-8 shadow-xl">
            <h3 class="text-2xl font-bold text-[hsl(var(--forest-green))] mb-6">Follow Us</h3>
            <div class="flex space-x-4">
              <a 
                href="#" 
                class="w-12 h-12 bg-[hsl(var(--forest-green))] rounded-full flex items-center justify-center text-white hover:bg-[hsl(var(--bright-yellow))] hover:text-black transition-all duration-300 hover:scale-110"
              >
                <span class="h-5 w-5">📘</span>
              </a>
              <a 
                href="#" 
                class="w-12 h-12 bg-[hsl(var(--forest-green))] rounded-full flex items-center justify-center text-white hover:bg-[hsl(var(--bright-yellow))] hover:text-black transition-all duration-300 hover:scale-110"
              >
                <span class="h-5 w-5">🐦</span>
              </a>
              <a 
                href="#" 
                class="w-12 h-12 bg-[hsl(var(--forest-green))] rounded-full flex items-center justify-center text-white hover:bg-[hsl(var(--bright-yellow))] hover:text-black transition-all duration-300 hover:scale-110"
              >
                <span class="h-5 w-5">💼</span>
              </a>
              <a 
                href="#" 
                class="w-12 h-12 bg-[hsl(var(--forest-green))] rounded-full flex items-center justify-center text-white hover:bg-[hsl(var(--bright-yellow))] hover:text-black transition-all duration-300 hover:scale-110"
              >
                <span class="h-5 w-5">📸</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const formData = ref({
  firstName: '',
  lastName: '',
  email: '',
  farmSize: '',
  message: ''
})
const isSubmitting = ref(false)
const farmSizes = [
  { value: 'less-than-1', label: 'Less than 1 hectare' },
  { value: '1-10', label: '1-10 hectares' },
  { value: '10-50', label: '10-50 hectares' },
  { value: '50-100', label: '50-100 hectares' },
  { value: 'more-than-100', label: 'More than 100 hectares' }
]
const handleSubmit = async (e: Event) => {
  e.preventDefault()
  isSubmitting.value = true
  // Simulate form submission
  await new Promise(resolve => setTimeout(resolve, 1000))
  alert("Message sent successfully! We'll get back to you within 24 hours.")
  formData.value = { firstName: '', lastName: '', email: '', farmSize: '', message: '' }
  isSubmitting.value = false
}
</script>

<style scoped>
.contact-section {
  padding: 2rem 0;
  background: #e0f7fa;
  text-align: center;
}
.contact-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  max-width: 400px;
  margin: 0 auto;
}
input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.75rem 2rem;
  background: #00bcd4;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background: #0097a7;
}
</style>
