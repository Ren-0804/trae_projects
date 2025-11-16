<template>
  <ErrorBoundary>
    <router-view />
  </ErrorBoundary>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
