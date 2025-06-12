<template>
  <div ref="chartContainer" class="chart-container" />
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, nextTick, watch } from 'vue'
import {
  createChart,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  UTCTimestamp,
  CrosshairMode
} from 'lightweight-charts'

const chartContainer = ref<HTMLElement | null>(null)
let chart: IChartApi | null = null
let candleSeries: ISeriesApi<'Candlestick'> | null = null
let allCandles: CandlestickData[] = []

const props = defineProps({
  timeframe: { type: String, required: true },
  symbol: { type: String, required: true },
  isBacktesting: { type: Boolean, required: true },
  currentIndex: { type: Number, required: false, default: 0 },
  selectionMode: { type: Boolean, required: false, default: false },
  backtestingStartIndex: { type: Number, required: false, default: null }
})

const emit = defineEmits<{
  (e: 'select-start', index: number): void
  (e: 'update:currentIndex', index: number): void
  (e: 'update:currentPrice', value: number): void
}>()

async function fetchBinanceCandles(symbol: string, interval: string): Promise<CandlestickData[]> {
  const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=500`
  const response = await fetch(url)
  const raw = await response.json()
  return raw.map((item: any) => ({
    time: Math.floor(item[0] / 1000) as UTCTimestamp,
    open: parseFloat(item[1]),
    high: parseFloat(item[2]),
    low: parseFloat(item[3]),
    close: parseFloat(item[4])
  }))
}

function resizeChart() {
  if (chart && chartContainer.value) {
    chart.resize(chartContainer.value.clientWidth, chartContainer.value.clientHeight)
  }
}

async function initializeChart() {
  if (!chartContainer.value) return

  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: chartContainer.value.clientHeight,
    layout: { background: { color: '#000' }, textColor: '#ccc' },
    grid: { vertLines: { color: '#444' }, horzLines: { color: '#444' } },
    timeScale: {
      timeVisible: true,
      rightOffset: 5
    },
    crosshair: { mode: CrosshairMode.Normal },
    interaction: {
      mouseWheel: { scale: 1.5 },
      pinchZoom: true,
      axesDrag: false
    }
  })

  candleSeries = chart.addCandlestickSeries({
    upColor: '#26a69a', borderUpColor: '#26a69a', wickUpColor: '#26a69a',
    downColor: '#ef5350', borderDownColor: '#ef5350', wickDownColor: '#ef5350'
  })

  allCandles = await fetchBinanceCandles(props.symbol, props.timeframe)
  updateDisplayedCandles()

  chart.subscribeClick(param => {
    if (props.selectionMode && param.time && typeof param.time === 'number') {
      const index = allCandles.findIndex(c => c.time === param.time)
      if (index !== -1) emit('select-start', index)
    }
  })

  window.addEventListener('resize', resizeChart)
  resizeChart()
}

function updateDisplayedCandles() {
  if (candleSeries) {
    if (props.isBacktesting && props.backtestingStartIndex !== null) {
      candleSeries.setData(allCandles.slice(0, props.currentIndex + 1))
    } else {
      candleSeries.setData(allCandles)
    }
  }

  // Emitir el precio actual si aplica
  if (props.isBacktesting && allCandles.length > props.currentIndex) {
    const price = allCandles[props.currentIndex]?.close
    if (price) emit('update:currentPrice', price)
  }
}

// 🔁 Actualiza velas + emite precio actual cuando cambie índice
watch(() => [props.isBacktesting, props.currentIndex, props.backtestingStartIndex], updateDisplayedCandles)

watch(() => [props.timeframe, props.symbol], async () => {
  if (chart) {
    allCandles = await fetchBinanceCandles(props.symbol, props.timeframe)
    updateDisplayedCandles()
  }
})

onMounted(async () => {
  await nextTick()
  await initializeChart()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.remove()
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>
