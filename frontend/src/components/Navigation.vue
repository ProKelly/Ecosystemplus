<template>
  <nav :class="navClass">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-3 md:py-4">
        <!-- Logo -->
        <router-link to="/">
          <div class="flex items-center space-x-2 cursor-pointer group">
            <span :class="logoColor + ' text-2xl md:text-3xl group-hover:scale-110 transition-transform duration-200'">🌿</span>
            <span :class="'text-xl md:text-2xl font-bold ' + logoColor + ' font-inter group-hover:scale-105 transition-transform duration-200'">
              EcoSystem+
            </span>
          </div>
        </router-link>
        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center space-x-6 xl:space-x-8">
          <NavLink to="/">Home</NavLink>
          <div class="relative group">
            <button :class="textColor + ' hover:text-[hsl(var(--bright-yellow))] transition-colors duration-200 flex items-center font-medium'">
              Features
              <span class="ml-1 w-4 h-4 group-hover:rotate-180 transition-transform duration-200">▼</span>
            </button>
            <!-- Features Dropdown -->
            <div class="absolute top-full left-0 w-72 bg-white/95 backdrop-blur-lg rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 mt-2 border border-gray-200/20 overflow-hidden">
              <div class="p-2">
                <div class="grid grid-cols-1 gap-1">
                  <router-link v-for="module in modules" :key="module.id" :to="`/module/${module.id}`">
                    <div class="flex items-center py-3 px-4 text-sm text-black hover:text-[hsl(var(--forest-green))] hover:bg-[hsl(var(--light-gray))]/50 rounded-lg transition-all duration-200 cursor-pointer group/item">
                      <span class="mr-3 text-lg group-hover/item:scale-110 transition-transform duration-200">{{ module.icon }}</span>
                      <div>
                        <div class="font-semibold">{{ module.title }}</div>
                        <div class="text-xs text-gray-500 mt-0.5">Satellite-powered insights</div>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          <NavLink to="/pricing">Pricing</NavLink>
          <NavLink to="/contact">Contact</NavLink>
          <!-- CTA Button -->
          <router-link to="/pricing">
            <button class="bg-[hsl(var(--bright-yellow))] text-black px-6 py-2 rounded-full font-bold hover:scale-105 hover:shadow-lg transition-all duration-300 ml-4">
              Get Started
            </button>
          </router-link>
        </div>
        <!-- Mobile Menu (simplified for brevity) -->
        <button class="lg:hidden p-2" @click="isOpen = !isOpen">
          <span :class="'h-6 w-6 ' + textColor">☰</span>
        </button>
        <div v-if="isOpen" class="fixed inset-0 z-50 bg-white/98 backdrop-blur-lg border-l border-gray-200/20 flex flex-col">
          <div class="flex items-center justify-between py-4 border-b border-gray-200/20 px-4">
            <div class="flex items-center space-x-2">
              <span class="text-[hsl(var(--forest-green))] text-2xl">🌿</span>
              <span class="text-xl font-bold text-[hsl(var(--forest-green))]">EcoSystem+</span>
            </div>
            <button class="p-2" @click="isOpen = false">✕</button>
          </div>
          <div class="flex-1 overflow-y-auto py-6 space-y-6 px-4">
            <div class="space-y-4">
              <NavLink to="/" @click="isOpen = false">
                <div class="text-lg font-semibold py-2">Home</div>
              </NavLink>
              <div class="space-y-3">
                <div class="text-lg font-semibold text-[hsl(var(--forest-green))] py-2">Features</div>
                <div class="grid grid-cols-1 gap-2 pl-4">
                  <router-link v-for="module in modules" :key="module.id" :to="`/module/${module.id}`" @click="isOpen = false">
                    <div class="flex items-center py-3 px-4 text-black hover:text-[hsl(var(--bright-yellow))] hover:bg-[hsl(var(--light-gray))]/30 rounded-lg transition-all duration-200 cursor-pointer group">
                      <span class="mr-3 text-xl group-hover:scale-110 transition-transform duration-200">{{ module.icon }}</span>
                      <div>
                        <div class="font-medium">{{ module.title }}</div>
                        <div class="text-xs text-gray-500 mt-0.5">AI-powered analysis</div>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
              <NavLink to="/pricing" @click="isOpen = false">
                <div class="text-lg font-semibold py-2">Pricing</div>
              </NavLink>
              <NavLink to="/contact" @click="isOpen = false">
                <div class="text-lg font-semibold py-2">Contact</div>
              </NavLink>
            </div>
          </div>
          <div class="border-t border-gray-200/20 pt-6 pb-4 px-4">
            <router-link to="/pricing" @click="isOpen = false">
              <button class="w-full bg-[hsl(var(--bright-yellow))] text-black py-3 rounded-full font-bold hover:scale-105 transition-all duration-300">
                Get Started Today
              </button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, defineComponent, h } from 'vue'
import { useRoute } from 'vue-router'
import { MODULES } from '@/constants/modules'
const modules = MODULES
const isOpen = ref(false)
const isScrolled = ref(false)
const isVisible = ref(true)
const lastScrollY = ref(0)
const route = useRoute()
const textColor = computed(() => (isScrolled.value || route.path !== '/') ? 'text-black' : 'text-white')
const logoColor = computed(() => (isScrolled.value || route.path !== '/') ? 'text-[hsl(var(--forest-green))]' : 'text-white')
const navClass = computed(() => `fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isVisible.value ? 'translate-y-0' : '-translate-y-full'} ${isScrolled.value || route.path !== '/' ? 'bg-white/95 backdrop-blur-lg shadow-lg border-b border-gray-200/20' : 'bg-transparent'}`)

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})
function handleScroll() {
  const currentScrollY = window.scrollY
  if (currentScrollY > 100) {
    isScrolled.value = true
    if (currentScrollY > lastScrollY.value && currentScrollY > 200) {
      isVisible.value = false
    } else {
      isVisible.value = true
    }
  } else {
    isScrolled.value = false
    isVisible.value = true
  }
  lastScrollY.value = currentScrollY
}

// NavLink component
const NavLink = defineComponent({
  name: 'NavLink',
  props: {
    to: { type: String, required: true }
  },
  setup(props, { slots }) {
    return () => h('router-link', { to: props.to, class: 'relative group ' + textColor.value + ' hover:text-[hsl(var(--bright-yellow))] transition-all duration-200 cursor-pointer font-medium' }, [
      slots.default && slots.default(),
      h('span', { class: 'absolute bottom-0 left-0 w-0 h-0.5 bg-[hsl(var(--bright-yellow))] transition-all duration-300 group-hover:w-full' })
    ])
  }
})
</script>

<style scoped>
/* Add your styles here or use Tailwind CSS as in the original */
</style>
