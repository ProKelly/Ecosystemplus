import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CropMonitoring from '../views/crop-monitoring.vue' 
import SoilMoisture from '../views/soil-moisture.vue' 
import CropClassification from '../views/crop-classification1.vue' 
import FieldBoundaryDetection from '@/components/field-boundary/FieldBoundaryDetection.vue'
import PersonalizedRecommendations from '@/components/personalized-recommendations/Bot.vue'
import Bot from '@/components/personalized-recommendations/Bot.vue'
import ForestMonitor from '../views/ForestMonitor.vue'
import ForestRegister from '../views/ForestRegister.vue'
import Farm from '../views/Farm.vue'
import FieldBoundaryDetail from '@/components/field-boundary/FieldBoundaryDetail.vue'


import { useAuthStore } from '@/stores/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/monitoring',
      name: 'crop-monitoring',
      component: CropMonitoring
    },
    {
    path: '/forest-monitoring',
    name: 'forest-monitoring',
    component: ForestMonitor
  },
  {
    path: '/register-forest',
    name: 'register-forest',
    component: ForestRegister
  },
    {
      path: '/soil-moisture',
      name: 'soil-moisture',
      component: SoilMoisture
    },
    {
      path: '/classification',
      name: 'crop-classification',
      component: CropClassification
    },
    {
      path: '/field-detection',
      name: 'FieldBoundaryDetection',
      component: FieldBoundaryDetection
    },
    {
      path: '/fields/:id',
      name: 'field-boundary-detail',
      component: FieldBoundaryDetail
    },
    {
      path: '/personalized-recommendations',
      name: 'personalized-recommendations',
      component: Bot
    },
    {
      path: '/farm',
      name: 'farm',
      component: Farm
    },
    {
      path: '/map',
      name: 'map-view',
      component: () => import('@/components/farm/FarmMapView.vue')
    },




    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/Login.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/Register.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/auth/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/community/create',
      name: 'create-community',
      component: () => import('@/views/community/CreateCommunity.vue'),
      meta: { requiresAuth: true, requiresCommunityAdmin: true }
    },
    {
      path: '/community/manage',
      name: 'manage-community',
      component: () => import('@/views/community/ManageCommunity.vue'),
      meta: { requiresAuth: true, requiresCommunityAdmin: true }
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Check if route is for guests only
  // if (to.meta.guestOnly && authStore.token) {
  //   return { name: 'dashboard' }
  // }

  // Check if user needs to be fetched
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }

  // Check if route requires community admin role
  // if (to.meta.requiresCommunityAdmin && !authStore.user?.is_community) {
  //   return { name: 'dashboard' }
  // }
})

export default router
