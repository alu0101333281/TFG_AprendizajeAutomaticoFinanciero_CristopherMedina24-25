/* Componente: PairList.vue */
<template>
  <div>
    <div v-for="pair in pairs" :key="pair.symbol" class="border-b py-2">
      <div class="font-semibold">{{ pair.symbol }}</div>
      <div class="text-sm text-gray-600">Precio: {{ pair.price }} | Cambio: {{ pair.change }}%</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const pairs = [
  { symbol: 'BTC/USD', price: '42,000', change: '+1.2' },
  { symbol: 'ETH/USD', price: '3,100', change: '-0.5' },
  { symbol: 'BNB/USD', price: '400', change: '+0.8' },
]
</script>
