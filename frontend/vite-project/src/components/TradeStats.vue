<template>
  <div>
    <n-button
      @click="toggleStats"
      secondary
      strong
      size="small"
      class="stats-button"
    >
     Estadísticas
    </n-button>

    <n-drawer
      v-model:show="showStats"
      placement="left"
      width="350"
      :style="{ backgroundColor: '#1e1e1e', color: 'white' }"
    >
      <template #header>
        Indicadores de rendimiento
      </template>

      <div v-if="trades.length > 0" class="stats-content">
        <ul>
          <li><strong>Total de operaciones:</strong> {{ trades.length }}</li>
          <li><strong>Win Rate:</strong> {{ winRate.toFixed(2) }}%</li>
          <li><strong>Loss Rate:</strong> {{ lossRate.toFixed(2) }}%</li>
          <li><strong>PnL Total:</strong> {{ totalPnL.toFixed(2) }} USDT</li>
          <li><strong>ROI Promedio:</strong> {{ avgRoi.toFixed(2) }}%</li>
          <li><strong>Ganancia media:</strong> {{ avgWin.toFixed(2) }} USDT</li>
          <li><strong>Pérdida media:</strong> {{ avgLoss.toFixed(2) }} USDT</li>
        </ul>
      </div>

      <div v-else>
        Aún no hay operaciones cerradas.
      </div>
    </n-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { NButton, NDrawer } from 'naive-ui'

const user = useUserStore()
const showStats = ref(false)

function toggleStats() {
  user.fetchClosedTrades()
  showStats.value = !showStats.value
}

const trades = computed(() => user.closedTrades)
const wins = computed(() => trades.value.filter(t => t.pnl > 0))
const losses = computed(() => trades.value.filter(t => t.pnl < 0))

const winRate = computed(() => (wins.value.length / trades.value.length) * 100 || 0)
const lossRate = computed(() => (losses.value.length / trades.value.length) * 100 || 0)
const totalPnL = computed(() => trades.value.reduce((sum, t) => sum + t.pnl, 0))
const avgRoi = computed(() => trades.value.reduce((sum, t) => sum + t.roi, 0) / trades.value.length || 0)
const avgWin = computed(() => wins.value.reduce((sum, t) => sum + t.pnl, 0) / wins.value.length || 0)
const avgLoss = computed(() => losses.value.reduce((sum, t) => sum + t.pnl, 0) / losses.value.length || 0)

const profitFactor = computed(() => {
  const winSum = wins.value.reduce((sum, t) => sum + t.pnl, 0)
  const lossSum = losses.value.reduce((sum, t) => sum + t.pnl, 0)
  return lossSum !== 0 ? (winSum / Math.abs(lossSum)).toFixed(2) : '∞'
})
</script>

<style scoped>

</style>
