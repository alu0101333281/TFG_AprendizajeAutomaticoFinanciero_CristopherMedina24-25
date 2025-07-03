<template>
  <div class="flex flex-col space-y-2">
    <button @click="emitTool('line')" class="p-2 hover:bg-gray-200 rounded" title="Línea">📏</button>
    <button @click="emitTool('horizontal')" class="p-2 hover:bg-gray-200 rounded" title="Horizontal">📶</button>
    <button @click="emitTool('vertical')" class="p-2 hover:bg-gray-200 rounded" title="Vertical">📐</button>
    <button @click="emitTool('channel')" class="p-2 hover:bg-gray-200 rounded" title="Canal">📊</button>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ (e: 'draw-tool', tool: string): void }>()

function emitTool(tool: string) {
  emit('draw-tool', tool)
}
</script>
