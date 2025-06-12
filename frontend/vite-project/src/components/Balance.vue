<template>
  <div class="balance-panel">
    <div class="panel-header">
      <span class="title">Saldo Inicial</span>
      <n-button size="small" tertiary @click="toggleBalance">
        {{ showBalance ? 'Cerrar' : 'Abrir' }}
      </n-button>
    </div>

    <n-collapse-transition :show="showBalance">
      <div class="balance-form">
        <n-form label-placement="left">
          <n-form-item label="Saldo Disponible (USDT)">
            <n-input-number
              v-model:value="balance"
              :min="10"
              :max="1000000"
            />
          </n-form-item>
          <n-button type="primary" block @click="applyBalance">
            Establecer Saldo
          </n-button>
        </n-form>
      </div>
    </n-collapse-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  NButton,
  NCollapseTransition,
  NForm,
  NFormItem,
  NInputNumber
} from 'naive-ui'

const showBalance = ref(false)
const balance = ref(1000)
const emit = defineEmits<{
  (e: 'set-balance', value: number): void
}>()

function toggleBalance() {
  showBalance.value = !showBalance.value
}

function applyBalance() {
  emit('set-balance', balance.value)
  showBalance.value = false
}
</script>

<style scoped>
/* Forzar color blanco en texto de Naive UI */
:deep(.n-form-item-label),
:deep(.n-input-number .n-input__input),
:deep(.n-button__content) {
  color: white !important;
}
.balance-panel {
  background-color: #1e1e1e;
  color: white;
  border-radius: 12px;
  padding: 1.2rem;
  max-width: 380px;
  margin: 2rem auto;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.title {
  font-weight: bold;
  font-size: 1.15rem;
}
.balance-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
