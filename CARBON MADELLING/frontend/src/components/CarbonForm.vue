<template>
  <div class="glass max-w-2xl w-full p-8 rounded-2xl shadow-xl animate-[floatIn_0.6s_ease-out]">
    <h1 class="text-3xl font-extrabold text-center mb-8 bg-gradient-to-r from-green-700 via-emerald-500 to-lime-400 bg-clip-text text-transparent">
      Farm Carbon Footprint
    </h1>

    <!-- Stepper indicators -->
    <div class="flex justify-center gap-2 mb-6">
      <span v-for="n in 3" :key="n" :class="['h-2 w-8 rounded-full transition', step>=n ? 'bg-brand-green' : 'bg-gray-300']"></span>
    </div>

    <!-- STEPS -->
    <div v-if="step===1">
      <p class="mb-4 text-gray-600 text-sm">Step 1 of 3 – Tell us about your farm basics.</p>
      <div class="grid sm:grid-cols-2 gap-6">
        <InputField label="Farm Area (ha) *" type="number" v-model.number="form.area_hectares" />
        <SelectField label="Season *" v-model="form.season" :options="seasonOptions" />
        <div class="sm:col-span-2 text-right"><button @click="next" :disabled="!canGoNext" class="px-6 py-2 rounded-full bg-brand-green text-white disabled:opacity-40">Next</button></div>
      </div>
    </div>

    <div v-else-if="step===2">
      <p class="mb-4 text-gray-600 text-sm">Step 2 of 3 – Inputs & resources you use each month.</p>
      <div class="grid sm:grid-cols-2 gap-6">
        <SelectField label="Farming Method *" v-model="form.farming_method" :options="methods" help="Choose how you generally manage your crops" />
        <SelectField label="Fertilizer Level *" v-model="form.fertilizer_level" :options="fertLevels" help="Approximate fertiliser per hectare" />
        <InputField label="Fuel Usage (L/month)" type="number" v-model.number="form.monthly_fuel_liters" />
        <SelectField label="Do you keep livestock?" v-model="form.has_livestock" :options="[{value:'yes',label:'Yes'},{value:'no',label:'No'}]" />
        <div class="sm:col-span-2 flex justify-between"><button @click="back" class="px-6 py-2 rounded-full bg-gray-200">Back</button><button @click="next" :disabled="!canGoNext" class="px-6 py-2 rounded-full bg-brand-green text-white disabled:opacity-40">Next</button></div>
      </div>
    </div>

    <div v-else class="space-y-6">
      <p class="text-gray-600 text-sm">Step 3 of 3 – Livestock numbers (leave blank if zero).</p>
      <transition name="fade-grow" mode="out-in">
        <div v-if="form.has_livestock==='yes'" key="ls">
          <h2 class="text-lg font-medium mb-2 text-green-800">Livestock Numbers</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <InputField v-for="animal in Object.keys(form.livestock)" :key="animal" :label="animal" type="number" v-model.number="form.livestock[animal]" />
          </div>
        </div>
      </transition>
      <div class="flex justify-between items-center">
        <button @click="back" class="px-6 py-2 rounded-full bg-gray-200">Back</button>
        <div v-if="previewTotal!==null" class="text-sm text-green-800">≈ {{ format(previewTotal) }} / month</div>
      </div>
    </div>

    <div v-if="error" class="text-red-600 text-sm text-center mt-4">{{ error }}</div>

    <button v-if="step===3" :disabled="loading" @click="submit"
      class="mt-6 w-full bg-gradient-to-r from-emerald-600 via-emerald-500 to-lime-500 bg-[length:200%_200%] animate-[pulseGradient_8s_linear_infinite] text-white py-3 rounded-full shadow-lg flex items-center justify-center gap-2 hover:shadow-xl transition active:scale-95 disabled:opacity-50">
      <svg v-if="loading" class="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10" class="opacity-25"/><path d="M4 12a8 8 0 018-8" class="opacity-75"/></svg>
      <span>{{ loading ? 'Calculating…' : 'Calculate' }}</span>
    </button>
  </div>
</template>

<script setup>
import { reactive, ref, watch, computed } from 'vue';
import InputField from './InputField.vue';
import SelectField from './SelectField.vue';

const emit = defineEmits(['calculated']);

const form = reactive({
  area_hectares: '',
  season: '',
  farming_method: '',
  fertilizer_level: '',
  monthly_fuel_liters: '',
  has_livestock: 'no',
  livestock: { cattle: '', goat: '', sheep: '', rams: '', pigs: '', poultry: '' },
});

const methods = [
  { value: 'conventional', label: 'Conventional (synthetic fertilisers & tillage)' },
  { value: 'organic', label: 'Organic (natural inputs, no chemicals)' },
  { value: 'agroforestry', label: 'Agro-forestry (trees integrated with crops)' },
  { value: 'conservation', label: 'Conservation (minimum till & cover crops)' },
  { value: 'permaculture', label: 'Permaculture (permanent mixed systems)' },
];

const fertLevels = [
  { value: 'none', label: 'None (0 kg/ha)' },
  { value: 'low', label: 'Low (≤ 50 kg/ha)' },
  { value: 'medium', label: 'Medium (50–100 kg/ha)' },
  { value: 'high', label: 'High (100 kg/ha+)' },
];

const seasonOptions = [
  { value: 'dry', label: 'Dry Season (Nov–Mar)' },
  { value: 'rainy', label: 'Rainy Season (Apr–Oct)' },
];

const loading = ref(false);
const error = ref('');
const step = ref(1);
const previewTotal = ref(null);

function next(){if(step.value<3) step.value++;}
function back(){if(step.value>1) step.value--;}
const canGoNext = computed(()=>{
  if(step.value===1){return form.area_hectares && form.season;}
  if(step.value===2){return form.farming_method && form.fertilizer_level;}
  return true;
});

function format(v){return v>=1000?`${(v/1000).toFixed(2)} t`:`${v.toFixed(2)} kg`;}

// simple debounce helper
function debounce(fn,ms){let t;return (...args)=>{clearTimeout(t);t=setTimeout(()=>fn(...args),ms);};}

const fetchPreview=debounce(async()=>{
  // need core fields to estimate
  if(!form.area_hectares||!form.season||!form.farming_method||!form.fertilizer_level) {previewTotal.value=null;return;}
  const payload={
    area_hectares:Number(form.area_hectares),season:form.season,farming_method:form.farming_method,
    fertilizer_level:form.fertilizer_level,monthly_fuel_liters:Number(form.monthly_fuel_liters||0),livestock:{}}
  if(form.has_livestock==='yes'){
    Object.keys(form.livestock).forEach(k=>{const v=parseInt(form.livestock[k]);if(!isNaN(v)&&v>0) payload.livestock[k]=v;});
  }
  try{const res=await fetch('http://localhost:8000/emissions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  if(res.ok){const d=await res.json();previewTotal.value=d.report.total_emissions;}}
  catch{previewTotal.value=null;}
},800);

watch(form,fetchPreview,{deep:true});

async function submit(){
  if(!form.area_hectares||!form.season||!form.farming_method||!form.fertilizer_level){
    error.value='Please fill all required fields';return;}
  loading.value=true;error.value='';
  try{
    const payload={
      area_hectares:Number(form.area_hectares),
      season:form.season,
      farming_method:form.farming_method,
      fertilizer_level:form.fertilizer_level,
      monthly_fuel_liters:Number(form.monthly_fuel_liters||0),
      livestock:{}
    };
    if(form.has_livestock==='yes'){
      Object.keys(form.livestock).forEach(k=>{
        const v=parseInt(form.livestock[k],10);
        if(!isNaN(v)&&v>0) payload.livestock[k]=v;
      });
    }
    const res=await fetch('http://localhost:8000/emissions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(!res.ok){const d=await res.json();throw new Error(d.detail||'Error');}
    const data=await res.json();
    emit('calculated',data.report);
  }catch(e){error.value=e.message||'Error';}
  finally{loading.value=false;}
}
</script>

<style scoped>
.fade-grow-enter-active,.fade-grow-leave-active{transition:all .4s ease;}
.fade-grow-enter-from,.fade-grow-leave-to{opacity:0;transform:scale(.95);}
</style> 