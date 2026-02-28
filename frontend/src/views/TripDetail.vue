<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <el-page-header @back="goBack" class="mb-6">
      <template #content>
        <div class="flex items-center">
          <el-icon class="mr-2" :size="20"><Location /></el-icon>
          <span class="text-lg font-semibold">{{ trip?.name }}</span>
        </div>
      </template>
      <template #extra>
        <el-button type="primary" @click="editDialogVisible = true">
          <el-icon class="mr-1"><Edit /></el-icon>
          编辑行程
        </el-button>
      </template>
    </el-page-header>

    <div v-if="loading" class="text-center py-12">
      <el-icon :size="32" class="is-loading"><Loading /></el-icon>
    </div>

    <div v-else-if="trip">
      <el-card class="mb-6">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-3">
              <el-tag :type="getTripStatusType(trip.status)">{{ getTripStatusText(trip.status) }}</el-tag>
              <span v-if="trip.start_date || trip.end_date" class="text-muted-foreground text-sm">
                <el-icon class="mr-1"><Calendar /></el-icon>
                {{ formatDateRange(trip.start_date, trip.end_date) }}
              </span>
            </div>
            <p v-if="trip.description" class="text-muted-foreground">{{ trip.description }}</p>
          </div>
        </div>
      </el-card>

      <el-row :gutter="20" class="mb-6">
        <el-col :span="8">
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">总支出</div>
            <div class="text-2xl font-bold text-red-500">¥{{ stats?.total_expense || '0.00' }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">人均支出</div>
            <div class="text-2xl font-bold text-primary">¥{{ stats?.average_expense || '0.00' }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="text-center">
            <div class="text-muted-foreground text-sm mb-2">参与人数</div>
            <div class="text-2xl font-bold text-foreground">{{ members.length }}人</div>
          </el-card>
        </el-col>
      </el-row>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="成员管理" name="members">
          <Members ref="membersRef" :trip-id="tripId" @update="handleMembersUpdate" />
        </el-tab-pane>

        <el-tab-pane label="钱包配置" name="wallets">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold">钱包列表</h3>
              <el-button type="primary" size="small" @click="walletDialogVisible = true">
                <el-icon class="mr-1"><Plus /></el-icon>
                新建钱包
              </el-button>
            </div>

            <div v-if="wallets.length === 0" class="text-center py-8 text-muted-foreground">
              暂无钱包
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <el-card v-for="wallet in wallets" :key="wallet.id">
                <div class="flex items-start justify-between mb-4">
                  <div>
                    <h4 class="font-semibold text-lg">{{ wallet.name }}</h4>
                    <div class="flex items-baseline mt-1">
                      <span class="text-2xl font-bold text-primary">¥{{ wallet.balance.toFixed(2) }}</span>
                    </div>
                  </div>
                  <el-dropdown @command="(cmd) => handleWalletAction(cmd, wallet)">
                    <el-icon class="cursor-pointer text-lg"><MoreFilled /></el-icon>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">编辑</el-dropdown-item>
                        <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>

                <div v-if="wallet.ownership && Object.keys(wallet.ownership).length > 0" class="border-t pt-3">
                  <div class="text-sm text-muted-foreground mb-2">归属比例</div>
                  <div class="space-y-1">
                    <div v-for="(ratio, memberId) in wallet.ownership" :key="memberId" class="flex items-center justify-between text-sm">
                      <span>{{ getMemberName(parseInt(memberId)) }}</span>
                      <span class="text-primary font-medium">{{ (ratio * 100).toFixed(0) }}%</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="支出记录" name="transactions">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold">支出明细</h3>
              <el-button type="primary" size="small" @click="goToTransactions">
                <el-icon class="mr-1"><Plus /></el-icon>
                记一笔
              </el-button>
            </div>

            <el-card v-if="transactions.length === 0" class="text-center py-8">
              <el-empty description="暂无支出记录" />
            </el-card>

            <el-card v-else>
              <el-table :data="transactions" stripe>
                <el-table-column prop="transaction_date" label="日期" width="120" />
                <el-table-column prop="category.name" label="分类" width="120" />
                <el-table-column prop="wallet.name" label="钱包" width="120" />
                <el-table-column prop="amount" label="金额" width="140">
                  <template #default="scope">
                    <span class="text-red-600 font-semibold">-¥{{ scope.row.amount }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="分摊" width="150">
                  <template #default="scope">
                    <el-tag size="small" type="info">{{ scope.row.split_method === 'equal' ? '均分' : '按比例' }}</el-tag>
                    <span class="ml-2 text-muted-foreground text-sm">{{ getSplitMembersText(scope.row) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="remark" label="备注" />
              </el-table>
            </el-card>
          </div>
        </el-tab-pane>

        <el-tab-pane label="统计分析" name="stats">
          <div v-if="stats" class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
            </div>

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
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="editDialogVisible" title="编辑行程" width="500px">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="80px">
        <el-form-item label="行程名称" prop="name">
          <el-input v-model="editForm.name" placeholder="请输入行程名称" />
        </el-form-item>
        <el-form-item label="行程描述" prop="description">
          <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="请输入行程描述（可选）" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="editForm.start_date" type="date" placeholder="选择开始日期" class="w-full" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="editForm.end_date" type="date" placeholder="选择结束日期" class="w-full" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="editForm.status" placeholder="选择状态" class="w-full">
            <el-option label="计划中" value="planning" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateTrip">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="walletDialogVisible" :title="editingWallet ? '编辑钱包' : '新建钱包'" width="500px">
      <el-form :model="walletForm" :rules="walletRules" ref="walletFormRef" label-width="80px">
        <el-form-item label="钱包名称" prop="name">
          <el-input v-model="walletForm.name" placeholder="请输入钱包名称" />
        </el-form-item>
        <el-form-item label="余额" prop="balance">
          <el-input-number v-model="walletForm.balance" :min="0" :precision="2" class="w-full" />
        </el-form-item>
        <el-form-item label="归属比例" prop="ownership">
          <div class="w-full space-y-2">
            <div v-for="member in members" :key="member.id" class="flex items-center space-x-2">
              <span class="w-24 text-sm">{{ member.name }}</span>
              <el-slider v-model="walletForm.ownership[member.id]" :min="0" :max="1" :step="0.01" :show-tooltip="false" class="flex-1" />
              <span class="w-16 text-right text-sm text-primary">{{ (walletForm.ownership[member.id] * 100).toFixed(0) }}%</span>
            </div>
            <div v-if="ownershipTotal !== 1" class="text-sm text-orange-500">
              当前总比例: {{ (ownershipTotal * 100).toFixed(0) }}% {{ ownershipTotal < 1 ? '(不足100%)' : '(超过100%)' }}
            </div>
            <div v-else class="text-sm text-green-500">比例分配正确</div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="walletDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleWalletSubmit" :disabled="ownershipTotal !== 1">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Location, Calendar, Edit, Plus, MoreFilled, Loading 
} from '@element-plus/icons-vue'
import Members from './Members.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const tripId = computed(() => parseInt(route.params.id))
const trip = ref(null)
const members = ref([])
const wallets = ref([])
const transactions = ref([])
const stats = ref(null)
const loading = ref(true)
const activeTab = ref('members')

const editDialogVisible = ref(false)
const walletDialogVisible = ref(false)
const editingWallet = ref(null)
const editFormRef = ref(null)
const walletFormRef = ref(null)
const membersRef = ref(null)

const editForm = ref({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'planning'
})

const walletForm = ref({
  name: '',
  balance: 0,
  trip_id: tripId.value,
  ownership: {}
})

const editRules = {
  name: [{ required: true, message: '请输入行程名称', trigger: 'blur' }]
}

const walletRules = {
  name: [{ required: true, message: '请输入钱包名称', trigger: 'blur' }],
  balance: [{ required: true, message: '请输入余额', trigger: 'blur' }]
}

const ownershipTotal = computed(() => {
  return Object.values(walletForm.value.ownership).reduce((sum, val) => sum + (val || 0), 0)
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

const getMemberName = (memberId) => {
  const member = members.value.find(m => m.id === memberId)
  return member ? member.name : `成员${memberId}`
}

const getSplitMembersText = (row) => {
  if (!row.split_members || row.split_members.length === 0) return '未设置'
  const count = row.split_members.length
  return `${count}人分摊`
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

const fetchTrip = async () => {
  try {
    const data = await apiClient.trips.get(tripId.value)
    trip.value = data
    Object.assign(editForm.value, {
      name: data.name,
      description: data.description || '',
      start_date: data.start_date,
      end_date: data.end_date,
      status: data.status
    })
  } catch (error) {
    ElMessage.error('获取行程详情失败')
  }
}

const fetchMembers = async () => {
  try {
    const data = await apiClient.members.listByTrip(tripId.value)
    members.value = data
    data.forEach(m => {
      if (!(m.id in walletForm.value.ownership)) {
        walletForm.value.ownership[m.id] = 0
      }
    })
  } catch (error) {
    ElMessage.error('获取成员列表失败')
  }
}

const fetchWallets = async () => {
  try {
    console.log('📡 Fetching wallets for trip:', tripId.value)
    const data = await apiClient.wallets.list({ trip_id: tripId.value })
    console.log('✅ Wallets API response:', data)
    console.log('📊 Wallets count:', Array.isArray(data) ? data.length : 'Not an array')
    wallets.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('❌ 获取钱包列表失败:', error)
    ElMessage.error('获取钱包列表失败')
  }
}

const fetchTransactions = async () => {
  try {
    const data = await apiClient.transactions.list({ trip_id: tripId.value })
    transactions.value = data
  } catch (error) {
    ElMessage.error('获取支出记录失败')
  }
}

const fetchStats = async () => {
  try {
    const data = await apiClient.stats.perPerson(tripId.value)
    stats.value = data
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

const handleMembersUpdate = (data) => {
  members.value = data
}

const handleUpdateTrip = async () => {
  await editFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      await apiClient.trips.update(tripId.value, editForm.value)
      ElMessage.success('行程更新成功')
      editDialogVisible.value = false
      fetchTrip()
    } catch (error) {
      ElMessage.error('更新失败')
    }
  })
}

const handleWalletAction = async (command, wallet) => {
  if (command === 'edit') {
    editingWallet.value = wallet
    walletForm.value = {
      name: wallet.name,
      balance: wallet.balance,
      trip_id: wallet.trip_id,
      ownership: { ...wallet.ownership } || {}
    }
    members.value.forEach(m => {
      if (!(m.id in walletForm.value.ownership)) {
        walletForm.value.ownership[m.id] = 0
      }
    })
    walletDialogVisible.value = true
  } else if (command === 'delete') {
    try {
      await ElMessageBox.confirm('确定要删除这个钱包吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await apiClient.wallets.delete(wallet.id)
      ElMessage.success('删除成功')
      fetchWallets()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
      }
    }
  }
}

const handleWalletSubmit = async () => {
  await walletFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    const ownership = {}
    for (const [memberId, ratio] of Object.entries(walletForm.value.ownership)) {
      if (ratio > 0) {
        ownership[parseInt(memberId)] = ratio
      }
    }
    
    try {
      const payload = {
        ...walletForm.value,
        trip_id: tripId.value,
        ownership: Object.keys(ownership).length > 0 ? ownership : null
      }
      
      if (editingWallet.value) {
        await apiClient.wallets.update(editingWallet.value.id, payload)
        ElMessage.success('钱包更新成功')
      } else {
        await apiClient.wallets.create(payload)
        ElMessage.success('钱包创建成功')
      }
      walletDialogVisible.value = false
      fetchWallets()
    } catch (error) {
      ElMessage.error(editingWallet.value ? '更新失败' : '创建失败')
    }
  })
}

const goBack = () => {
  router.push('/trips')
}

const goToTransactions = () => {
  router.push({ path: '/transactions', query: { trip_id: tripId.value } })
}

onMounted(async () => {
  console.log('🚀 TripDetail mounted, tripId:', tripId.value)
  loading.value = true
  try {
    await Promise.all([
      fetchTrip(),
      fetchMembers(),
      fetchWallets(),
      fetchTransactions(),
      fetchStats()
    ])
    console.log('✅ All data fetched, wallets:', wallets.value.length)
  } catch (error) {
    console.error('❌ Error fetching data:', error)
  }
  loading.value = false
  console.log('📊 Final state - trip:', !!trip.value, 'wallets:', wallets.value.length)
})
</script>
