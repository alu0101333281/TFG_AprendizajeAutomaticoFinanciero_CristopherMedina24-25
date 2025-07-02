<template>
  <div class="position-card" :class="form.side">
    <div class="summary" @click="toggleDetails">
      <div class="header">
        <strong>{{ symbol }}</strong>
        <span @click.stop="showConfirm = true" class="close">×</span>
      </div>
      <div class="entry">
        Entrada: {{ form.entryPrice?.toFixed(2) || '-' }} USDT
      </div>
      <div class="details">
        <div>
          Volumen: {{ (form.volume * (form.leverage || 1)).toFixed(2) }} USDT
        </div>
        <div>
          ROI:
          <span :class="roi >= 0 ? 'profit' : 'loss'">
            {{ roi.toFixed(2) }}%
          </span>
        </div>
        <div>
          PnL:
          <span :class="roi >= 0 ? 'profit' : 'loss'">
            {{ pnl.toFixed(2) }} USDT
          </span>
        </div>
      </div>
    </div>

    <n-collapse-transition :show="showDetails">
      <div class="advanced">
        <n-form label-placement="left" size="small">
          <n-form-item label="Stop Loss">
            <n-input-number
              v-model:value="form.stopLoss"
              :min="0"
              :status="stopLossInvalid ? 'error' : undefined"
            />
          </n-form-item>
          <n-form-item label="Take Profit">
            <n-input-number
              v-model:value="form.takeProfit"
              :min="0"
              :status="takeProfitInvalid ? 'error' : undefined"
            />
          </n-form-item>
        </n-form>
      </div>
    </n-collapse-transition>

    <n-modal
      v-model:show="showConfirm"
      preset="dialog"
      title="Cerrar operación"
      positive-text="Sí"
      negative-text="No"
      @positive-click="emit('close', pnl, currentPrice)"
      @negative-click="showConfirm = false"
    >
      ¿Estás seguro de que deseas cerrar esta operación?
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import {
  NForm,
  NFormItem,
  NInputNumber,
  NCollapseTransition,
  NModal
} from 'naive-ui'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()

const props = defineProps<{
  form: {
    side: 'buy' | 'sell'
    orderType: 'market' | 'limit'
    entryPrice: number
    volume: number
    stopLoss?: number | null
    takeProfit?: number | null
    leverage: number
    active: boolean
  }
  symbol: string
  currentPrice: number
  currentCandle: { high: number; low: number }
}>()

const emit = defineEmits<{
  (e: 'close', pnl: number, closePrice: number): void
}>()

const showConfirm = ref(false)
const showDetails = ref(false)

function toggleDetails() {
  showDetails.value = !showDetails.value
}

// Activar orden limit cuando el precio pase por el punto de entrada
watch(() => [props.form.active, props.currentCandle], () => {
  if (!props.form.active && props.form.orderType === 'limit') {
    const entry = props.form.entryPrice
    const { high, low } = props.currentCandle
    const shouldActivate =
      (props.form.side === 'buy' && low <= entry) ||
      (props.form.side === 'sell' && high >= entry)

    if (shouldActivate) {
      props.form.active = true
    }
  }

  if (props.form.active) {
    const { high, low } = props.currentCandle
    const stop = props.form.stopLoss
    const take = props.form.takeProfit
    const entry = props.form.entryPrice
    const amount = props.form.volume / entry
    let closePrice: number | null = null

    if (props.form.side === 'buy') {
      if (stop && low <= stop) closePrice = stop
      else if (take && high >= take) closePrice = take
    } else {
      if (stop && high >= stop) closePrice = stop
      else if (take && low <= take) closePrice = take
    }

    if (closePrice !== null) {
      const priceDiff = closePrice - entry
      const profit = props.form.side === 'buy'
        ? priceDiff * amount
        : -priceDiff * amount
      const leveragedPnl = profit * props.form.leverage
      emit('close', leveragedPnl, closePrice)
    }
  }
})

// Calcula la cantidad de activo comprado: volumen / precio de entrada
const assetAmount = computed(() => {
  return props.form.volume / props.form.entryPrice
})

// PnL basado en la diferencia porcentual del activo multiplicado por leverage y volumen
const pnl = computed(() => {
  if (!props.form.active) return 0
  const diff = props.currentPrice - props.form.entryPrice
  const basePnl = props.form.side === 'buy'
    ? diff * assetAmount.value
    : -diff * assetAmount.value

  return basePnl * props.form.leverage
})

// ROI = (pnl / inversión inicial) * 100
const roi = computed(() => {
  if (!props.form.active) return 0
  const investment = props.form.volume
  return (pnl.value / investment) * 100
})

// Validaciones SL y TP
const stopLossInvalid = computed(() =>
  props.form.stopLoss != null &&
  ((props.form.side === 'buy' && props.form.stopLoss >= props.currentPrice) ||
   (props.form.side === 'sell' && props.form.stopLoss <= props.currentPrice))
)

const takeProfitInvalid = computed(() =>
  props.form.takeProfit != null &&
  ((props.form.side === 'buy' && props.form.takeProfit <= props.currentPrice) ||
   (props.form.side === 'sell' && props.form.takeProfit >= props.currentPrice))
)
</script>

<style scoped>
.position-card {
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-left: 4px solid;
  padding: 1rem;
  width: 280px;
  border-radius: 10px;
  color: white;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}
.position-card:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}
.position-card.buy {
  border-left-color: #4caf50;
}
.position-card.sell {
  border-left-color: #f44336;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close {
  cursor: pointer;
  color: gray;
  font-size: 1.2rem;
}
.details {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
.advanced {
  margin-top: 1rem;
  padding-top: 0.5rem;
  border-top: 1px solid #555;
}
:deep(.n-form-item-label) {
  color: white !important;
}
:deep(.n-input-number .n-input__input) {
  color: black !important;
  background-color: white !important;
}
.profit {
  color: #4caf50;
}
.loss {
  color: #f44336;
}
</style>
