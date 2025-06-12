<template>
  <div class="position-card" :class="form.side">
    <!-- Header + Entrada = zona de clic para expandir -->
    <div class="summary" @click="toggleDetails">
      <div class="header">
        <strong>{{ symbol }}</strong>
        <span @click.stop="showConfirm = true" class="close">×</span>
      </div>
      <div class="entry">Entrada: {{ form.entryPrice.toFixed(2) }} USDT</div>
      <div class="details">
        <div>Volumen: {{ form.volume }}</div>
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

    <!-- Detalles avanzados -->
    <n-collapse-transition :show="showDetails">
      <div class="advanced">
        <n-form label-placement="left" size="small">
          <n-form-item label="Stop Loss">
            <n-input-number v-model:value="form.stopLoss" :min="0" />
          </n-form-item>
          <n-form-item label="Take Profit">
            <n-input-number v-model:value="form.takeProfit" :min="0" />
          </n-form-item>
        </n-form>
        <n-button type="error" block size="small" @click.stop="showConfirm = true">
          Cerrar operación
        </n-button>
      </div>
    </n-collapse-transition>

    <!-- Confirmación -->
    <n-modal
      v-model:show="showConfirm"
      preset="dialog"
      title="Cerrar operación"
      positive-text="Sí"
      negative-text="No"
      @positive-click="$emit('close')"
      @negative-click="showConfirm = false"
    >
      ¿Estás seguro de que deseas cerrar esta operación?
    </n-modal>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import { NForm, NFormItem, NInputNumber, NButton, NModal, NCollapseTransition } from 'naive-ui'

const props = defineProps<{
  form: {
    side: 'buy' | 'sell'
    entryPrice: number
    volume: number
    stopLoss?: number | null
    takeProfit?: number | null
  }
  symbol: string
  currentPrice: number
}>()

const showConfirm = ref(false)
const showDetails = ref(false)

function toggleDetails() {
  showDetails.value = !showDetails.value
}

const pnl = computed(() => {
  const diff = props.currentPrice - props.form.entryPrice
  return props.form.side === 'buy'
    ? diff * props.form.volume
    : -diff * props.form.volume
})

const roi = computed(() => {
  const base = props.form.entryPrice * props.form.volume
  return (pnl.value / base) * 100
})
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
/* ✅ Forzar color blanco en etiquetas Naive UI */
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
