import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    balance: 0
  }),
  actions: {
    async fetchUserInfo() {
      const token = localStorage.getItem('token')
      if (!token) return

      try {
        const userRes = await fetch('http://localhost:8080/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const { username } = await userRes.json()
        this.username = username

        const balanceRes = await fetch('http://localhost:8080/users/balance', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const { balance } = await balanceRes.json()
        this.balance = balance
      } catch (e) {
        console.error('Error al obtener datos del usuario:', e)
      }
    }
  }
})