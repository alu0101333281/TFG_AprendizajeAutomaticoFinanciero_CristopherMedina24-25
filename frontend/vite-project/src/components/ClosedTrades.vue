<template>
  <div>
    <n-button
      @click="toggleClosedTrades"
      secondary
      strong
      size="small"
      class="custom-button"
    >
      Historial de trades
    </n-button>

    <n-drawer
      v-model:show="showClosed"
      placement="right"
      width="400"
      :style="{ backgroundColor: '#1e1e1e', color: 'white' }"
    >
      <template #header>
        <span style="color: white;">Historial de operaciones cerradas</span>
      </template>

      <div v-if="user.closedTrades.length === 0" style="color: white;">
        No hay operaciones cerradas aún.
      </div>

      <n-list
        v-else
        bordered
        :style="{ backgroundColor: '#1e1e1e' }"
      >
        <n-list-item
          v-for="(trade, index) in user.closedTrades.slice().reverse()"
          :key="index"
          @click="selectTrade(trade)"
          style="cursor: pointer; color: white; border-bottom: 1px solid #333;"
        >
          <div>
            <strong>{{ trade.symbol }}</strong> -
            {{ trade.side.toUpperCase() }} |
            <span :class="trade.pnl >= 0 ? 'profit' : 'loss'">
              {{ trade.pnl.toFixed(2) }} USDT
            </span>
          </div>
          <div class="timestamp">
            Cerrada el {{ new Date(trade.exit_time).toLocaleString() }}
          </div>
        </n-list-item>
      </n-list>
    </n-drawer>

    <n-modal
      v-model:show="showModal"
      preset="dialog"
      title="Detalle de la operación"
      :style="{ backgroundColor: '#1e1e1e', color: 'white' }"
      @close="closeModal"
    >
      <div v-if="selectedTrade">
        <p><strong>Symbol:</strong> {{ selectedTrade.symbol }}</p>
        <p><strong>Tipo:</strong> {{ selectedTrade.side }}</p>
        <p><strong>Entrada:</strong> {{ selectedTrade.entry_price }} USDT</p>
        <p><strong>Salida:</strong> {{ selectedTrade.exit_price }} USDT</p>
        <p><strong>Volumen:</strong> {{ selectedTrade.volume }} USDT</p>
        <p><strong>Apalancamiento:</strong> x{{ selectedTrade.leverage }}</p>
        <p><strong>ROI:</strong> {{ selectedTrade.roi.toFixed(2) }}%</p>
        <p><strong>Ganancia/Pérdida:</strong>
          <span :class="selectedTrade.pnl >= 0 ? 'profit' : 'loss'">
            {{ selectedTrade.pnl.toFixed(2) }} USDT
          </span>
        </p>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  NButton,
  NDrawer,
  NList,
  NListItem,
  NModal
} from 'naive-ui'

const user = useUserStore()
const showClosed = ref(false)
const selectedTrade = ref<any>(null)
const showModal = ref(false)

function toggleClosedTrades() {
  user.fetchClosedTrades()
  showClosed.value = !showClosed.value
}

function selectTrade(trade: any) {
  selectedTrade.value = trade
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedTrade.value = null
}
</script>

