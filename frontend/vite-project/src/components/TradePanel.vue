<template>
  <div class="trade-panel">
    <div class="panel-header">
      <span class="title">Abrir Operación</span>
      <n-button size="small" tertiary @click="resetPanel">Volver</n-button>
    </div>

    <!-- Nivel 1: Compra o Venta -->
    <div v-if="!form.side" class="trade-form">
      <n-button block type="success" @click="selectSide('buy')">Comprar</n-button>
      <n-button block type="error" @click="selectSide('sell')">Vender</n-button>
    </div>

    <!-- Nivel 2: Mercado o Límite -->
    <div v-else-if="!form.orderType" class="trade-form">
      <n-button block type="primary" @click="selectOrderType('market')">Mercado</n-button>
      <n-button block type="warning" @click="selectOrderType('limit')">Límite</n-button>
    </div>

    <!-- Nivel 3: Formulario completo -->
    <div v-else class="trade-form">
      <n-form :model="form" label-placement="left">
        <!-- Mostrar tipo -->
        <n-form-item label="Operación">
          <span>{{ form.side === 'buy' ? 'Compra' : 'Venta' }} ({{ form.orderType }})</span>
        </n-form-item>

        <!-- Campo de precio -->
        <n-form-item label="Precio de Entrada (USDT)">
          <n-input-number
            v-if="form.orderType === 'limit'"
            v-model:value="form.entryPrice"
            :status="validateEntryPrice()"
            :min="0.01"
          />
          <n-input-number
            v-else
            :value="currentPrice"
            :readonly="true"
          />
        </n-form-item>

        <!-- Otros campos -->
        <n-form-item label="Stop Loss (USDT)">
          <n-input-number v-model:value="form.stopLoss" :min="0" />
        </n-form-item>

        <n-form-item label="Take Profit (USDT)">
          <n-input-number v-model:value="form.takeProfit" :min="0" />
        </n-form-item>

        <n-form-item label="Volumen (USDT)">
          <n-input-number v-model:value="form.volume" :min="1" />
        </n-form-item>

        <n-form-item label="Apalancamiento">
          <n-input-number v-model:value="form.leverage" :min="1" :max="100" />
        </n-form-item>

        <n-button type="primary" block @click="submitTrade">
          Ejecutar Operación
        </n-button>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInputNumber
} from 'naive-ui'

const props = defineProps<{
  currentPrice: number
  balance: number
}>()

const emit = defineEmits<{
  (e: 'open-trade', payload: Record<string, any>): void
}>()

const form = reactive<{
  side: 'buy' | 'sell' | null
  orderType: 'market' | 'limit' | null
  entryPrice: number | null
  stopLoss: number | null
  takeProfit: number | null
  volume: number
  leverage: number
}>({
  side: null,
  orderType: null,
  entryPrice: null,
  stopLoss: null,
  takeProfit: null,
  volume: 1,
  leverage: 1
})

function selectSide(side: 'buy' | 'sell') {
  form.side = side
}

function selectOrderType(type: 'market' | 'limit') {
  form.orderType = type
  if (type === 'market') {
    form.entryPrice = props.currentPrice
  } else {
    form.entryPrice = null
  }
}

function resetPanel() {
  form.side = null
  form.orderType = null
  form.entryPrice = null
  form.stopLoss = null
  form.takeProfit = null
  form.volume = 1
  form.leverage = 1
}

function submitTrade() {
  if (form.orderType === 'limit' && validateEntryPrice() === 'error') return

  emit('open-trade', {
    ...form,
    entryPrice: form.orderType === 'market' ? props.currentPrice : form.entryPrice
  })

  resetPanel()
}

function validateEntryPrice(): 'error' | undefined {
  if (form.orderType !== 'limit' || form.entryPrice == null) return undefined
  if (form.side === 'buy' && form.entryPrice >= props.currentPrice) return 'error'
  if (form.side === 'sell' && form.entryPrice <= props.currentPrice) return 'error'
  return undefined
}
</script>

<style scoped>
.trade-panel {
  background-color: #1e1e1e;
  color: white;
  border-radius: 10px;
  padding: 1rem;
  max-width: 360px;
  margin: auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.title {
  font-weight: bold;
  font-size: 1.1rem;
  color: white;
}

.trade-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Asegurar visibilidad de inputs */
:deep(.n-form-item-label),
:deep(.n-button__content),
:deep(.n-input-number .n-input__input) {
  color: white !important;
}
</style>
