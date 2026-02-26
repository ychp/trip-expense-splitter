<template>
  <el-container class="h-screen">
    <el-aside width="240px" class="sidebar border-r border-border overflow-hidden">
      <div class="flex items-center justify-center py-7 px-5 text-xl font-semibold tracking-wide border-b border-border bg-gradient-to-r from-sky-50 via-cyan-50 to-blue-50">
        <div class="relative flex items-center">
          <div class="absolute inset-0 bg-gradient-to-r from-sky-500 to-blue-500 rounded-lg blur opacity-20"></div>
          <div class="relative bg-gradient-to-br from-sky-500 to-blue-600 rounded-lg p-2 mr-3">
            <el-icon :size="24" class="text-white"><Wallet /></el-icon>
          </div>
        </div>
        <span class="bg-gradient-to-r from-sky-600 to-blue-600 bg-clip-text text-transparent">出行账本</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/trips">
          <el-icon><Location /></el-icon>
          <span>行程管理</span>
        </el-menu-item>
        <el-menu-item index="/transactions">
          <el-icon><List /></el-icon>
          <span>支出记录</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataAnalysis /></el-icon>
          <span>统计分析</span>
        </el-menu-item>
        <el-menu-item index="/wallets">
          <el-icon><Wallet /></el-icon>
          <span>钱包配置</span>
        </el-menu-item>
        <el-menu-item index="/categories">
          <el-icon><Grid /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-main class="bg-background p-6 lg:p-8 overflow-y-auto">
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
.sidebar {
  background: hsl(var(--background));
  position: relative;
}

.sidebar::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.03) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(125, 211, 252, 0.02) 0%, transparent 40%);
  pointer-events: none;
}

.sidebar-menu {
  @apply border-none bg-transparent py-2.5;
  position: relative;
  z-index: 1;
}

.sidebar-menu .el-menu-item {
  @apply mx-3 rounded-xl h-12 transition-all duration-300;
  line-height: 3rem;
  color: hsl(var(--foreground) / 0.75);
}

.sidebar-menu .el-menu-item:hover {
  background: linear-gradient(90deg, hsl(var(--accent)) 0%, hsl(var(--muted)) 100%);
  color: hsl(var(--foreground));
  transform: translateX(2px);
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(90deg, hsl(var(--primary) / 0.15) 0%, hsl(var(--primary) / 0.08) 100%);
  color: hsl(var(--primary));
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08);
}

.sidebar-menu .el-icon {
  @apply mr-2 text-lg;
}
</style>
