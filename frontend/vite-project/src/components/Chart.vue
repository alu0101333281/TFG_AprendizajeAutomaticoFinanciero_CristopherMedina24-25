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
  backtestingStartIndex: { type: Number, required: false, default: null },
  selectedTool: { type: String, default: null }
})

const emit = defineEmits<{
  (e: 'select-start', index: number): void
  (e: 'update:currentIndex', index: number): void
  (e: 'update:currentPrice', value: number): void
  (e: 'update:currentCandle', value: CandlestickData): void
  (e: 'clear-tool'): void
}>()

const drawingClicks = ref<{ time: number; price: number }[]>([])

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

function handleDrawClick(param: any) {
  if (!param.time || !param.seriesPrices) return
  if (!candleSeries || !param.seriesPrices.has(candleSeries)) return
  const price = param.seriesPrices.get(candleSeries) as number
  const time = param.time

  drawingClicks.value.push({ time, price })

  const drawLine = (
  points: { time: number; price: number }[],
  color = '#f0f'
) => {
  chart?.addLineSeries({ color, lineWidth: 2 }).setData(
    points.map(p => ({
      time: p.time as UTCTimestamp,
      value: p.price
    }))
  )
}

  if (props.selectedTool === 'horizontal') {
    drawLine([
      { time: allCandles[0]?.time || time, price },
      { time: allCandles[allCandles.length - 1]?.time || time + 100, price }
    ], '#4caf50')
    finishDrawing()
  } else if (props.selectedTool === 'vertical') {
    drawLine([
      { time, price: price - 50 },
      { time, price: price + 50 }
    ], '#2196f3')
    finishDrawing()
  } else if (props.selectedTool === 'line' && drawingClicks.value.length === 2) {
    drawLine(drawingClicks.value, '#ff9800')
    finishDrawing()
  } else if (props.selectedTool === 'channel' && drawingClicks.value.length === 2) {
    const [p1, p2] = drawingClicks.value
    drawLine([p1, p2], '#ab47bc')
    drawLine([{ ...p1, price: p1.price + 50 }, { ...p2, price: p2.price + 50 }], '#ab47bc')
    finishDrawing()
  }
}


function finishDrawing() {
  drawingClicks.value = []
  emit('clear-tool')
}

async function initializeChart() {
  if (!chartContainer.value) return

  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: chartContainer.value.clientHeight,
    layout: { background: { color: '#000' }, textColor: '#ccc' },
    grid: { vertLines: { color: '#444' }, horzLines: { color: '#444' } },
    timeScale: { timeVisible: true, rightOffset: 5 },
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
    } else if (props.selectedTool) {
      handleDrawClick(param)
    }
  })

  window.addEventListener('resize', resizeChart)
  resizeChart()
}

function updateDisplayedCandles() {
  if (!candleSeries) return

  if (props.isBacktesting && props.backtestingStartIndex !== null) {
    candleSeries.setData(allCandles.slice(0, props.currentIndex + 1))
  } else {
    candleSeries.setData(allCandles)
  }

  if (props.isBacktesting && allCandles.length > props.currentIndex) {
    const candle = allCandles[props.currentIndex]
    if (candle) {
      emit('update:currentPrice', candle.close)
      emit('update:currentCandle', candle)
    }
  }
}

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

