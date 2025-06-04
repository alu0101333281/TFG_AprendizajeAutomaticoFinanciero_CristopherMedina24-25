<!-- src/components/Controls.vue -->
<template>
    <div class="mt-4 flex gap-2">
      <button @click="prev" class="btn">⏪</button>
      <button @click="togglePlay" class="btn">{{ isPlaying ? '⏸ Pause' : '▶️ Play' }}</button>
      <button @click="next" class="btn">⏩</button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const isPlaying = ref(false)
  
  const togglePlay = () => {
    isPlaying.value = !isPlaying.value
  }
  
  const next = () => {
    console.log('Next candle')
  }
  
  const prev = () => {
    console.log('Previous candle')
  }
  </script>
  
  <style scoped>
  .btn {
    background-color: #ddd;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
  </style>
  