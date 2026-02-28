<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-foreground">钱包配置</h1>
        <p class="text-muted-foreground mt-1">配置行程钱包和每个成员的余额</p>
      </div>
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon class="mr-1"><Plus /></el-icon>
        新建钱包
      </el-button>
    </div>

    <div class="flex items-center space-x-4">
      <el-select v-model="selectedTripId" placeholder="选择行程" class="w-64" @change="fetchWallets">
        <el-option v-for="trip in trips" :key="trip.id" :label="trip.name" :value="trip.id" />
      </el-select>
      <span v-if="selectedTrip" class="text-muted-foreground text-sm">{{ selectedTrip.description || '无描述' }}</span>
    </div>

    <el-card v-if="!selectedTripId" class="text-center py-12">
      <el-empty description="请选择一个行程查看钱包" />
    </el-card>

    <div v-else-if="wallets.length === 0" class="text-center py-12">
      <el-empty description="该行程暂无钱包，点击右上角创建钱包" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <el-card v-for="wallet in wallets" :key="wallet.id" class="hover:shadow-lg transition-shadow">
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-semibold text-lg">{{ wallet.name }}</span>
            <el-dropdown @command="(cmd) => handleAction(cmd, wallet)">
              <el-icon class="cursor-pointer"><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </template>
        <div class="space-y-3">
          <div class="flex items-baseline justify-between">
            <span class="text-muted-foreground text-sm">总余额</span>
            <span class="text-2xl font-bold text-primary">¥{{ totalBalance(wallet).toFixed(2) }}</span>
          </div>
          <div v-if="wallet.balance_by_member && Object.keys(wallet.balance_by_member).length > 0" class="border-t pt-3">
            <div class="text-sm text-muted-foreground mb-2">成员余额</div>
            <div class="space-y-1">
              <div v-for="(balance, memberId) in wallet.balance_by_member" :key="memberId" class="flex items-center justify-between text-sm">
                <span>{{ getMemberName(parseInt(memberId)) }}</span>
                <span class="text-primary font-medium">¥{{ balance.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="editingWallet ? '编辑钱包' : '新建钱包'" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="钱包名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入钱包名称" />
        </el-form-item>
        <el-form-item label="成员余额" prop="balance_by_member">
          <div class="w-full space-y-2">
            <div v-for="member in members" :key="member.id" class="flex items-center space-x-2">
              <span class="w-24 text-sm">{{ member.name }}</span>
              <el-input-number 
                v-model="form.balance_by_member[member.id]" 
                :min="0" 
                :precision="2" 
                :step="100"
                class="flex-1"
                placeholder="输入余额"
              />
              <span class="w-20 text-right text-sm text-muted-foreground">¥{{ (form.balance_by_member[member.id] || 0).toFixed(2) }}</span>
            </div>
            <div class="text-sm text-muted-foreground pt-2">
              总余额: <span class="font-bold text-primary">¥{{ totalFormBalance.toFixed(2) }}</span>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiClient } from '@/api/client'

const trips = ref([])
const members = ref([])
const wallets = ref([])
const selectedTripId = ref(null)
const dialogVisible = ref(false)
const editingWallet = ref(null)
const formRef = ref(null)

const form = ref({
  name: '',
  trip_id: null,
  balance_by_member: {}
})

const rules = {
  name: [{ required: true, message: '请输入钱包名称', trigger: 'blur' }]
}

const selectedTrip = computed(() => {
  return trips.value.find(t => t.id === selectedTripId.value)
})

const totalFormBalance = computed(() => {
  return Object.values(form.value.balance_by_member).reduce((sum, val) => sum + (val || 0), 0)
})

const totalBalance = (wallet) => {
  if (!wallet.balance_by_member) return 0
  return Object.values(wallet.balance_by_member).reduce((sum, val) => sum + (val || 0), 0)
}

const fetchTrips = async () => {
  try {
    console.log('📡 Fetching trips...')
    const data = await apiClient.trips.list()
    console.log('✅ Trips received:', data)
    trips.value = data
    if (trips.value.length > 0) {
      selectedTripId.value = trips.value[0].id
      console.log('✅ Selected trip:', selectedTripId.value)
      await fetchWallets()
    }
  } catch (error) {
    console.error('❌ 获取行程列表失败:', error)
    ElMessage.error('获取行程列表失败')
  }
}

const fetchMembers = async () => {
  if (!selectedTripId.value) return
  try {
    const data = await apiClient.members.listByTrip(selectedTripId.value)
    members.value = data
  } catch (error) {
    console.error('获取成员列表失败')
  }
}

const fetchWallets = async () => {
  if (!selectedTripId.value) return
  try {
    console.log('📡 Fetching wallets for trip:', selectedTripId.value)
    const data = await apiClient.wallets.list({ trip_id: selectedTripId.value })
    console.log('✅ Wallets received:', data)
    console.log('📊 Wallets count:', Array.isArray(data) ? data.length : 'Not an array')
    wallets.value = Array.isArray(data) ? data : []
    await fetchMembers()
  } catch (error) {
    console.error('❌ 获取钱包列表失败:', error)
    ElMessage.error('获取钱包列表失败')
  }
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    const balance_by_member = {}
    for (const [memberId, balance] of Object.entries(form.value.balance_by_member)) {
      if (balance > 0) {
        balance_by_member[parseInt(memberId)] = balance
      }
    }
    
    try {
      const payload = {
        name: form.value.name,
        trip_id: selectedTripId.value,
        balance_by_member: Object.keys(balance_by_member).length > 0 ? balance_by_member : null
      }
      
      if (editingWallet.value) {
        await apiClient.wallets.update(editingWallet.value.id, payload)
        ElMessage.success('钱包更新成功')
      } else {
        await apiClient.wallets.create(payload)
        ElMessage.success('钱包创建成功')
      }
      dialogVisible.value = false
      fetchWallets()
    } catch (error) {
      ElMessage.error(editingWallet.value ? '更新失败' : '创建失败')
    }
  })
}

const handleAction = async (command, wallet) => {
  if (command === 'edit') {
    editingWallet.value = wallet
    form.value = {
      name: wallet.name,
      trip_id: wallet.trip_id,
      balance_by_member: { ...wallet.balance_by_member } || {}
    }
    // 确保所有成员都在表单中
    members.value.forEach(m => {
      if (!(m.id in form.value.balance_by_member)) {
        form.value.balance_by_member[m.id] = 0
      }
    })
    dialogVisible.value = true
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

const getMemberName = (memberId) => {
  const member = members.value.find(m => m.id === memberId)
  return member ? member.name : `成员${memberId}`
}

onMounted(() => {
  fetchTrips()
})
</script>
