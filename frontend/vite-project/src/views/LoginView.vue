<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Usuario</label>
        <input id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input id="password" type="password" v-model="form.password" required />
      </div>
      <button type="submit">Entrar</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p>
      ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
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
  password: ''
})

const error = ref('')

async function handleLogin() {
  try {
    const response = await axios.post('http://localhost:8080/users/login', form.value)
    localStorage.setItem('token', response.data.access_token)
    router.push('/app')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al iniciar sesión'
  }
}
</script>

<style scoped>
.login-container {
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
</style>
