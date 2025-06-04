<!-- src/components/TradeLog.vue -->
<template>
    <div class="border p-4 rounded">
      <h2 class="text-lg font-bold mb-2">Historial de Trades</h2>
      <ul>
        <li v-for="(trade, index) in trades" :key="index">
          {{ trade.type }} @ {{ trade.price }} – {{ trade.result }}
        </li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const trades = ref([
    { type: 'BUY', price: 105, result: '+10€' },
    { type: 'SELL', price: 115, result: '-5€' },
  ])
  </script>
  