<template>
  <div style="
    min-height: calc(100vh - 120px);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    position: relative;
    overflow: hidden;
  ">
    <!-- 背景装饰 -->
    <div style="
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
      background-size: 50px 50px;
      animation: float 20s ease-in-out infinite;
    "></div>
    
    <div style="
      position: absolute;
      top: 20%;
      right: 10%;
      width: 300px;
      height: 300px;
      background: rgba(255,255,255,0.1);
      border-radius: 50%;
      filter: blur(40px);
      animation: pulse 4s ease-in-out infinite;
    "></div>
    
    <div style="
      position: absolute;
      bottom: 20%;
      left: 10%;
      width: 200px;
      height: 200px;
      background: rgba(255,255,255,0.08);
      border-radius: 50%;
      filter: blur(30px);
      animation: pulse 6s ease-in-out infinite reverse;
    "></div>

    <TheWelcome />
  </div>
</template>

<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}
</style>
