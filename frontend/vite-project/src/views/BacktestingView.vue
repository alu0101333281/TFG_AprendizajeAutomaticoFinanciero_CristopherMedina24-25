<template>
  <div class="h-screen w-screen grid grid-cols-[60px_1fr_300px] grid-rows-[auto_1fr] bg-gray-900 text-white">
    <div class="row-span-2 bg-gray-800 border-r border-gray-700 p-2 flex flex-col gap-2">
      <DrawingTools />
    </div>

    <div class="col-span-1 bg-gray-900 border-b border-gray-800 p-2 flex items-center justify-start gap-4">
      <Timeframes @update:timeframe="handleTimeframeChange" />
      <button
        @click="toggleBacktestingMode"
        class="bg-blue-600 px-4 py-2 rounded text-white"
      >
        {{ isBacktesting ? 'Salir Backtesting' : 'Iniciar Backtesting' }}
      </button>

      <Controls
        v-if="isBacktesting"
        :is-playing="isPlaying"
        :play-speed="playSpeed"
        @toggle-play="togglePlay"
        @start-selection="activateSelectionMode"
        @next-candle="nextCandle"
        @prev-candle="prevCandle"
        @update:playSpeed="val => playSpeed = val"
      />
    </div>

    <div class="relative bg-black">
      <Chart
        :timeframe="selectedTimeframe"
        :symbol="selectedPair"
        :backtesting-start-index="backtestingStartIndex"
        :is-backtesting="isBacktesting"
        :current-index="currentIndex"
        :selection-mode="isSelectingStart"
        @select-start="handleBacktestingStart"
        @update:currentIndex="val => currentIndex = val"
      />
    </div>

    <div class="row-span-2 bg-gray-800 border-l border-gray-700 p-2 overflow-y-auto">
      <PairList @pair-selected="handlePairChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const selectedPair = ref('BTCUSDT')
const selectedTimeframe = ref('1m')
const rawCandleData = ref<any[]>([])

const isBacktesting = ref(false)
const isSelectingStart = ref(false)
const backtestingStartIndex = ref<number | null>(null)
const currentIndex = ref(0)
const isPlaying = ref(false)
const playSpeed = ref(500)

let intervalId: ReturnType<typeof setInterval> | null = null

function toggleBacktestingMode() {
  isBacktesting.value = !isBacktesting.value
  if (!isBacktesting.value) {
    stopPlayback()
    isSelectingStart.value = false
    backtestingStartIndex.value = null
    currentIndex.value = 0
  }
}

function activateSelectionMode() {
  isSelectingStart.value = true
}

function handleBacktestingStart(index: number) {
  backtestingStartIndex.value = index
  currentIndex.value = index
  isSelectingStart.value = false
}

function togglePlay() {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) startPlayback()
  else stopPlayback()
}

function startPlayback() {
  stopPlayback()
  intervalId = setInterval(() => {
    if (currentIndex.value < rawCandleData.value.length - 1) {
      currentIndex.value++
    } else {
      stopPlayback()
      isPlaying.value = false
    }
  }, playSpeed.value)
}

function stopPlayback() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

function nextCandle() {
  if (currentIndex.value < (rawCandleData.value.length - 1)) {
    currentIndex.value++
  }
}

function prevCandle() {
  if (currentIndex.value > (backtestingStartIndex.value || 0)) {
    currentIndex.value--
  }
}

async function fetchBinanceData(symbol: string, interval: string) {
  try {
    const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=500`
    const res = await axios.get(url)
    rawCandleData.value = res.data
  } catch (e) {
    console.error('Error fetching Binance data:', e)
  }
}

function handlePairChange(pair: string) {
  selectedPair.value = pair
  fetchBinanceData(pair, selectedTimeframe.value)
}

function handleTimeframeChange(tf: string) {
  selectedTimeframe.value = tf
  fetchBinanceData(selectedPair.value, tf)
}

fetchBinanceData(selectedPair.value, selectedTimeframe.value)

import Chart from '@/components/Chart.vue'
import Controls from '@/components/Controls.vue'
import Timeframes from '@/components/TimeFrames.vue'
import PairList from '@/components/PairList.vue'
import DrawingTools from '@/components/DrawingTools.vue'
</script>
