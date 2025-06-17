<script setup lang="ts">
import chart from './views/BacktestingView.vue'
import login from './views/LoginView.vue'
import register from './views/RegisterView.vue'
</script>

<template>
<router-view />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
