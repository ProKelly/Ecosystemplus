<script setup lang="ts">
console.log('jeje')
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref<HTMLElement | null>(null)
const selectedLocation = ref<{ lat: number; lng: number } | null>(null)
const locationData = ref<Record<string, any>>({})

function registerLocation() {
  if (selectedLocation.value) {
    locationData.value = {
      latitude: selectedLocation.value.lat,
      longitude: selectedLocation.value.lng,
      timestamp: new Date().toISOString(),
    }
    console.log('Location registered:', locationData.value)
  } else {
    alert('Please select a location on the map.')
  }
}

onMounted(() => {
  if (!mapContainer.value) {
    console.error('Map container not found.')
    return
  }

  const map = L.map(mapContainer.value).setView([7.5, 13.5], 6)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)

  let marker: L.Marker

  map.on('click', (e: L.LeafletMouseEvent) => {
    selectedLocation.value = e.latlng
    if (marker) {
      marker.setLatLng(e.latlng)
    } else {
      marker = L.marker(e.latlng).addTo(map)
    }
  })
})
</script>

<template>
  <div class="min-h-screen bg-white px-6 md:px-16 lg:px-24 py-10 shadow-md">
    <div ref="mapContainer" class="h-96 w-full mb-4 rounded shadow"></div>
    <button @click="registerLocation" class="bg-green-600 text-white px-4 py-2 rounded">
      Register Location
    </button>
  </div>
</template>

<!-- <style scoped>
#map {
  height: 400px;
}
</style> -->
