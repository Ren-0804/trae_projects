<template>
  <div style="
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    padding: 48px;
    max-width: 800px;
    animation: slideIn 0.8s ease-out;
  ">
    <div style="text-align: center; margin-bottom: 40px;">
      <h1 style="
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 8px 0;
      ">🚗 司机管理系统</h1>
      <p style="
        color: #6b7280;
        font-size: 16px;
        margin: 0;
      ">现代化车队管理解决方案</p>
    </div>

    <WelcomeItem>
      <template #icon>
        <DocumentationIcon />
      </template>
      <template #heading>系统功能</template>

      本系统提供完整的司机管理功能，包括
      <strong style="color: #667eea;">司机信息管理</strong>、
      <strong style="color: #10b981;">车辆调度</strong>、
      <strong style="color: #f59e0b;">证书管理</strong>、
      <strong style="color: #ef4444;">安全监控</strong>等核心模块。
      现代化的界面设计，让管理更高效、更直观。
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <ToolingIcon />
      </template>
      <template #heading>技术特色</template>

      基于
      <strong style="color: #667eea;">Vue 3 + TypeScript</strong> 构建，采用
      <strong style="color: #10b981;">现代化UI设计</strong>，
      支持<strong style="color: #f59e0b;">响应式布局</strong>，
      提供<strong style="color: #ef4444;">流畅的用户体验</strong>。
      后端采用 FastAPI 框架，确保系统的高性能和稳定性。
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <EcosystemIcon />
      </template>
      <template #heading>核心模块</template>

      🚗 <strong>司机管理</strong> - 完整的司机信息档案<br/>
      🚙 <strong>车辆管理</strong> - 车辆信息与维护记录<br/>
      📅 <strong>排班调度</strong> - 智能排班与调度管理<br/>
      📋 <strong>证书管理</strong> - 证书到期提醒与管理<br/>
      ⚠️ <strong>安全管理</strong> - 实时监控与预警系统<br/>
      📊 <strong>数据统计</strong> - 全面的数据分析报告
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <CommunityIcon />
      </template>
      <template #heading>使用指南</template>

      点击左侧导航菜单开始使用各项功能。
      <strong style="color: #667eea;">司机管理</strong>用于维护司机基本信息，
      <strong style="color: #10b981;">车辆管理</strong>跟踪车辆状态，
      <strong style="color: #f59e0b;">排班调度</strong>安排日常工作，
      系统会自动提醒证书到期和重要事项。
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <SupportIcon />
      </template>
      <template #heading>系统优势</template>

      采用<strong style="color: #667eea;">玻璃拟态设计</strong>，界面现代美观；
      <strong style="color: #10b981;">响应式布局</strong>，适配各种设备；
      <strong style="color: #f59e0b;">实时数据更新</strong>，信息及时准确；
      <strong style="color: #ef4444;">智能提醒功能</strong>，避免遗漏重要事项。
      让车队管理变得简单高效！
    </WelcomeItem>
  </div>
</template>

<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'

const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<style scoped>
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>