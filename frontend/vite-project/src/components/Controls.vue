<template>
  <div class="controls flex items-center gap-4 p-2 bg-gray-800 rounded">
    <!-- Botón para activar selección de punto inicial -->
    <button @click="activateSelectionMode" :class="['btn', isSelecting ? 'bg-yellow-600' : '']">
      Seleccionar inicio
    </button>

    <!-- Botones de navegación -->
    <button @click="$emit('prev-candle')" class="btn">⏪</button>
    <button @click="$emit('toggle-play')" class="btn">
      {{ isPlaying ? '⏸️ Pause' : '▶️ Play' }}
    </button>
    <button @click="$emit('next-candle')" class="btn">⏩</button>

    <!-- Control de velocidad -->
    <div class="flex items-center gap-2">
      <label for="speed" class="text-sm">Velocidad</label>
      <input
        id="speed"
        type="range"
        min="100"
        max="2000"
        step="100"
        :value="playSpeed"
        @input="$emit('update:playSpeed', +($event.target as HTMLInputElement).value)"
      />
      <span class="text-xs">{{ playSpeed }}ms</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  isPlaying: boolean
  playSpeed: number
}>()

const emit = defineEmits<{
  (e: 'start-selection'): void
  (e: 'next-candle'): void
  (e: 'prev-candle'): void
  (e: 'toggle-play'): void
  (e: 'update:playSpeed', speed: number): void
}>()

const isSelecting = ref(false)

const activateSelectionMode = () => {
  isSelecting.value = true
  emit('start-selection')
}
</script>

<style scoped>
.controls {
  background-color: #2d2d2d;
  border-radius: 0.5rem;
}
.btn {
  background-color: #444;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}
.btn:hover {
  background-color: #666;
}
</style>
