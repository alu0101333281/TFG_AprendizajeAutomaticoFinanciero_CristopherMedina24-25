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
  UTCTimestamp
} from 'lightweight-charts'

const chartContainer = ref<HTMLElement | null>(null)
let chart: IChartApi | null = null
let candleSeries: ISeriesApi<'Candlestick'> | null = null

// Props: timeframe (1m, 5m...) y symbol (BTCUSDT, ETHUSDT, etc.)
const props = defineProps({
  timeframe: {
    type: String,
    required: true
  },
  symbol: {
    type: String,
    required: true
  }
})

// Convierte datos de Binance a formato lightweight-charts
function transformRawToCandlestickData(raw: any[]): CandlestickData[] {
  return raw.map(item => ({
    time: Math.floor(item[0] / 1000) as UTCTimestamp,
    open: parseFloat(item[1]),
    high: parseFloat(item[2]),
    low: parseFloat(item[3]),
    close: parseFloat(item[4])
  }))
}

// Fetch a Binance con símbolo y temporalidad
async function fetchBinanceCandles(symbol: string, interval: string): Promise<CandlestickData[]> {
  const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=500`
  const response = await fetch(url)
  const raw = await response.json()
  return transformRawToCandlestickData(raw)
}

// Resize chart al cambiar tamaño
const resizeChart = () => {
  if (chart && chartContainer.value) {
    chart.resize(
      chartContainer.value.clientWidth,
      chartContainer.value.clientHeight
    )
  }
}

// Inicialización
onMounted(async () => {
  await nextTick()
  if (!chartContainer.value) return

  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
    height: chartContainer.value.clientHeight,
    layout: {
      background: { color: '#ffffff' },
      textColor: '#000000'
    },
    grid: {
      vertLines: { color: '#e0e0e0' },
      horzLines: { color: '#e0e0e0' }
    },
    timeScale: {
      timeVisible: true,
      secondsVisible: false
    }
  })

  candleSeries = chart.addCandlestickSeries({
    upColor: '#26a69a',
    borderUpColor: '#26a69a',
    wickUpColor: '#26a69a',
    downColor: '#ef5350',
    borderDownColor: '#ef5350',
    wickDownColor: '#ef5350'
  })

  const candles = await fetchBinanceCandles(props.symbol, props.timeframe)
  candleSeries.setData(candles)

  window.addEventListener('resize', resizeChart)
  resizeChart()
})

// Reaccionar a cambios en timeframe o símbolo
watch(() => [props.timeframe, props.symbol], async ([newTF, newSymbol]) => {
  if (candleSeries) {
    const newCandles = await fetchBinanceCandles(newSymbol, newTF)
    candleSeries.setData(newCandles)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>
