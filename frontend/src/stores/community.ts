import { defineStore } from 'pinia'
import api from '@/api'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

export const useCommunityStore = defineStore('community', () => {
  const communities = ref([])
  const currentCommunity = ref(null)
  const authStore = useAuthStore()

  const createCommunity = async (communityData: {
    name: string
    email: string
    latitude: number
    longitude: number
  }) => {
    const token = authStore.token
    const response = await api.createCommunity(communityData, token)
    currentCommunity.value = response.data
    return response.data
  }

  const fetchCommunities = async () => {
    const token = authStore.token
    const response = await api.fetchCommunities(token)
    communities.value = response.data
  }

  return {
    communities,
    currentCommunity,
    createCommunity,
    fetchCommunities
  }
})