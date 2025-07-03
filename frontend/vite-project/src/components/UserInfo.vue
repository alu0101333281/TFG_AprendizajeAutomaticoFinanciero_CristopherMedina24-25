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

</style>
