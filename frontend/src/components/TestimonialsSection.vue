<script setup lang="ts">
import { TESTIMONIALS } from '@/constants/modules' // Adjust path if needed
const testimonials = TESTIMONIALS
</script>

<template>
  <section class="relative py-20 bg-gradient-to-b from-white to-[hsl(var(--light-gray))]/30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-[hsl(var(--forest-green))] mb-6">
          Transforming Lives Across Africa
        </h2>
        <p class="text-xl text-black max-w-3xl mx-auto">
          Real stories from farmers and organizations using EcoSystem+ to revolutionize agriculture
        </p>
      </div>
      <!-- Testimonials Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="(testimonial, index) in testimonials" :key="index" class="glassmorphism rounded-3xl p-8 shadow-xl hover:shadow-2xl hover:-translate-y-2 transition-all duration-300">
          <div class="flex items-center mb-6">
            <img 
              :src="testimonial.image" 
              :alt="`${testimonial.name}, ${testimonial.role}`" 
              class="w-16 h-16 rounded-full object-cover mr-4" 
            />
            <div>
              <h4 class="font-bold text-[hsl(var(--forest-green))]">{{ testimonial.name }}</h4>
              <p class="text-gray-600 text-sm">{{ testimonial.role }}</p>
            </div>
          </div>
          <p class="text-black leading-relaxed mb-4">
            "{{ testimonial.quote }}"
          </p>
          <div class="flex text-[hsl(var(--bright-yellow))]">
            <span v-for="star in testimonial.rating" :key="star + '-' + index" class="w-5 h-5">★</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.testimonials-section {
  padding: 2rem 0;
  background: #fff;
  text-align: center;
}
.testimonials {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
}
blockquote {
  background: #f8f9fa;
  border-left: 4px solid #00bcd4;
  padding: 1rem 2rem;
  border-radius: 6px;
  font-style: italic;
}
span {
  display: block;
  margin-top: 0.5rem;
  color: #888;
}
</style>
