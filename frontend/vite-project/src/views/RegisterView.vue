<template>
  <div class="register-container">
    <h2>Registrarse</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Usuario</label>
        <input id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input id="password" type="password" v-model="form.password" required />
      </div>
<div class="form-group">
  <label for="balance">Balance inicial</label>
  <n-input-number
    id="balance"
    v-model:value="form.balance"
    :min="1"
    placeholder="Ej: 1000"
    class="balance-input"
  />
</div>

      <button type="submit">Registrarse</button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p>
      ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  username: '',
  password: '',
  balance: 0
})

const error = ref('')

async function handleRegister() {
    // Validación manual del balance
  if (!form.value.balance || form.value.balance < 1) {
    error.value = 'Debes ingresar un balance inicial válido (mínimo 1 USDT)'
    return
  }
  try {
    await axios.post('http://localhost:8080/users/register', form.value)
    router.push('/login')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al registrarse'
  }
}
</script>

<style scoped>
/* Caja del formulario */
.register-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: #1e1e1e;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px #000;
}

/* Etiquetas + inputs estándar */
.form-group {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  background: #2a2a2a;
  color: white;
  border: 1px solid #444;
  border-radius: 5px;
  caret-color: white;
}

button {
  width: 100%;
  padding: 0.5rem;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background: #369f6e;
}

.error {
  color: #f44336;
  margin-top: 0.5rem;
}

:deep(.n-input-number) {
  width: 100%;
}

:deep(.n-input-number .n-input__input) {
  background-color: #2a2a2a !important;
  color: white !important;
  border: 1px solid #444 !important;
  border-radius: 5px !important;
  caret-color: white !important;
  opacity: 1 !important;
}

:deep(.n-input-number .n-input__input[readonly]) {
  background-color: #2a2a2a !important;
  color: white !important;
  opacity: 1 !important;
}

:deep(.n-input__placeholder) {
  color: #bbb !important;
  opacity: 1 !important;
}

:deep(.n-input-number .n-input__suffix) {
  color: white !important;
}

:deep(.n-input.n-input--focus .n-input__input) {
  box-shadow: 0 0 0 2px #42b88366;
}
</style>

