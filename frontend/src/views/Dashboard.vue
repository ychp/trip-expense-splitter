<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-foreground">欢迎回来</h1>
        <p class="text-muted-foreground mt-1">管理您的旅行预算和支出</p>
      </div>
      <el-button type="primary" size="large" @click="goToTrips">
        <el-icon class="mr-1"><Plus /></el-icon>
        新建行程
      </el-button>
    </div>

    <el-card v-if="trips.length === 0" class="text-center py-16">
      <el-icon :size="80" class="text-muted-foreground mb-4"><Location /></el-icon>
      <h3 class="text-lg font-semibold mb-2">暂无行程</h3>
      <p class="text-muted-foreground mb-4">开始创建您的第一个旅行行程吧</p>
      <el-button type="primary" @click="goToTrips">
        <el-icon class="mr-1"><Plus /></el-icon>
        创建行程
      </el-button>
    </el-card>

    <div v-else>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">当前行程</h2>
        <el-button link type="primary" @click="goToTrips">查看全部</el-button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <el-card 
          v-for="trip in activeTrips" 
          :key="trip.id" 
          class="trip-card hover:shadow-lg transition-all duration-300 cursor-pointer"
          @click="viewTrip(trip)"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-lg font-bold mb-1">{{ trip.name }}</h3>
              <p v-if="trip.description" class="text-sm text-muted-foreground line-clamp-2">{{ trip.description }}</p>
            </div>
            <el-tag :type="getTripStatusType(trip.status)" size="small">
              {{ getTripStatusText(trip.status) }}
            </el-tag>
          </div>
          
          <div v-if="trip.start_date || trip.end_date" class="flex items-center text-sm text-muted-foreground mb-4">
            <el-icon class="mr-1"><Calendar /></el-icon>
            <span>{{ formatDateRange(trip.start_date, trip.end_date) }}</span>
          </div>

          <div v-if="tripStats[trip.id]" class="border-t pt-4 space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-muted-foreground">总支出</span>
              <span class="font-bold text-red-500">¥{{ tripStats[trip.id].total_expense }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-muted-foreground">人均支出</span>
              <span class="font-bold text-primary">¥{{ tripStats[trip.id].average_expense }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-muted-foreground">参与人数</span>
              <span class="font-medium">{{ tripStats[trip.id].member_count }}人</span>
            </div>
          </div>
        </el-card>
      </div>

      <div v-if="completedTrips.length > 0" class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">历史行程</h2>
      </div>

      <div v-if="completedTrips.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <el-card 
          v-for="trip in completedTrips.slice(0, 3)" 
          :key="trip.id" 
          class="opacity-70 hover:opacity-100 transition-opacity"
        >
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold">{{ trip.name }}</h3>
            <el-tag type="info" size="small">已完成</el-tag>
          </div>
          <div v-if="trip.start_date || trip.end_date" class="flex items-center text-sm text-muted-foreground">
            <el-icon class="mr-1"><Calendar /></el-icon>
            <span>{{ formatDateRange(trip.start_date, trip.end_date) }}</span>
          </div>
        </el-card>
      </div>
    </div>

    <el-divider v-if="recentTransactions.length > 0" />

    <div v-if="recentTransactions.length > 0">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">最近支出</h2>
        <el-button link type="primary" @click="goToTransactions">查看全部</el-button>
      </div>

      <el-card>
        <div class="space-y-3">
          <div 
            v-for="txn in recentTransactions" 
            :key="txn.id" 
            class="flex items-center p-4 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
            @click="goToTransactions"
          >
            <div class="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center mr-3">
              <el-icon class="text-red-500"><Wallet /></el-icon>
            </div>
            <div class="flex-1">
              <div class="font-medium">{{ txn.category?.name || '-' }}</div>
              <div class="text-sm text-muted-foreground">{{ txn.wallet?.name || '-' }} · {{ txn.trip?.name || '-' }}</div>
            </div>
            <div class="text-right">
              <div class="font-bold text-red-500">-¥{{ txn.amount }}</div>
              <div class="text-xs text-muted-foreground">{{ txn.transaction_date }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Location, Calendar, Wallet } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const trips = ref([])
const tripStats = ref({})
const recentTransactions = ref([])

const activeTrips = computed(() => {
  return trips.value.filter(t => t.status !== 'completed')
})

const completedTrips = computed(() => {
  return trips.value.filter(t => t.status === 'completed')
})

const getTripStatusType = (status) => {
  const typeMap = {
    planning: 'warning',
    ongoing: 'success',
    completed: 'info'
  }
  return typeMap[status] || 'info'
}

const getTripStatusText = (status) => {
  const textMap = {
    planning: '计划中',
    ongoing: '进行中',
    completed: '已完成'
  }
  return textMap[status] || status
}

const formatDateRange = (start, end) => {
  if (!start && !end) return ''
  if (!start) return `至 ${end}`
  if (!end) return `${start} 起`
  return `${start} ~ ${end}`
}

const fetchTrips = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/trips/')
    trips.value = data
    await fetchTripsStats()
  } catch (error) {
    ElMessage.error('获取行程列表失败')
  }
}

const fetchTripsStats = async () => {
  for (const trip of activeTrips.value) {
    try {
      const { data } = await axios.get(`http://localhost:8000/api/stats/per-person/${trip.id}`)
      tripStats.value[trip.id] = {
        total_expense: data.total_expense.toFixed(2),
        average_expense: data.average_expense.toFixed(2),
        member_count: data.member_count
      }
    } catch (error) {
      console.error('Failed to fetch stats for trip', trip.id)
    }
  }
}

const fetchRecentTransactions = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/transactions/', {
      params: { limit: 5 }
    })
    recentTransactions.value = data.slice(0, 5)
  } catch (error) {
    console.error('Failed to fetch recent transactions')
  }
}

const viewTrip = (trip) => {
  router.push({ name: 'Statistics', query: { trip_id: trip.id } })
}

const goToTrips = () => {
  router.push('/trips')
}

const goToTransactions = () => {
  router.push('/transactions')
}

onMounted(async () => {
  await Promise.all([
    fetchTrips(),
    fetchRecentTransactions()
  ])
})
</script>

<style scoped>
.trip-card {
  background: linear-gradient(135deg, hsl(var(--background)) 0%, hsl(var(--muted)) 100%);
}

.trip-card:hover {
  transform: translateY(-4px);
}
</style>
