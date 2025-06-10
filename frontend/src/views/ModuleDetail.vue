<template>
  <div class="min-h-screen bg-white">
    <Navigation />
    <div v-if="!module" class="pt-24 pb-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl font-bold text-[hsl(var(--forest-green))] mb-4">Module Not Found</h1>
        <p class="text-xl text-gray-600 mb-8">The module you're looking for doesn't exist.</p>
        <RouterLink to="/">
          <Button class="bg-[hsl(var(--bright-yellow))] text-black hover:scale-105 transition-all duration-300">
            <span class="mr-2">➡️</span>
            Back to Home
          </Button>
        </RouterLink>
      </div>
      <Footer />
    </div>
    <template v-else>
      <!-- Hero Section -->
      <section class="relative pt-24 pb-20 overflow-hidden">
        <div class="absolute inset-0 z-0">
          <img :src="module.image" :alt="`${module.title} satellite imagery background`" class="w-full h-full object-cover animate-float" />
          <div class="absolute inset-0 hero-gradient"></div>
        </div>
        <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div class="space-y-6">
            <Badge class="bg-[hsl(var(--bright-yellow))] text-black px-4 py-2 text-lg">
              <span class="mr-2 text-xl">{{ module.icon }}</span>
              Agricultural Technology
            </Badge>
            <h1 class="text-4xl md:text-6xl font-bold text-[hsl(var(--forest-green))] leading-tight">{{ module.title }}</h1>
            <p class="text-xl md:text-2xl text-black font-medium max-w-3xl mx-auto">{{ module.description }}</p>
          </div>
        </div>
      </section>
      <!-- Overview Section -->
      <section class="py-20 bg-gradient-to-b from-white to-[hsl(var(--light-gray))]/30">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card class="glassmorphism rounded-3xl p-8 shadow-xl">
            <h2 class="text-3xl font-bold text-[hsl(var(--forest-green))] mb-6">How It Works</h2>
            <p class="text-lg text-black leading-relaxed">
              {{ module.title }} leverages cutting-edge Sentinel satellite technology to provide farmers with unprecedented insights into their agricultural operations.
              Using advanced machine learning algorithms and real-time data processing, our platform delivers actionable intelligence that helps optimize farming practices,
              increase yields, and promote sustainable agriculture across Africa.
            </p>
          </Card>
        </div>
      </section>
      <!-- Feature Highlights -->
      <section class="py-20">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 class="text-3xl font-bold text-[hsl(var(--forest-green))] text-center mb-12">Key Features</h2>
          <div class="grid md:grid-cols-2 gap-8">
            <Card v-for="(feature, index) in module.features" :key="index" class="glassmorphism rounded-2xl p-6 shadow-lg hover:shadow-xl hover:-translate-y-2 transition-all duration-300 group">
              <div class="flex items-start space-x-4">
                <div class="w-10 h-10 bg-[hsl(var(--forest-green))]/10 rounded-full flex items-center justify-center flex-shrink-0 group-hover:bg-[hsl(var(--bright-yellow))]/20 transition-colors duration-300">
                  <span class="text-[hsl(var(--forest-green))] h-5 w-5 group-hover:text-[hsl(var(--bright-yellow))] transition-colors duration-300">✔️</span>
                </div>
                <div>
                  <h3 class="font-semibold text-[hsl(var(--forest-green))] mb-2 group-hover:text-[hsl(var(--bright-yellow))] transition-colors duration-300">{{ feature }}</h3>
                  <p class="text-gray-600 text-sm">
                    Advanced satellite-based monitoring using Sentinel data for precision agriculture insights.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>
      <!-- Use Case Scenario -->
      <section class="py-20 bg-gradient-to-b from-[hsl(var(--light-gray))]/30 to-white">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card class="glassmorphism rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 border-2 border-[hsl(var(--bright-yellow))]/20 hover:border-[hsl(var(--bright-yellow))]/50">
            <div class="flex items-start space-x-4 mb-6">
              <div class="w-12 h-12 bg-[hsl(var(--bright-yellow))]/20 rounded-full flex items-center justify-center flex-shrink-0">
                <span class="text-[hsl(var(--bright-yellow))] h-6 w-6">⚡</span>
              </div>
              <div>
                <h2 class="text-3xl font-bold text-[hsl(var(--forest-green))] mb-4">Real-World Impact</h2>
                <p class="text-lg text-black leading-relaxed">
                  Discover how a {{ module.title.toLowerCase() }} implementation helped a cooperative of 200 smallholder farmers in Ghana increase their crop yields by 35%
                  while reducing water usage by 20%. Through satellite-powered insights and AI-driven recommendations, farmers gained unprecedented visibility into their
                  fields, enabling data-driven decisions that transformed their agricultural practices and improved livelihoods across the entire community.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </section>
      <!-- Data Visualization Preview -->
      <section class="py-20">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-[hsl(var(--forest-green))] mb-4">Advanced Visualizations</h2>
            <p class="text-lg text-gray-600">Interactive satellite data analysis powered by Sentinel imagery</p>
          </div>
          <Card class="glassmorphism rounded-3xl p-8 shadow-xl">
            <div class="aspect-video bg-gradient-to-br from-[hsl(var(--forest-green))]/10 to-[hsl(var(--bright-yellow))]/10 rounded-2xl flex items-center justify-center">
              <div class="text-center">
                <div class="w-16 h-16 bg-[hsl(var(--forest-green))]/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span class="text-3xl">{{ module.icon }}</span>
                </div>
                <h3 class="text-xl font-semibold text-[hsl(var(--forest-green))] mb-2">Interactive {{ module.title }} Dashboard</h3>
                <p class="text-gray-600">Real-time satellite data visualization coming soon</p>
              </div>
            </div>
          </Card>
        </div>
      </section>
      <!-- CTA Section -->
      <section class="py-20 bg-gradient-to-b from-white to-[hsl(var(--light-gray))]/30">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-3xl font-bold text-[hsl(var(--forest-green))] mb-6">Ready to Get Started?</h2>
          <p class="text-lg text-gray-600 mb-8">
            Transform your agricultural operations with {{ module.title }} and join thousands of farmers already benefiting from our satellite-powered insights.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <RouterLink to="/pricing">
              <Button size="lg" class="bg-[hsl(var(--bright-yellow))] text-black px-8 py-4 rounded-full text-lg font-bold hover:scale-105 hover:shadow-xl transition-all duration-300 animate-glow">
                <span class="mr-2">⚡</span>
                Try EcoSystem+
              </Button>
            </RouterLink>
            <RouterLink to="/contact">
              <Button variant="outline" size="lg" class="border-[hsl(var(--forest-green))] text-[hsl(var(--forest-green))] hover:bg-[hsl(var(--forest-green))] hover:text-white px-8 py-4 rounded-full text-lg font-bold hover:scale-105 transition-all duration-300">
                Contact Sales
              </Button>
            </RouterLink>
          </div>
        </div>
      </section>
      <Footer />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import Navigation from '../components/Navigation.vue';
import Footer from '../components/Footer.vue';
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import Badge from '../components/ui/Badge.vue';
import { MODULES } from '../constants/modules';

const route = useRoute();
const moduleId = computed(() => route.params.id);
const module = computed(() => MODULES.find(m => m.id === moduleId.value));
</script>
