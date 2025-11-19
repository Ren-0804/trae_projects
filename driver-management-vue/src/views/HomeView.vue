<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <section class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">欢迎使用司机管理系统</h1>
        <p class="welcome-subtitle">专业的车队管理解决方案</p>
      </div>
    </section>

    <!-- 统计卡片 -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <UserOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-number">24</div>
            <div class="stat-label">活跃司机</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <CarOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-number">18</div>
            <div class="stat-label">运营车辆</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <CalendarOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-number">12</div>
            <div class="stat-label">今日任务</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <WarningOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-number">3</div>
            <div class="stat-label">待处理警报</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 快速操作 -->
    <section class="quick-actions-section">
      <h2 class="section-title">快速操作</h2>
      <div class="action-grid">
        <button class="action-btn">
          <PlusOutlined />
          <span>添加司机</span>
        </button>
        <button class="action-btn">
          <CarOutlined />
          <span>添加车辆</span>
        </button>
        <button class="action-btn">
          <CalendarOutlined />
          <span>创建排班</span>
        </button>
        <button class="action-btn">
          <FileTextOutlined />
          <span>生成报告</span>
        </button>
      </div>
    </section>

    <!-- 最近活动 -->
    <section class="recent-activity-section">
      <h2 class="section-title">最近活动</h2>
      <div class="activity-list">
        <div class="activity-item">
          <div class="activity-avatar">张</div>
          <div class="activity-content">
            <div class="activity-text">张三完成了车辆检查</div>
            <div class="activity-time">2分钟前</div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-avatar">李</div>
          <div class="activity-content">
            <div class="activity-text">李四开始了新的运输任务</div>
            <div class="activity-time">15分钟前</div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-avatar">王</div>
          <div class="activity-content">
            <div class="activity-text">王五提交了保养申请</div>
            <div class="activity-time">1小时前</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import {
  UserOutlined,
  CarOutlined,
  CalendarOutlined,
  WarningOutlined,
  PlusOutlined,
  FileTextOutlined
} from '@ant-design/icons-vue'
</script>

<style scoped>
.dashboard {
  padding: 0;
  background-color: var(--color-bg-secondary);
  min-height: calc(100vh - var(--layout-header-height));
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-700) 100%);
  color: white;
  padding: var(--spacing-2xl) var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.welcome-content {
  max-width: var(--layout-content-max-width);
  margin: 0 auto;
}

.welcome-title {
  font-size: var(--font-size-3xl);
  font-weight: 600;
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: var(--font-size-md);
  margin: 0;
  opacity: 0.9;
  line-height: 1.4;
}

/* 统计卡片 */
.stats-section {
  margin-bottom: var(--spacing-xl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-lg);
  max-width: var(--layout-content-max-width);
  margin: 0 auto;
}

.stat-card {
  background-color: var(--color-bg-container);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-1);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  transition: all var(--duration-fast) var(--ease-out);
  border: 1px solid var(--color-border-light);
}

.stat-card:hover {
  box-shadow: var(--shadow-2);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background-color: var(--color-primary-50);
  color: var(--color-primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-lg);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: var(--font-size-2xl);
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.2;
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.3;
}

/* 快速操作 */
.quick-actions-section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-lg) 0;
  padding: 0 var(--spacing-lg);
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  max-width: var(--layout-content-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.action-btn {
  background-color: var(--color-bg-container);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-base);
  padding: var(--spacing-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  text-align: center;
}

.action-btn:hover {
  background-color: var(--color-primary-50);
  border-color: var(--color-primary-200);
  color: var(--color-primary-600);
  box-shadow: var(--shadow-1);
}

.action-btn:active {
  transform: scale(0.98);
}

/* 最近活动 */
.recent-activity-section {
  margin-bottom: var(--spacing-xl);
}

.activity-list {
  max-width: var(--layout-content-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--color-bg-container);
  border-radius: var(--radius-base);
  margin-bottom: var(--spacing-sm);
  border: 1px solid var(--color-border-light);
  transition: all var(--duration-fast) var(--ease-out);
}

.activity-item:hover {
  background-color: var(--color-gray-50);
}

.activity-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--color-primary-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: var(--font-size-sm);
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.4;
  margin-bottom: 2px;
}

.activity-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  line-height: 1.3;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-section {
    padding: var(--spacing-xl) var(--spacing-md);
  }

  .welcome-title {
    font-size: var(--font-size-2xl);
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
    padding: 0 var(--spacing-md);
  }

  .stat-card {
    padding: var(--spacing-md);
  }

  .action-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    padding: 0 var(--spacing-md);
  }

  .activity-list {
    padding: 0 var(--spacing-md);
  }
}
</style>
