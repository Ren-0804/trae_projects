<template>
  <div style="
    display: flex;
    position: relative;
    margin-top: 2rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  "
  @mouseenter="hoverUp"
  @mouseleave="hoverDown"
  >
    <div style="
      display: flex;
      align-items: center;
      justify-content: center;
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      margin-right: 1rem;
      box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    ">
      <slot name="icon"></slot>
    </div>
    <div style="flex: 1;">
      <h3 style="
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2c3e50;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      ">
        <slot name="heading"></slot>
      </h3>
      <div style="color: #4b5563; line-height: 1.6;">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const hoverUp = (e: Event) => {
  const el = e.currentTarget as HTMLElement
  if (el && el.style) el.style.transform = 'translateY(-4px)'
}
const hoverDown = (e: Event) => {
  const el = e.currentTarget as HTMLElement
  if (el && el.style) el.style.transform = 'translateY(0)'
}
</script>

<style scoped>
@media (min-width: 1024px) {
  .item {
    margin-top: 0;
    padding: 2rem;
  }
}
</style>
