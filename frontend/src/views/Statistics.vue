<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-foreground">统计分析</h1>
      <p class="text-muted-foreground mt-1">查看旅行支出人均对比和分类占比</p>
    </div>

    <el-card>
      <el-form :inline="true">
        <el-form-item label="行程">
          <el-select v-model="selectedTripId" placeholder="选择行程" class="w-[200px]" @change="fetchStats">
            <el-option v-for="trip in trips" :key="trip.id" :label="trip.name" :value="trip.id" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="!selectedTripId" class="text-center py-12">
      <el-empty description="请选择一个行程查看统计" />
    </el-card>

    <template v-else>
      <div v-if="loading" class="text-center py-12">
        <el-icon :size="32" class="is-loading"><Loading /></el-icon>
      </div>

      <div v-else-if="stats" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">总支出</div>
            <div class="text-3xl font-bold text-red-500">¥{{ stats.total_expense }}</div>
          </el-card>
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">人均支出</div>
            <div class="text-3xl font-bold text-primary">¥{{ stats.average_expense }}</div>
          </el-card>
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">参与人数</div>
            <div class="text-3xl font-bold text-foreground">{{ stats.member_count }}人</div>
          </el-card>
        </div>

        <el-card>
          <template #header>
            <span class="font-semibold">人均支出对比</span>
          </template>
          <div class="space-y-4">
            <div v-for="member in stats.member_stats" :key="member.member_id" class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-medium">{{ member.member_name }}</span>
                <div class="flex items-center space-x-4">
                  <span class="text-lg font-bold" :class="getAmountClass(member.total_amount, stats.average_expense)">
                    ¥{{ member.total_amount.toFixed(2) }}
                  </span>
                  <span class="text-sm text-muted-foreground">
                    {{ getDiffText(member.total_amount, stats.average_expense) }}
                  </span>
                </div>
              </div>
              <el-progress 
                :percentage="getPercentage(member.total_amount, stats.total_expense)" 
                :color="getProgressColor(member.total_amount, stats.average_expense)"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <el-card>
            <template #header>
              <span class="font-semibold">分类占比</span>
            </template>
            <div class="space-y-3">
              <div v-for="(ratio, category) in stats.category_ratios" :key="category" class="space-y-1">
                <div class="flex items-center justify-between text-sm">
                  <span>{{ category }}</span>
                  <span class="text-muted-foreground">{{ ratio }}%</span>
                </div>
                <el-progress 
                  :percentage="ratio" 
                  :show-text="false"
                  :color="getCategoryColor(category)"
                />
              </div>
            </div>
          </el-card>

          <el-card>
            <template #header>
              <span class="font-semibold">人均分类支出</span>
            </template>
            <div class="space-y-3">
              <div v-for="member in stats.member_stats" :key="member.member_id">
                <div class="font-medium mb-2">{{ member.member_name }}</div>
                <div class="space-y-1 pl-4">
                  <div v-for="(amount, category) in member.by_category" :key="category" class="flex items-center justify-between text-sm">
                    <span class="text-muted-foreground">{{ category }}</span>
                    <span>¥{{ amount.toFixed(2) }}</span>
                  </div>
                  <div v-if="Object.keys(member.by_category).length === 0" class="text-muted-foreground text-sm">无支出</div>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <el-card>
          <template #header>
            <span class="font-semibold">钱包使用情况</span>
          </template>
          <div v-if="walletSummary" class="space-y-3">
            <div v-for="wallet in walletSummary.wallets" :key="wallet.wallet_id" class="p-4 border rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium">{{ wallet.wallet_name }}</span>
                <span class="text-sm text-muted-foreground">{{ wallet.transaction_count }}笔交易</span>
              </div>
              <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div class="text-muted-foreground text-xs">余额</div>
                  <div class="font-semibold">¥{{ wallet.balance }}</div>
                </div>
                <div>
                  <div class="text-muted-foreground text-xs">已支出</div>
                  <div class="font-semibold text-red-500">¥{{ wallet.total_spent }}</div>
                </div>
                <div>
                  <div class="text-muted-foreground text-xs">剩余</div>
                  <div class="font-semibold" :class="wallet.remaining < 0 ? 'text-red-500' : 'text-green-500'">¥{{ wallet.remaining }}</div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const trips = ref([])
const selectedTripId = ref(null)
const stats = ref(null)
const walletSummary = ref(null)
const loading = ref(false)

const fetchTrips = async () => {
  try {
    console.log('📡 Statistics: Fetching trips...')
    const data = await apiClient.trips.list()
    console.log('✅ Statistics: Trips received:', data)
    trips.value = data
    if (trips.value.length > 0) {
      selectedTripId.value = trips.value[0].id
      console.log('✅ Statistics: Selected trip:', selectedTripId.value)
      await fetchStats()
    }
  } catch (error) {
    console.error('❌ Statistics: 获取行程列表失败', error)
    ElMessage.error('获取行程列表失败')
  }
}

const fetchStats = async () => {
  if (!selectedTripId.value) return
  loading.value = true
  try {
    console.log('📡 Statistics: Fetching stats for trip:', selectedTripId.value)
    const [statsData, walletData] = await Promise.all([
      apiClient.stats.perPerson(selectedTripId.value),
      apiClient.stats.walletSummary(selectedTripId.value)
    ])
    console.log('✅ Statistics: Stats data received:', statsData)
    console.log('✅ Statistics: Wallet summary received:', walletData)
    stats.value = statsData
    walletSummary.value = walletData
  } catch (error) {
    console.error('❌ Statistics: 获取统计数据失败', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

const getAmountClass = (amount, average) => {
  if (amount > average) return 'text-red-500'
  if (amount < average) return 'text-green-500'
  return 'text-foreground'
}

const getDiffText = (amount, average) => {
  const diff = amount - average
  if (Math.abs(diff) < 0.01) return '持平'
  const sign = diff > 0 ? '+' : ''
  return `${sign}${diff.toFixed(2)}`
}

const getPercentage = (amount, total) => {
  if (total === 0) return 0
  return Math.round((amount / total) * 100)
}

const getProgressColor = (amount, average) => {
  if (amount > average) return '#f56565'
  if (amount < average) return '#48bb78'
  return '#0ea5e9'
}

const getCategoryColor = (category) => {
  const colors = {
    '交通费': '#3b82f6',
    '住宿费': '#8b5cf6',
    '餐饮费': '#f59e0b',
    '门票费': '#10b981',
    '购物费': '#ef4444',
    '娱乐费': '#ec4899',
    '其他': '#6b7280'
  }
  return colors[category] || '#6b7280'
}

onMounted(() => {
  fetchTrips()
})
</script>
