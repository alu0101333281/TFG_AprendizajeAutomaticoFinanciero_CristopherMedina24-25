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

// ✅ Props para timeframe y datos crudos estilo Binance
const props = defineProps({
  timeframe: {
    type: String,
    required: true
  },
  rawData: {
    type: Array as () => any[], // Esperamos un array de arrays de datos de velas tipo Binance
    required: true
  }
})

// ✅ Convierte datos de Binance a formato compatible con lightweight-charts
function transformRawToCandlestickData(raw: any[]): CandlestickData[] {
  return raw.map(item => ({
    time: Math.floor(item[0] / 1000) as UTCTimestamp,
    open: parseFloat(item[1]),
    high: parseFloat(item[2]),
    low: parseFloat(item[3]),
    close: parseFloat(item[4])
  }))
}

// ✅ Agrupa datos de 1m a 5m, 15m, 1h, etc.
function groupCandles(data: CandlestickData[], intervalInMinutes: number): CandlestickData[] {
  const grouped: CandlestickData[] = []

  for (let i = 0; i < data.length; i += intervalInMinutes) {
    const group = data.slice(i, i + intervalInMinutes)
    if (group.length === 0) continue

    const open = group[0].open
    const close = group[group.length - 1].close
    const high = Math.max(...group.map(d => d.high))
    const low = Math.min(...group.map(d => d.low))
    const time = group[0].time

    grouped.push({ time, open, high, low, close })
  }

  return grouped
}

// ✅ Calcula los datos procesados según timeframe
function getDataForTimeframe(timeframe: string, raw: any[]): CandlestickData[] {
  const timeframes: Record<string, number> = {
    '1m': 1,
    '5m': 5,
    '15m': 15,
    '1h': 60,
    '4h': 240,
    '1D': 1440
  }

  const interval = timeframes[timeframe] || 1
  const baseCandles = transformRawToCandlestickData(raw)
  return interval === 1 ? baseCandles : groupCandles(baseCandles, interval)
}

// ✅ Redimensionar gráfico si cambia tamaño ventana
const resizeChart = () => {
  if (chart && chartContainer.value) {
    chart.resize(
      chartContainer.value.clientWidth,
      chartContainer.value.clientHeight
    )
  }
}

// ✅ Inicialización del gráfico
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
    wickDownColor: '#ef5350',
  })

  if (props.rawData.length) {
    const formatted = getDataForTimeframe(props.timeframe, props.rawData)
    candleSeries.setData(formatted)
  }

  window.addEventListener('resize', resizeChart)
  resizeChart()
})

// ✅ Reaccionar a cambios en timeframe o datos
watch(() => [props.timeframe, props.rawData], ([newTF, newRaw]) => {
  if (candleSeries && newRaw.length) {
    const formatted = getDataForTimeframe(newTF, newRaw)
    candleSeries.setData(formatted)
  }
}, { deep: true })

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
