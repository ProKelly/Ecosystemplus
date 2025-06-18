<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { 
  PaperAirplaneIcon, 
  SparklesIcon, 
  SunIcon, 
  ChartBarIcon, 
  MapIcon, 
  CalendarIcon, 
  QuestionMarkCircleIcon,
  UserCircleIcon,
  CogIcon,
  BookmarkIcon,
  LightBulbIcon,
  CloudIcon,
  ShieldCheckIcon,
  ArrowsRightLeftIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'

// Chat state
const messages = ref<Array<{role: string, content: string, images?: Array<string>}>>([
  {
    role: 'assistant',
    content: 'Welcome to your EcoSystem+ AI Assistant! I can help with:\n\n• Crop selection\n• Pest management\n• Soil health\n• Weather impacts\n\nWhat would you like to discuss today?',
    images: []
  }
])
const userInput = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const activeTab = ref('chat')

// User profile
const userProfile = ref({
  name: 'Green Valley Farm',
  location: 'Iowa, USA',
  size: '120 hectares',
  soil: 'Clay loam',
  crops: ['Corn', 'Soybeans'],
  challenges: ['Pest infestations', 'Drought', 'Soil erosion']
})

// Quick actions
const quickActions = [
  { icon: SunIcon, text: 'Crop advice', query: 'Best crops for my soil' },
  { icon: ShieldCheckIcon, text: 'Pest control', query: 'Organic pest solutions' },
  { icon: CloudIcon, text: 'Weather', query: 'Weather impact on my crops' },
  { icon: ArrowsRightLeftIcon, text: 'Rotation', query: 'Optimal crop rotation' }
]

// Simulate AI response
const getAIResponse = async (query: string) => {
  isLoading.value = true
  isTyping.value = true
  
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1200 + Math.random() * 800))
  
  // Mock responses
  const responses = [
    `For ${userProfile.value.crops.join(' and ')} in ${userProfile.value.location}, consider:\n\n• Soil testing every 3 months\n• Drip irrigation for water efficiency\n• Companion planting with legumes`,
    `Based on your ${userProfile.value.soil} soil:\n\n• pH should be 6.0-6.8\n• Add organic matter annually\n• Rotate with nitrogen-fixing crops`,
    `Weather patterns suggest:\n\n• Earlier planting this season\n• Increased rainfall expected\n• Monitor for fungal diseases`,
    `For pest management:\n\n• Scout fields weekly\n• Introduce beneficial insects\n• Use targeted treatments only`
  ]
  
  messages.value.push({
    role: 'assistant',
    content: responses[Math.floor(Math.random() * responses.length)],
    images: []
  })
  
  isLoading.value = false
  isTyping.value = false
  scrollToBottom()
}

const sendMessage = () => {
  if (!userInput.value.trim()) return
  
  messages.value.push({
    role: 'user',
    content: userInput.value
  })
  
  getAIResponse(userInput.value)
  userInput.value = ''
  scrollToBottom()
}

const startQuickAction = (query: string) => {
  userInput.value = query
  sendMessage()
}

const scrollToBottom = () => {
  nextTick(() => {
    const container = document.getElementById('chat-messages')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  })
}

const windowWidth = ref(window.innerWidth)

function isMobile() {
  return windowWidth.value < 768
}

onMounted(() => {
  window.addEventListener('resize', () => {
    windowWidth.value = window.innerWidth
  })
})
</script>

<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="bg-white border-b border-emerald-100 shadow-sm sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="bg-emerald-100 p-2 rounded-lg">
              <SparklesIcon class="h-6 w-6 text-emerald-600" />
            </div>
            <h1 class="text-xl font-bold text-gray-800">
              <span class="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                Farm Assistant
              </span>
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <button class="p-2 rounded-full hover:bg-emerald-50 transition-colors">
              <UserCircleIcon class="h-5 w-5 text-emerald-600" />
            </button>
            <button class="p-2 rounded-full hover:bg-emerald-50 transition-colors">
              <CogIcon class="h-5 w-5 text-emerald-600" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Sidebar -->
      <div class="lg:col-span-3 space-y-6">
        <!-- User Profile -->
        <div class="bg-gradient-to-br from-emerald-50 to-white rounded-2xl shadow-lg p-6 mb-6">
              <!-- Desktop only heading/desc -->
            <div v-if="!isMobile()" class="text-right">
              <h3 class="text-lg font-bold text-gray-900 leading-tight">Your Farm Profile</h3>
              <p class="text-xs text-gray-500 mt-1">Personalized for you</p>
            </div>
          <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4 gap-4">
            <div class="flex items-center gap-3">
              <div class="bg-emerald-100 rounded-full p-2">
                <SparklesIcon class="h-7 w-7 text-emerald-500" />
              </div>
              <!-- Mobile only heading/desc -->
              <div v-if="isMobile()">
                <h3 class="text-lg font-bold text-gray-900 leading-tight">Your Farm Profile</h3>
                <p class="text-xs text-gray-500 mt-1">Personalized for you</p>
              </div>
            </div>
            <button class="flex items-center gap-1 text-xs font-semibold text-emerald-700 hover:text-emerald-900 bg-emerald-50 border border-emerald-100 px-3 py-1.5 rounded-lg shadow-sm transition-colors">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
              Edit Profile
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-4">
            <div class="flex flex-col gap-1">
              <span class="text-xs text-gray-500">Location</span>
              <span class="flex items-center gap-2 text-base font-semibold text-gray-800">
                <MapIcon class="h-5 w-5 text-blue-400" />
                {{ userProfile.location }}
              </span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs text-gray-500">Farm Size</span>
              <span class="flex items-center gap-2 text-base font-semibold text-gray-800">
                <ChartBarIcon class="h-5 w-5 text-emerald-400" />
                {{ userProfile.size }}
              </span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs text-gray-500">Soil Type</span>
              <span class="flex items-center gap-2 text-base font-semibold text-gray-800">
                <SunIcon class="h-5 w-5 text-amber-400" />
                {{ userProfile.soil }}
              </span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs text-gray-500">Current Crops</span>
              <div class="flex flex-wrap gap-2 mt-1">
                <span v-for="crop in userProfile.crops" :key="crop" class="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full text-xs font-semibold border border-emerald-200 shadow-sm">
                  {{ crop }}
                </span>
              </div>
            </div>
          </div>
          <div>
            <span class="text-xs text-gray-500 mb-1 block">Challenges</span>
            <div class="flex flex-wrap gap-2">
              <span v-for="challenge in userProfile.challenges" :key="challenge" class="bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-semibold border border-red-200 shadow-sm">
                {{ challenge }}
              </span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-xl border border-emerald-100 shadow-sm p-5">
          <div class="flex items-center space-x-3 mb-4">
            <div class="bg-emerald-100 p-2 rounded-lg">
              <LightBulbIcon class="h-5 w-5 text-emerald-600" />
            </div>
            <h3 class="font-medium text-gray-800">Quick Actions</h3>
          </div>
          
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="(action, index) in quickActions"
              :key="index"
              @click="startQuickAction(action.query)"
              class="flex flex-col items-center p-3 border border-emerald-100 rounded-lg hover:bg-emerald-50 transition-colors group"
            >
              <component 
                :is="action.icon" 
                class="h-6 w-6 mb-2 text-emerald-500 group-hover:text-emerald-600 transition-colors" 
              />
              <span class="text-xs text-center font-medium text-gray-700 group-hover:text-emerald-600 transition-colors">
                {{ action.text }}
              </span>
            </button>
          </div>
        </div>

      </div>

      <!-- Main Chat Area -->
      <div class="lg:col-span-9 flex flex-col">
        <div class="bg-white rounded-xl border border-emerald-100 shadow-sm flex-1 flex flex-col h-[calc(100vh-180px)]">
          <!-- Chat Header -->
          <div class="border-b border-emerald-100 p-4 bg-white sticky top-0 z-10">
            <div class="flex items-center justify-between">
              <h2 class="font-medium text-gray-800 flex items-center">
                <span class="bg-emerald-100 p-1.5 rounded-lg mr-3">
                  <SparklesIcon class="h-5 w-5 text-emerald-600" />
                </span>
                Agricultural Assistant
              </h2>
              <div class="flex space-x-2">
                <button 
                  @click="activeTab = 'chat'"
                  :class="[activeTab === 'chat' ? 'text-emerald-600 bg-emerald-50' : 'text-gray-500 hover:bg-emerald-50', 'p-2 rounded-lg transition-colors']"
                  title="Chat"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </button>
                <button 
                  @click="activeTab = 'saved'"
                  :class="[activeTab === 'saved' ? 'text-emerald-600 bg-emerald-50' : 'text-gray-500 hover:bg-emerald-50', 'p-2 rounded-lg transition-colors']"
                  title="Saved"
                >
                  <BookmarkIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- Messages Container -->
          <div 
            id="chat-messages"
            class="flex-1 p-4 overflow-y-auto space-y-4"
            :class="{'bg-gray-50': activeTab !== 'chat'}"
          >
            <template v-if="activeTab === 'chat'">
              <div 
                v-for="(message, index) in messages" 
                :key="index"
                :class="[message.role === 'user' ? 'justify-end' : 'justify-start', 'flex']"
              >
                <div 
                  :class="[message.role === 'user' ? 'bg-emerald-600 text-white' : 'bg-emerald-50 text-gray-800 border border-emerald-100', 'rounded-2xl px-4 py-3 max-w-3xl shadow-xs']"
                >
                  <div class="whitespace-pre-wrap">{{ message.content }}</div>
                </div>
              </div>

              <!-- Typing indicator -->
              <div v-if="isTyping" class="flex justify-start">
                <div class="bg-emerald-50 text-gray-800 rounded-2xl px-4 py-3 border border-emerald-100">
                  <div class="flex space-x-2">
                    <div class="h-2 w-2 bg-emerald-400 rounded-full animate-bounce"></div>
                    <div class="h-2 w-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="h-2 w-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="h-full flex flex-col items-center justify-center py-12">
                <BookmarkIcon class="h-12 w-12 text-emerald-400 mb-4" />
                <h3 class="text-lg font-medium text-gray-800 mb-2">Saved Recommendations</h3>
                <p class="text-gray-500 max-w-md text-center">
                  Your bookmarked recommendations will appear here. Click the bookmark icon on any message to save it.
                </p>
              </div>
            </template>
          </div>

          <!-- Input Area -->
          <div class="border-t border-emerald-100 p-4 bg-white sticky bottom-0">
            <div class="flex items-center space-x-3">
              <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                placeholder="Ask about crops, soil, or weather..."
                class="flex-1 border border-emerald-200 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent shadow-xs text-gray-700 placeholder-gray-400"
              />
              <button
                @click="sendMessage"
                :disabled="isLoading"
                class="bg-emerald-600 hover:bg-emerald-700 text-white rounded-full p-3 disabled:opacity-50 transition-colors shadow-md hover:shadow-lg"
              >
                <PaperAirplaneIcon class="h-5 w-5" />
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-2 text-center flex items-center justify-center">
              <ShieldCheckIcon class="h-3 w-3 mr-1" />
              EcoSystem+ AI provides agricultural guidance only
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
/* Chat messages container styling */
#chat-messages {
  scroll-behavior: smooth;
  max-height: calc(100vh - 300px);
  min-height: 200px;
  padding-bottom: 1rem;
}

/* Animation for messages */
@keyframes messageIn {
  0% { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}

.flex > div {
  animation: messageIn 0.25s ease-out;
}

/* Custom scrollbar */
#chat-messages::-webkit-scrollbar {
  width: 6px;
}

#chat-messages::-webkit-scrollbar-track {
  background: #f0fdf4;
}

#chat-messages::-webkit-scrollbar-thumb {
  background: #a7f3d0;
  border-radius: 3px;
}

/* Shadow utility */
.shadow-xs {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Input field styling */
input::placeholder {
  color: #9ca3af;
  opacity: 1;
}

/* Responsive adjustments */
@media (max-width: 1023px) {
  #chat-messages {
    max-height: calc(100vh - 260px);
  }
}
</style>