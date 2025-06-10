<template>
  <Card 
    :class="[
      'glassmorphism rounded-3xl p-8 shadow-xl hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 relative',
      plan.popular ? 'border-2 border-[hsl(var(--bright-yellow))]/50' : 'hover:border-2 hover:border-[hsl(var(--bright-yellow))]/50'
    ]"
  >
    <div v-if="plan.popular" class="absolute -top-4 left-1/2 transform -translate-x-1/2">
      <Badge class="bg-[hsl(var(--bright-yellow))] text-black px-4 py-2 rounded-full text-sm font-bold">
        Most Popular
      </Badge>
    </div>
    <div class="text-center mb-8">
      <div :class="[
        'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4',
        plan.popular ? 'bg-[hsl(var(--bright-yellow))]/20' : 'bg-[hsl(var(--forest-green))]/10'
      ]">
        <span class="text-2xl">{{ plan.icon }}</span>
      </div>
      <h3 class="text-2xl font-bold text-[hsl(var(--forest-green))] mb-2">{{ plan.name }}</h3>
      <p class="text-gray-600 mb-4">{{ plan.description }}</p>
      <div class="text-4xl font-bold text-black mb-2">{{ plan.price }}</div>
      <div class="text-gray-500">{{ plan.period }}</div>
    </div>
    <div class="space-y-4 mb-8">
      <div v-for="(feature, featureIndex) in plan.features" :key="featureIndex" class="flex items-center">
        <CheckIcon :class="['mr-3 h-5 w-5', plan.popular ? 'text-[hsl(var(--bright-yellow))]' : 'text-[hsl(var(--forest-green))]']" />
        <span class="text-black">{{ feature }}</span>
      </div>
    </div>
    <router-link v-if="plan.id === 'enterprise'" to="/contact">
      <Button class="w-full bg-[hsl(var(--forest-green))] text-white py-4 rounded-full font-bold hover:scale-105 hover:shadow-lg transition-all duration-300">
        {{ plan.cta }}
      </Button>
    </router-link>
    <Button
      v-else
      :class="[
        'w-full py-4 rounded-full font-bold hover:scale-105 hover:shadow-lg transition-all duration-300',
        plan.popular ? 'bg-[hsl(var(--bright-yellow))] text-black animate-scale-pulse' : 'bg-[hsl(var(--bright-yellow))] text-black'
      ]"
    >
      {{ plan.cta }}
    </Button>
  </Card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import Card from '../components/ui/Card.vue';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';
import CheckIcon from '../components/icons/CheckIcon.vue';

defineProps<{ plan: any }>();
</script>
