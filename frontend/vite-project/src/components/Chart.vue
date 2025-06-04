<template>
    <div ref="chartContainer" class="chart-container" />
  </template>
  
  <script setup lang="ts">
  import { onMounted, onBeforeUnmount, ref, nextTick } from 'vue'
  import { createChart } from 'lightweight-charts'
  
  const chartContainer = ref<HTMLElement | null>(null)
  let chart: ReturnType<typeof createChart> | null = null
  
  const resizeChart = () => {
    if (chart && chartContainer.value) {
      chart.resize(
        chartContainer.value.clientWidth,
        chartContainer.value.clientHeight
      )
    }
  }
  
  onMounted(async () => {
    await nextTick() // Esperar a que el contenedor tenga altura real
    if (!chartContainer.value) return
  
    console.log('✅ chartContainer montado', chartContainer.value)
    console.log('🧪 Container size:', chartContainer.value.clientWidth, chartContainer.value.clientHeight)
  
    chart = createChart(chartContainer.value, {
      width: chartContainer.value.clientWidth,
      height: chartContainer.value.clientHeight,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#000000',
      },
      grid: {
        vertLines: { color: '#e0e0e0' },
        horzLines: { color: '#e0e0e0' },
      },
    })
  
    console.log('✅ Gráfico creado:', chart)
  
    const candleSeries = chart.addCandlestickSeries()
    console.log('✅ Serie creada:', candleSeries)
  
    candleSeries.setData([
      { time: '2025-04-01', open: 100, high: 110, low: 95, close: 105 },
      { time: '2025-04-02', open: 105, high: 115, low: 100, close: 110 },
      { time: '2025-04-03', open: 110, high: 120, low: 108, close: 115 },
    ])
  
    window.addEventListener('resize', resizeChart)
    resizeChart()
  })
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', resizeChart)
  })
  </script>
  
  <style scoped>
  .chart-container {
    width: 100%;
    height: 100%;
    min-height: 400px; /* 👈 Clave para que siempre tenga algo de altura */
  }
  </style>
  
  