<template>
  <div class="h-screen w-screen grid grid-cols-[60px_1fr_300px] grid-rows-[auto_1fr_auto] gap-0 bg-gray-900 text-white">

    <!-- Herramientas de dibujo (izquierda) -->
    <div class="row-span-3 bg-gray-800 border-r border-gray-700 p-2">
      <DrawingTools />
    </div>

    <!-- Barra superior con timeframes y controles -->
    <div class="col-span-1 bg-gray-800 border-b border-gray-700 p-2 flex items-center justify-between">
      <Timeframes @update:timeframe="handleTimeframeChange" />
      <Controls />
    </div>

    <!-- Gráfico -->
    <div class="bg-black overflow-hidden">
      <Chart :rawData="binanceData" :timeframe="selectedTimeframe" />
    </div>

    <!-- TradeLog (abajo del gráfico) -->
    <div class="bg-gray-800 border-t border-gray-700 p-2 overflow-auto">
      <TradeLog />
    </div>

    <!-- Barra lateral derecha con pares -->
    <div class="row-span-3 bg-gray-800 border-l border-gray-700 p-2 overflow-y-auto">
      <CurrencyPairs />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'

const selectedTimeframe = ref('1m')

function handleTimeframeChange(tf) {
  console.log('📥 Nuevo timeframe recibido en BacktestingView:', tf)
  selectedTimeframe.value = tf
}
import Chart from '@/components/Chart.vue'
import Controls from '@/components/Controls.vue'
import TradeLog from '@/components/TradeLog.vue'
import Timeframes from '@/components/TimeFrames.vue'
import CurrencyPairs from '@/components/PairList.vue'
import DrawingTools from '@/components/DrawingTools.vue'
import binanceData from '@/assets/data/binanceData.json'
</script>
