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
      <Chart :timeframe="selectedTimeframe" :symbol="selectedPair" />
    </div>

    <!-- TradeLog (abajo del gráfico) -->
    <div class="bg-gray-800 border-t border-gray-700 p-2 overflow-auto">
      <TradeLog />
    </div>

    <!-- Barra lateral derecha con pares -->
    <div class="row-span-3 bg-gray-800 border-l border-gray-700 p-2 overflow-y-auto">
      <PairList @pair-selected="handlePairChange" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// 🔘 Par de monedas actualmente seleccionado (por defecto BTC/USDT)
const selectedPair = ref('BTCUSDT')

// ⏱️ Timeframe actual seleccionado (por defecto 1 minuto)
const selectedTimeframe = ref('1m')

// 📊 Datos crudos de velas obtenidos de la API de Binance
const rawCandleData = ref([])

/**
 * 📡 Función para obtener datos de velas desde Binance según par y timeframe
 * @param symbol - Par de monedas (ej. BTCUSDT)
 * @param interval - Intervalo de tiempo (ej. 1m, 5m, 1h)
 */
async function fetchBinanceData(symbol: string, interval: string) {
  try {
    const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=100`
    const res = await axios.get(url)
    rawCandleData.value = res.data // Guardamos los datos recibidos
  } catch (e) {
    console.error('Error fetching Binance data:', e)
  }
}

/**
 * 🟦 Manejador de cambio de par (llamado desde el componente PairList)
 * Actualiza el par seleccionado y vuelve a pedir los datos.
 */
function handlePairChange(pair: string) {
  selectedPair.value = pair
  fetchBinanceData(pair, selectedTimeframe.value)
}

// 🚀 Obtener datos iniciales al cargar la vista por primera vez
fetchBinanceData(selectedPair.value, selectedTimeframe.value)

/**
 * ⬛ Manejador de cambio de timeframe (llamado desde el componente Timeframes)
 * Actualiza el timeframe y vuelve a pedir los datos.
 */
function handleTimeframeChange(tf: string) {
  console.log('📥 Nuevo timeframe recibido en BacktestingView:', tf)
  selectedTimeframe.value = tf
  fetchBinanceData(selectedPair.value, tf)
}

import Chart from '@/components/Chart.vue'
import Controls from '@/components/Controls.vue'
import TradeLog from '@/components/TradeLog.vue'
import Timeframes from '@/components/TimeFrames.vue'
import PairList from '@/components/PairList.vue'
import DrawingTools from '@/components/DrawingTools.vue'
</script>
