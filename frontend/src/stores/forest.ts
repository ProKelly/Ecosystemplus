// stores/forest.js
import { ref } from 'vue'
import { defineStore } from 'pinia'

interface Forest {
  id: string;
  name: string;
  area: number;
  coordinates: [number, number][];
}

export const useForestStore = defineStore('forest', () => {
  const forests = ref<Forest[]>([
    { id: '1', name: 'Bamenda Conservation Zone', area: 1245.3, coordinates: [[5.9631, 10.1591], [5.9831, 10.1791], [5.9531, 10.1791]] },
    { id: '2', name: 'Korup National Park', area: 1259.7, coordinates: [[5.2631, 9.8591], [5.2831, 9.8791], [5.2531, 9.8791]] }
  ])
  const currentForestId = ref<string>('')

  function addForest(forest: Forest) {
    forests.value.push(forest)
  }
  function setCurrentForest(id: string) {
    currentForestId.value = id
  }

  return { forests, currentForestId, addForest, setCurrentForest }
})