<template>
  <section class="relative py-20 bg-gradient-to-b from-[hsl(var(--light-gray))]/30 to-white">
    <!-- Background -->
    <div class="absolute inset-0 opacity-10">
      <img 
        src="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&h=1080" 
        alt="Peaceful agricultural landscape with crops swaying gently in the morning breeze" 
        class="w-full h-full object-cover" 
      />
    </div>
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-[hsl(var(--forest-green))] mb-6 animate-fade-in">
          Plans for Every Farmer's Future
        </h2>
        <p class="text-xl text-black max-w-3xl mx-auto animate-fade-in">
          Choose the perfect plan to transform your agricultural operations with cutting-edge satellite technology
        </p>
      </div>
      <!-- Pricing Cards -->
      <div class="grid md:grid-cols-3 gap-8 mb-16">
        <PricingCard
          v-for="(plan, index) in PRICING_PLANS"
          :key="plan.id"
          :plan="plan"
        />
      </div>
      <!-- FAQ Section -->
      <div class="max-w-4xl mx-auto">
        <h3 class="text-3xl font-bold text-[hsl(var(--forest-green))] text-center mb-12">
          Frequently Asked Questions
        </h3>
        <Accordion type="single" collapsible class="space-y-4">
          <AccordionItem
            v-for="(item, index) in FAQ_ITEMS"
            :key="index"
            :value="`item-${index}`"
            class="glassmorphism rounded-2xl overflow-hidden shadow-lg"
          >
            <AccordionTrigger class="px-8 py-6 text-left hover:bg-[hsl(var(--light-gray))]/30 transition-colors duration-200">
              <span class="font-semibold text-[hsl(var(--forest-green))]">{{ item.question }}</span>
            </AccordionTrigger>
            <AccordionContent class="px-8 pb-6">
              <p class="text-black leading-relaxed">{{ item.answer }}</p>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import PricingCard from './PricingCard.vue';
import { PRICING_PLANS, FAQ_ITEMS } from '../constants/modules';
import Accordion from '../components/ui/Accordion.vue';
import AccordionItem from '../components/ui/AccordionItem.vue';
import AccordionTrigger from '../components/ui/AccordionTrigger.vue';
import AccordionContent from '../components/ui/AccordionContent.vue';
</script>
