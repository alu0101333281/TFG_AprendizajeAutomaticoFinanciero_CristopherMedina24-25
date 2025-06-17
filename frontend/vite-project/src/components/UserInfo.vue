<template>
  <div class="user-info" v-if="username">
    <span>👤 {{ username }}</span>
    <button @click="logout">Cerrar sesión</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const res = await fetch('http://localhost:8080/users/me', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (res.ok) {
        const data = await res.json()
        username.value = data.username
      } else {
        localStorage.removeItem('token')
        router.push('/login')
      }
    } catch (e) {
      console.error('Error al verificar usuario:', e)
    }
  }
})

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.user-info {
  position: fixed;
  top: 10px;
  right: 10px;
  background: #1e1e1e;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info button {
  background: #f44336;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
