<template>
    <div class="flex space-x-2">
    <button
      v-for="frame in timeframes"
      :key="frame"
      @click="selectTimeframe(frame)"
      class="px-3 py-1 border rounded hover:bg-gray-100"
      :class="{ 'bg-gray-200 text-black': selected === frame }"
    >
      {{ frame }}
    </button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  const timeframes = ['1m', '5m', '15m', '1h', '4h', '1D']
  const selected = ref('1m')
  const emit =defineEmits(['update:timeframe'])
  function selectTimeframe(tf){
    console.log('🕒 Se seleccionó timeframe:', tf)
    selected.value = tf
    emit('update:timeframe',tf)
  }
  </script>