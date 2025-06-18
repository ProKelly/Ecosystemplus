import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CropMonitoring from '../views/crop-monitoring.vue' 
import SoilMoisture from '../views/soil-moisture.vue' 
import CropClassification from '../views/crop-classification1.vue' 
import FieldBoundaryDetection from '@/components/field-boundary/FieldBoundaryDetection.vue'
import PersonalizedRecommendations from '@/components/personalized-recommendations/Bot.vue'
import Bot from '@/components/personalized-recommendations/Bot.vue'


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
      path: '/personalized-recommendations',
      name: 'personalized-recommendations',
      component: Bot
    }
  ],
})

export default router
