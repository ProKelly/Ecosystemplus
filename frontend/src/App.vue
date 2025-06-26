<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { 
  Bars3Icon, 
  XMarkIcon, 
  UserCircleIcon, 
  ChevronDownIcon,
  ArrowRightOnRectangleIcon,
  Cog6ToothIcon,
  HomeIcon,
  InformationCircleIcon,
  MapIcon,
  ChartBarSquareIcon,
  ViewfinderCircleIcon,
  ScaleIcon,
  LightBulbIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'

const mobileMenuOpen = ref(false)
const userDropdownOpen = ref(false)
const modulesDropdownOpen = ref(false)
const scrolled = ref(false)

const authStore = useAuthStore()
const isAuthenticated = computed(() => !!authStore.user)
const userInitials = computed(() => {
  if (!authStore.user) return ''
  return `${authStore.user.first_name?.[0] || ''}${authStore.user.last_name?.[0] || ''}`
})

const handleScroll = () => {
  scrolled.value = window.scrollY > 10
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

const modules = [
  { name: 'Field Detection', path: '/field-detection', icon: ViewfinderCircleIcon },
  { name: 'Crop Classification', path: '/classification', icon: ChartBarSquareIcon },
  { name: 'Crop Monitoring', path: '/monitoring', icon: MapIcon },
  { name: 'Forest Monitoring', path: '/forest-monitoring', icon: ScaleIcon },
  { name: 'Soil Analysis', path: '/soil-moisture', icon: SparklesIcon },
  { name: 'Yield Prediction', path: '/yield-prediction', icon: LightBulbIcon }
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-green-50 to-white flex flex-col">
    <!-- Navigation Bar -->
    <header 
      class="fixed w-full z-50 transition-all duration-300"
      :class="scrolled ? 'bg-white/95 shadow-md backdrop-blur-lg border-b border-green-100' : 'bg-white/90 backdrop-blur-lg border-b border-green-100'"
    >
      <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <RouterLink 
              to="/" 
              class="flex items-center space-x-2 group transition-all duration-200"
            >
              <span class="text-2xl font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent tracking-tight group-hover:scale-105 transition-transform duration-200">
                <span class="hidden sm:inline">🌿EcoSystem</span>
                <span class="text-emerald-600">+</span>
              </span>
            </RouterLink>
          </div>

          <!-- Desktop Navigation -->
          <div class="hidden lg:flex items-center space-x-6">
            <!-- Home Link -->
            <RouterLink 
              to="/" 
              class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors duration-200 flex items-center"
              active-class="text-emerald-600 font-semibold"
            >
              <HomeIcon class="h-5 w-5 mr-1.5" />
              Home
            </RouterLink>
            
            <!-- Modules Dropdown -->
            <div class="relative group">
              <button 
                @click="modulesDropdownOpen = !modulesDropdownOpen"
                class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors duration-200 flex items-center"
                :class="{ 'text-emerald-600 font-semibold': modulesDropdownOpen }"
              >
                <SparklesIcon class="h-5 w-5 mr-1.5" />
                <span>Modules</span>
                <ChevronDownIcon 
                  class="h-4 w-4 ml-1 text-emerald-400 transition-transform duration-200"
                  :class="{ 'rotate-180': modulesDropdownOpen }"
                />
              </button>
              
              <!-- Dropdown -->
              <transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-1"
              >
                <div 
                  v-show="modulesDropdownOpen"
                  @click.away="modulesDropdownOpen = false"
                  class="absolute left-0 mt-2 w-72 bg-white rounded-xl shadow-lg border border-green-100 z-30 py-2 divide-y divide-green-50"
                >
                  <div class="px-4 py-3">
                    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Agricultural Modules
                    </h3>
                  </div>
                  <div class="py-1">
                    <RouterLink 
                      v-for="module in modules"
                      :key="module.path"
                      :to="module.path" 
                      class="group flex items-center px-4 py-2.5 text-sm text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150"
                      @click="modulesDropdownOpen = false"
                    >
                      <component :is="module.icon" class="h-5 w-5 mr-3 text-emerald-500 group-hover:text-emerald-600" />
                      {{ module.name }}
                    </RouterLink>
                  </div>
                </div>
              </transition>
            </div>
            
            <!-- Farm Management Link -->
            <RouterLink 
              to="/farm" 
              class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors duration-200 flex items-center"
              active-class="text-emerald-600 font-semibold"
            >
              <MapIcon class="h-5 w-5 mr-1.5" />
              Farms
            </RouterLink>

            <!-- About Link -->
            <RouterLink 
              to="/about" 
              class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors duration-200 flex items-center"
              active-class="text-emerald-600 font-semibold"
            >
              <InformationCircleIcon class="h-5 w-5 mr-1.5" />
              About
            </RouterLink>

            <!-- Auth Buttons -->
            <div v-if="!isAuthenticated" class="flex items-center space-x-3 ml-4">
              <RouterLink 
                to="/login" 
                class="px-4 py-2 text-sm font-medium text-emerald-600 hover:text-emerald-700 transition-colors duration-200"
              >
                Sign In
              </RouterLink>
              <RouterLink 
                to="/register" 
                class="px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white text-sm font-semibold rounded-lg shadow-sm hover:shadow-md hover:scale-[1.02] transition-all duration-200"
              >
                Get Started
              </RouterLink>
            </div>

            <!-- User Profile Dropdown -->
            <div v-else class="relative ml-4">
              <button 
                @click="userDropdownOpen = !userDropdownOpen"
                class="flex items-center space-x-2 focus:outline-none group"
              >
                <div v-if="authStore.user?.profile_image" class="h-8 w-8 rounded-full overflow-hidden border-2 border-emerald-100 group-hover:border-emerald-200 transition-colors">
                  <img 
                    :src="authStore.user.profile_image" 
                    alt="User profile" 
                    class="h-full w-full object-cover"
                  >
                </div>
                <div v-else class="h-8 w-8 rounded-full bg-emerald-100 flex items-center justify-center border-2 border-emerald-100 group-hover:border-emerald-200 transition-colors">
                  <span v-if="userInitials" class="font-semibold text-emerald-700 text-sm">
                    {{ userInitials }}
                  </span>
                  <UserCircleIcon v-else class="h-6 w-6 text-emerald-600" />
                </div>
              </button>

              <!-- User Dropdown Menu -->
              <transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-1"
              >
                <div 
                  v-show="userDropdownOpen"
                  @click.away="userDropdownOpen = false"
                  class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-green-100 z-30 py-1 divide-y divide-green-50"
                >
                  <div class="px-4 py-3">
                    <p class="text-sm font-semibold text-gray-900 truncate">
                      {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
                    </p>
                    <p class="text-xs text-gray-500 truncate">
                      {{ authStore.user?.email }}
                    </p>
                  </div>
                  <div class="py-1">
                    <RouterLink 
                      to="/profile" 
                      class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-emerald-600 transition-colors duration-150"
                      @click="userDropdownOpen = false"
                    >
                      <Cog6ToothIcon class="h-5 w-5 mr-3 text-gray-400 group-hover:text-emerald-500" />
                      Profile Settings
                    </RouterLink>
                  </div>
                  <div class="py-1">
                    <button 
                      @click="authStore.logout()"
                      class="group flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-red-600 transition-colors duration-150"
                    >
                      <ArrowRightOnRectangleIcon class="h-5 w-5 mr-3 text-gray-400 group-hover:text-red-500" />
                      Sign Out
                    </button>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- Mobile menu button -->
          <div class="flex lg:hidden items-center">
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-emerald-600 hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-emerald-500 transition-colors duration-200"
              :aria-expanded="mobileMenuOpen"
            >
              <span class="sr-only">Open main menu</span>
              <Bars3Icon v-if="!mobileMenuOpen" class="block h-6 w-6" />
              <XMarkIcon v-else class="block h-6 w-6" />
            </button>
          </div>
        </div>
      </nav>

      <!-- Mobile Navigation -->
      <transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div 
          v-show="mobileMenuOpen"
          class="lg:hidden bg-white shadow-xl rounded-b-lg mx-4 border border-green-100"
        >
          <div class="px-2 pt-2 pb-3 space-y-1">
            <!-- Mobile Home Link -->
            <RouterLink 
              to="/" 
              @click="mobileMenuOpen = false"
              class="group flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-green-50 transition-colors duration-150"
              active-class="bg-green-50 text-emerald-600 font-semibold"
            >
              <HomeIcon class="h-5 w-5 mr-3 text-gray-500 group-hover:text-emerald-500" />
              Home
            </RouterLink>

            <!-- Mobile Modules Links -->
            <div class="px-3 py-2">
              <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Modules
              </h3>
              <div class="space-y-1">
                <RouterLink 
                  v-for="module in modules"
                  :key="module.path"
                  :to="module.path"
                  @click="mobileMenuOpen = false"
                  class="group flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-green-50 transition-colors duration-150"
                  active-class="bg-green-50 text-emerald-600 font-semibold"
                >
                  <component :is="module.icon" class="h-5 w-5 mr-3 text-gray-500 group-hover:text-emerald-500" />
                  {{ module.name }}
                </RouterLink>
              </div>
            </div>

            <!-- Mobile Farm Link -->
            <RouterLink 
              to="/farm" 
              @click="mobileMenuOpen = false"
              class="group flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-green-50 transition-colors duration-150"
              active-class="bg-green-50 text-emerald-600 font-semibold"
            >
              <MapIcon class="h-5 w-5 mr-3 text-gray-500 group-hover:text-emerald-500" />
              Farms
            </RouterLink>

            <!-- Mobile About Link -->
            <RouterLink 
              to="/about" 
              @click="mobileMenuOpen = false"
              class="group flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-green-50 transition-colors duration-150"
              active-class="bg-green-50 text-emerald-600 font-semibold"
            >
              <InformationCircleIcon class="h-5 w-5 mr-3 text-gray-500 group-hover:text-emerald-500" />
              About
            </RouterLink>

            <!-- Mobile Auth Links -->
            <div v-if="!isAuthenticated" class="pt-4 border-t border-green-100">
              <RouterLink 
                to="/login" 
                @click="mobileMenuOpen = false"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-emerald-600 hover:bg-green-50 transition-colors duration-150"
              >
                Sign In
              </RouterLink>
              <RouterLink 
                to="/register" 
                @click="mobileMenuOpen = false"
                class="mt-3 w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 transition-colors duration-150"
              >
                Get Started
              </RouterLink>
            </div>

            <!-- Mobile User Links -->
            <div v-else class="pt-4 border-t border-green-100">
              <RouterLink 
                to="/profile" 
                @click="mobileMenuOpen = false"
                class="group flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-emerald-600 hover:bg-green-50 transition-colors duration-150"
              >
                <Cog6ToothIcon class="h-5 w-5 mr-3 text-gray-500 group-hover:text-emerald-500" />
                Profile Settings
              </RouterLink>
              <button 
                @click="authStore.logout(); mobileMenuOpen = false"
                class="group flex items-center w-full px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 transition-colors duration-150"
              >
                <ArrowRightOnRectangleIcon class="h-5 w-5 mr-3 text-gray-500 group-hover:text-red-500" />
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </transition>
    </header>

    <!-- Main Content -->
    <main class="pt-16">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}

/* Router link transitions */
.router-link-active:not(.auth-link) {
  position: relative;
}

.router-link-active:not(.auth-link)::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #16a34a, #10b981);
  border-radius: 2px;
  animation: underlineGrow 0.3s ease-out forwards;
}

@keyframes underlineGrow {
  from {
    transform: scaleX(0);
    opacity: 0;
  }
  to {
    transform: scaleX(1);
    opacity: 1;
  }
}

/* Mobile menu transition */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>