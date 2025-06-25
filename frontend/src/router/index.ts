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
  ],
})

export default router
