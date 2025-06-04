<template>
    <div class="flex space-x-2">
      <button v-for="frame in timeframes" :key="frame" class="px-3 py-1 border rounded hover:bg-gray-100">
        {{ frame }}
      </button>
    </div>
  </template>
  
  <script setup lang="ts">
  const timeframes = ['1m', '5m', '15m', '1h', '4h', '1D']
  </script>