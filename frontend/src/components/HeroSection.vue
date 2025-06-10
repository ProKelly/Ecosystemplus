<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- 4K Motion Background -->
    <div class="absolute inset-0 z-0">
      <img 
        src="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=3840&h=2160" 
        alt="Aerial view of sustainable farming fields with satellite monitoring technology" 
        class="w-full h-full object-cover animate-float" 
      />
      <div class="absolute inset-0 hero-gradient"></div>
    </div>
    <!-- Hero Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="space-y-8">
        <!-- Headline with letter-by-letter reveal -->
        <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold text-[hsl(var(--forest-green))] leading-tight">
          <div class="mb-4">
            <LetterReveal text="Grow Smarter," :delay="0.1" />
          </div>
          <div>
            <LetterReveal text="Sustain Longer" :delay="0.75" />
          </div>
        </h1>
        <!-- Subheading -->
        <p 
          :class="['text-xl md:text-2xl lg:text-3xl text-black font-medium max-w-4xl mx-auto opacity-0', animationClass]"
          style="animation-delay: 1.8s"
        >
          Revolutionize farming with AI, satellites, and real-time insights
        </p>
        <!-- CTA Buttons -->
        <div 
          :class="['flex flex-col sm:flex-row gap-6 justify-center items-center opacity-0', animationClass]"
          style="animation-delay: 2.2s"
        >
          <router-link to="/pricing">
            <button 
              class="bg-[hsl(var(--bright-yellow))] text-black px-8 py-4 rounded-full text-lg font-bold hover:scale-105 hover:shadow-xl transition-all duration-300 animate-scale-pulse animate-glow flex items-center"
            >
              <span class="mr-2">🚀</span>
              Discover EcoSystem+
            </button>
          </router-link>
          <a href="#demo" class="text-[hsl(var(--forest-green))] text-lg font-semibold hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 relative group flex items-center">
            <span class="inline mr-2">▶</span>
            Watch Demo
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-[hsl(var(--bright-yellow))] transition-all duration-300 group-hover:w-full"></span>
          </a>
        </div>
      </div>
    </div>
    <!-- Scroll Indicator -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
      <span class="text-[hsl(var(--forest-green))] w-8 h-8 text-4xl">▼</span>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const animationClass = ref('')
onMounted(() => {
  animationClass.value = 'animate-fade-in'
})
// LetterReveal as a local component
const LetterReveal = defineComponent({
  name: 'LetterReveal',
  props: {
    text: { type: String, required: true },
    delay: { type: Number, default: 0 },
  },
  setup(props) {
    return () => props.text.split('').map((char, index) =>
      h('span', {
        class: 'inline-block animate-letter-reveal',
        style: { animationDelay: `${props.delay + index * 0.05}s` },
      }, char === ' ' ? '\u00A0' : char)
    )
  }
})
</script>

<style scoped>
/* Add your styles here or use Tailwind CSS as in the original */
</style>
