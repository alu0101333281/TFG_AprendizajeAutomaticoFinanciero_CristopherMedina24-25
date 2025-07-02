import { defineStore } from 'pinia'

interface ClosedTrade {
  side: 'buy' | 'sell'
  entry_price: number
  exit_price: number
  volume: number
  leverage: number
  entry_time: string
  exit_time: string
  pnl: number
  roi: number
  symbol: string
}

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    balance: 0,
    closedTrades: [] as ClosedTrade[]
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

        const closedTradesRes = await fetch('http://localhost:8080/users/closed_trades', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const trades = await closedTradesRes.json()
        this.closedTrades = trades
      } catch (e) {
        console.error('Error al obtener datos del usuario:', e)
      }
    },

    async fetchClosedTrades() {
      const token = localStorage.getItem('token')
      if (!token) return

      try {
        const closedTradesRes = await fetch('http://localhost:8080/users/closed_trades', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const trades = await closedTradesRes.json()
        this.closedTrades = trades
      } catch (e) {
        console.error('Error al obtener operaciones cerradas:', e)
      }
    }
  }
})
