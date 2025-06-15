<template>
  <div class="h-screen w-screen grid grid-cols-[60px_1fr_300px] grid-rows-[auto_1fr] bg-gray-900 text-white">
    <div class="row-span-2 bg-gray-800 border-r border-gray-700 p-2 flex flex-col gap-2">
      <DrawingTools />
    </div>

    <div class="col-span-1 bg-gray-900 border-b border-gray-800 p-2 flex items-center justify-start gap-4">
      <Timeframes @update:timeframe="handleTimeframeChange" />
      <button @click="toggleBacktestingMode" class="bg-blue-600 px-4 py-2 rounded text-white">
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
      <div class="absolute top-2 right-4 z-10 text-white text-lg font-bold bg-gray-800 px-4 py-1 rounded shadow">
        Balance: {{ balance.toFixed(2) }} USDT
      </div>
      <Chart
        :timeframe="selectedTimeframe"
        :symbol="selectedPair"
        :backtesting-start-index="backtestingStartIndex"
        :is-backtesting="isBacktesting"
        :current-index="currentIndex"
        :selection-mode="isSelectingStart"
        @select-start="handleBacktestingStart"
        @update:currentIndex="val => currentIndex = val"
        @update:currentPrice="val => currentPrice = val"
        @update:currentCandle="val => currentCandle = val"
      />
    </div>

    <div class="row-span-2 bg-gray-800 border-l border-gray-700 p-2 overflow-y-auto">
      <PairList @pair-selected="handlePairChange" />
    </div>

    <div>
      <TradePanel
        :balance="balance"
        :currentPrice="currentPrice"
        :canTrade="backtestingStartIndex !== null"
        @open-trade="handleOpenTrade"
      />
    </div>

    <div class="open-positions">
      <OpenPosition
        v-for="position in openPositions"
        :key="position.id"
        :form="position"
        :symbol="selectedPair"
        :currentPrice="currentPrice"
        :currentCandle="currentCandle"
        @close="(pnl, closePrice) => handleClosePosition(position.id, pnl, closePrice)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import Chart from '@/components/Chart.vue'
import Controls from '@/components/Controls.vue'
import Timeframes from '@/components/TimeFrames.vue'
import PairList from '@/components/PairList.vue'
import DrawingTools from '@/components/DrawingTools.vue'
import TradePanel from '@/components/TradePanel.vue'
import OpenPosition from '@/components/OpenPositions.vue'

const selectedPair = ref('BTCUSDT')
const selectedTimeframe = ref('1m')
const rawCandleData = ref<any[]>([])
const currentPrice = ref(0)
const currentCandle = ref({ high: 0, low: 0 })

const isBacktesting = ref(false)
const isSelectingStart = ref(false)
const backtestingStartIndex = ref<number | null>(null)
const currentIndex = ref(0)
const isPlaying = ref(false)
const playSpeed = ref(500)

let baseBalance = 1000
const balance = ref(baseBalance)

const openPositions = ref<any[]>([])

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
  // Resetear el punto de inicio y la vela actual
  backtestingStartIndex.value = index
  currentIndex.value = index
  isSelectingStart.value = false

  // Cerrar todas las operaciones abiertas sin afectar el balance
  openPositions.value = []
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
      checkForAutoClose()
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
  if (currentIndex.value < rawCandleData.value.length - 1) {
    currentIndex.value++
    checkForAutoClose()
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

function handleOpenTrade(trade: any) {
  openPositions.value.push({
    ...trade,
    id: Date.now(),
    active: trade.orderType === 'market' // market se activa de inmediato
  })
}

function handleClosePosition(id: number, pnl: number, closePrice: number) {
  const index = openPositions.value.findIndex(pos => pos.id === id)
  if (index !== -1) {
    openPositions.value.splice(index, 1)
    baseBalance += pnl
    if (baseBalance < 0) baseBalance = 0
    balance.value = baseBalance
  }
}

function checkForAutoClose() {
  const { high, low } = currentCandle.value

  for (const pos of [...openPositions.value]) {
    if (!pos.active) continue

    const assetAmount = pos.volume / pos.entryPrice
    const maxLoss = -pos.volume
    let closePrice: number | null = null
    let pnl = 0

    // Check SL/TP
    if (pos.stopLoss) {
      const hitSL =
        (pos.side === 'buy' && low <= pos.stopLoss) ||
        (pos.side === 'sell' && high >= pos.stopLoss)
      if (hitSL) closePrice = pos.stopLoss
    }

    if (!closePrice && pos.takeProfit) {
      const hitTP =
        (pos.side === 'buy' && high >= pos.takeProfit) ||
        (pos.side === 'sell' && low <= pos.takeProfit)
      if (hitTP) closePrice = pos.takeProfit
    }

    // Check liquidación por pérdida = volumen total
    const diff = currentPrice.value - pos.entryPrice
    const rawPnl = pos.side === 'buy'
      ? diff * assetAmount
      : -diff * assetAmount
    const leveragedPnl = rawPnl * pos.leverage

    if (!closePrice && leveragedPnl <= maxLoss) {
      closePrice = pos.side === 'buy'
        ? pos.entryPrice - (pos.volume / (assetAmount * pos.leverage))
        : pos.entryPrice + (pos.volume / (assetAmount * pos.leverage))
    }

    if (closePrice !== null) {
      const finalDiff = closePrice - pos.entryPrice
      const finalPnl = pos.side === 'buy'
        ? finalDiff * assetAmount * pos.leverage
        : -finalDiff * assetAmount * pos.leverage

      handleClosePosition(pos.id, finalPnl, closePrice)
    }
  }
}

fetchBinanceData(selectedPair.value, selectedTimeframe.value)
</script>

<style scoped>
.open-positions {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  z-index: 999;
}
</style>
