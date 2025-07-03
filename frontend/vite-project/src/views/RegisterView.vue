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
  balance: 1000
})

const error = ref('')

async function handleRegister() {
  try {
    await axios.post('http://localhost:8080/users/register', form.value)
    router.push('/login')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al registrarse'
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: #1e1e1e;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px #000;
}

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
}

button {
  width: 100%;
  padding: 0.5rem;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #369f6e;
}

.error {
  color: #f44336;
  margin-top: 0.5rem;
}

.balance-wrapper {
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

:deep(.n-form-item-label) {
  color: white !important;
  width: 100% !important;
  text-align: center;
}

:deep(.n-input-number .n-input__input) {
  color: white !important;
  background-color: #2a2a2a !important;
  text-align: center;
  caret-color: white !important;
}

:deep(.n-input) {
  background-color: #2a2a2a !important;
  border: 1px solid #444 !important;
  border-radius: 5px !important;
}
</style>
