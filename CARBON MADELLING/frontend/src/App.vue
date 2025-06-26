<template>
  <ParticleBg />
  <div class="min-h-screen flex flex-col text-gray-800 relative">
    <SideNav />
    <div class="flex-1 flex flex-col md:pl-64">
      <TopBar />
      <main class="flex-1 flex items-start justify-center py-10 px-4">
        <CarbonForm v-if="view==='form'" @calculated="onCalculated" />
        <CarbonDashboard v-else :report="report" @back="reset" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SideNav from './components/SideNav.vue';
import TopBar from './components/TopBar.vue';
import CarbonForm from './components/CarbonForm.vue';
import CarbonDashboard from './views/CarbonDashboard.vue';
import ParticleBg from './components/ParticleBg.vue';

const report = ref(null);
const view = ref('form');

function onCalculated(res) {
  report.value = res;
  view.value = 'dashboard';
}

function reset() {
  report.value = null;
  view.value = 'form';
}
</script>

<style scoped>
</style> 