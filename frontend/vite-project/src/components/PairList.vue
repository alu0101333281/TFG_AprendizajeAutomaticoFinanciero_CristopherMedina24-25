<template>
  <div class="pair-list">
    <label for="pair">Seleccionar par:</label>
    <select id="pair" v-model="selectedPair" @change="emitPairChange">
      <option v-for="pair in pairs" :key="pair" :value="pair">
        {{ pair }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['pair-selected'])

const selectedPair = ref('BTCUSDT')

const pairs = [
  'BTCUSDT',
  'ETHUSDT',
  'LTCUSDT',
  'BNBUSDT',
  'XRPUSDT'
]

function emitPairChange() {
  emit('pair-selected', selectedPair.value)
}
</script>

<style scoped>
.pair-list {
  margin-bottom: 1rem;
}
select {
  padding: 0.5rem;
}
</style>
