<template>
  <el-container style="height: 100vh">
    <el-aside width="240px" class="sidebar">
      <div class="logo">
        <el-icon :size="28" style="margin-right: 8px"><Wallet /></el-icon>
        <span>家庭账本</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/transactions">
          <el-icon><List /></el-icon>
          <span>流水记录</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataAnalysis /></el-icon>
          <span>统计分析</span>
        </el-menu-item>
        <el-menu-item index="/accounts">
          <el-icon><CreditCard /></el-icon>
          <span>账户管理</span>
        </el-menu-item>
        <el-menu-item index="/categories">
          <el-icon><Grid /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #6366f1;
  --primary-light: #818cf8;
  --primary-dark: #4f46e5;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #3b82f6;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.sidebar {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  padding: 28px 20px;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  border: none;
  background: transparent;
  padding: 10px 0;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.85);
  margin: 4px 12px;
  border-radius: 12px;
  height: 48px;
  line-height: 48px;
  transition: all 0.3s ease;
}

.sidebar-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.sidebar-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  font-weight: 500;
}

.sidebar-menu .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.main-content {
  background-color: var(--bg-color);
  padding: 24px 32px;
  overflow-y: auto;
}

h2 {
  font-size: 26px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
}

.el-card {
  border-radius: 16px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.el-card:hover {
  box-shadow: var(--shadow-md);
}

.el-card__header {
  padding: 18px 24px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  font-size: 16px;
  color: var(--text-primary);
}

.el-table {
  border-radius: 12px;
  overflow: hidden;
}

.el-table th.el-table__cell {
  background-color: #f1f5f9;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.el-table__row {
  transition: background-color 0.2s ease;
}

.el-table__row:hover {
  background-color: #f8fafc;
}

.el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.el-button--success {
  background-color: var(--success-color);
  border: none;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.el-button--danger {
  background-color: var(--danger-color);
  border: none;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.el-input__wrapper,
.el-select .el-input__wrapper,
.el-date-editor .el-input__wrapper {
  border-radius: 10px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.el-input__wrapper:hover,
.el-select .el-input__wrapper:hover {
  box-shadow: var(--shadow-md);
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.el-dialog {
  border-radius: 20px;
  overflow: hidden;
}

.el-dialog__header {
  padding: 24px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.el-dialog__title {
  font-size: 18px;
  font-weight: 600;
}

.el-dialog__body {
  padding: 28px;
}

.el-tag--success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  padding: 6px 12px;
}

.el-tag--danger {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 6px 12px;
}

.el-form-item__label {
  color: var(--text-secondary);
  font-weight: 500;
}
</style>
