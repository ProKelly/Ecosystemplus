<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PropType } from 'vue'

interface Field {
  id: number
  name: string
  area: string
  date: string
  accuracy: string
}

// Props
const props = defineProps({
  history: {
    type: Array as PropType<Field[]>,
    required: true,
    default: () => []
  }
})

// State for sorting
const sortColumn = ref<keyof Field>('date')
const sortDirection = ref<'asc' | 'desc'>('desc')

// Computed sorted history
const sortedHistory = computed(() => {
  return [...props.history].sort((a, b) => {
    const valueA = a[sortColumn.value]
    const valueB = b[sortColumn.value]
    
    if (sortColumn.value === 'area') {
      // Convert area strings (e.g., "15.2 ha") to numbers for comparison
      const numA = parseFloat(String(valueA))
      const numB = parseFloat(String(valueB))
      return sortDirection.value === 'asc' ? numA - numB : numB - numA
    } else if (sortColumn.value === 'accuracy') {
      // Convert accuracy strings (e.g., "92%") to numbers
      const numA = parseFloat(String(valueA))
      const numB = parseFloat(String(valueB))
      return sortDirection.value === 'asc' ? numA - numB : numB - numA
    } else {
      // String comparison for name and date
      return sortDirection.value === 'asc'
        ? String(valueA).localeCompare(String(valueB))
        : String(valueB).localeCompare(String(valueA))
    }
  })
})

// Toggle sorting
const toggleSort = (column: keyof Field) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

// Emit event to view field on map
const emit = defineEmits(['view-field'])
const viewField = (field: Field) => {
  emit('view-field', field)
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th 
            v-for="column in ['name', 'area', 'date', 'accuracy']" 
            :key="column"
            scope="col"
            class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:text-gray-700"
            :class="{ 'text-emerald-600': sortColumn === column }"
            @click="toggleSort(column as keyof Field)"
          >
            <div class="flex items-center">
              {{ column.charAt(0).toUpperCase() + column.slice(1) }}
              <svg 
                v-if="sortColumn === column" 
                class="ml-1 h-4 w-4" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  :d="sortDirection === 'asc' ? 'M19 14l-7 7m0 0l-7-7m7 7V3' : 'M5 10l7-7m0 0l7 7m-7-7v18'"
                />
              </svg>
            </div>
          </th>
          <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr 
          v-for="field in sortedHistory" 
          :key="field.id" 
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-3 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900">{{ field.name }}</div>
          </td>
          <td class="px-4 py-3 whitespace-nowrap">
            <div class="text-sm text-gray-500">{{ field.area }}</div>
          </td>
          <td class="px-4 py-3 whitespace-nowrap">
            <div class="text-sm text-gray-500">{{ field.date }}</div>
          </td>
          <td class="px-4 py-3 whitespace-nowrap">
            <div class="text-sm text-gray-500">{{ field.accuracy }}</div>
          </td>
          <td class="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
            <button 
              @click="viewField(field)"
              class="text-emerald-600 hover:text-emerald-900"
            >
              View on Map
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* Ensure table cells don't wrap unnecessarily */
td, th {
  vertical-align: middle;
}

/* Add subtle hover effect for action buttons */
.text-emerald-600:hover {
  transition: color 0.2s ease-in-out;
}
</style>