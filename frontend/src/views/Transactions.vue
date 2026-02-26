<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-foreground">支出记录</h1>
      <p class="text-muted-foreground mt-1">记录并分摊旅行支出</p>
    </div>

    <el-card>
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="行程">
          <el-select v-model="queryForm.trip_id" placeholder="选择行程" clearable class="w-[180px]" @change="fetchData">
            <el-option v-for="trip in trips" :key="trip.id" :label="trip.name" :value="trip.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            class="w-[280px]"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">
            <el-icon class="mr-1"><Search /></el-icon>
            查询
          </el-button>
          <el-button type="success" @click="showAddDialog" :disabled="!queryForm.trip_id">
            <el-icon class="mr-1"><Plus /></el-icon>
            记一笔
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="!queryForm.trip_id" class="text-center py-12">
      <el-empty description="请选择一个行程查看支出记录" />
    </el-card>

    <el-card v-else class="overflow-hidden">
      <el-table :data="tableData" stripe class="w-full">
        <el-table-column prop="transaction_date" label="日期" width="120" />
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="wallet.name" label="钱包" width="120" />
        <el-table-column prop="amount" label="金额" width="140">
          <template #default="scope">
            <span class="text-red-600 font-semibold">-¥{{ scope.row.amount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="分摊" width="200">
          <template #default="scope">
            <el-tag size="small" type="info">{{ scope.row.split_method === 'equal' ? '均分' : '按比例' }}</el-tag>
            <span class="ml-2 text-muted-foreground text-sm">{{ getSplitMembersText(scope.row) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">
              <el-icon class="mr-1"><Edit /></el-icon>
              编辑
            </el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">
              <el-icon class="mr-1"><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑支出' : '记一笔'" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="form.amount" :min="0" :precision="2" :step="100" class="w-full" />
        </el-form-item>
        <el-form-item label="日期" prop="transaction_date">
          <el-date-picker v-model="form.transaction_date" type="date" value-format="YYYY-MM-DD" class="w-full" />
        </el-form-item>
        <el-form-item label="钱包" prop="wallet_id">
          <el-select v-model="form.wallet_id" placeholder="选择钱包" class="w-full" @change="handleWalletChange">
            <el-option v-for="wallet in filteredWallets" :key="wallet.id" :label="`${wallet.name} (¥${wallet.balance})`" :value="wallet.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="选择分类" class="w-full">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="分摊方式" prop="split_method">
          <el-radio-group v-model="form.split_method" @change="handleSplitMethodChange">
            <el-radio label="equal">均分</el-radio>
            <el-radio label="ratio">按钱包余额比例</el-radio>
            <el-radio label="custom">自定义比例</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="分摊成员" prop="split_members" v-if="form.split_method === 'equal'">
          <el-checkbox-group v-model="form.split_members">
            <el-checkbox v-for="member in members" :key="member.id" :label="member.id">{{ member.name }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="按钱包余额" v-else-if="form.split_method === 'ratio'">
          <div class="w-full">
            <div v-if="selectedWallet && selectedWallet.balance_by_member">
              <div v-for="(balance, memberId) in selectedWallet.balance_by_member" :key="memberId" class="mb-2 p-2 bg-muted rounded">
                <span class="font-medium">{{ getMemberName(parseInt(memberId)) }}</span>
                <span class="ml-2 text-primary">¥{{ balance.toFixed(2) }}</span>
                <span class="ml-2 text-muted-foreground">({{ getWalletRatio(parseInt(memberId)) }}%)</span>
                <span class="ml-2 text-orange-500">¥{{ getMemberSplit(parseInt(memberId)) }}</span>
              </div>
            </div>
            <div v-else class="text-muted-foreground text-sm">该钱包未配置成员余额</div>
          </div>
        </el-form-item>
        <el-form-item label="自定义比例" v-else-if="form.split_method === 'custom'">
          <div class="w-full space-y-2">
            <div v-for="member in members" :key="member.id" class="flex items-center space-x-2">
              <span class="w-24 text-sm">{{ member.name }}</span>
              <el-slider 
                v-model="form.split_ratios[member.id]" 
                :min="0" 
                :max="1" 
                :step="0.01" 
                :show-tooltip="false" 
                class="flex-1" 
              />
              <span class="w-16 text-right text-sm text-primary">{{ (form.split_ratios[member.id] * 100).toFixed(0) }}%</span>
              <span class="w-20 text-right text-sm text-orange-500">¥{{ (form.amount * (form.split_ratios[member.id] || 0)).toFixed(2) }}</span>
            </div>
            <div v-if="customRatioTotal !== 1" class="text-sm text-orange-500">
              当前总比例: {{ (customRatioTotal * 100).toFixed(0) }}% {{ customRatioTotal < 1 ? '(不足100%)' : '(超过100%)' }}
            </div>
            <div v-else class="text-sm text-green-500">比例分配正确</div>
          </div>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="添加备注..." />
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
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const queryForm = reactive({
  trip_id: null
})

const dateRange = ref([])
const tableData = ref([])
const trips = ref([])
const wallets = ref([])
const members = ref([])
const categories = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  amount: 0,
  transaction_date: new Date().toISOString().split('T')[0],
  trip_id: null,
  wallet_id: null,
  category_id: null,
  split_method: 'equal',
  split_members: [],
  split_ratios: {},
  remark: ''
})

const rules = {
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  transaction_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  wallet_id: [{ required: true, message: '请选择钱包', trigger: 'change' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  split_members: [{ type: 'array', min: 1, message: '请选择分摊成员', trigger: 'change' }]
}

const filteredWallets = computed(() => {
  return wallets.value.filter(w => w.trip_id === queryForm.trip_id)
})

const selectedWallet = computed(() => {
  return wallets.value.find(w => w.id === form.wallet_id)
})

const customRatioTotal = computed(() => {
  return Object.values(form.split_ratios).reduce((sum, val) => sum + (val || 0), 0)
})

const fetchTrips = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/trips/')
    trips.value = data
    if (trips.value.length > 0) {
      queryForm.trip_id = trips.value[0].id
    }
  } catch (error) {
    ElMessage.error('获取行程列表失败')
  }
}

const fetchWallets = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/wallets/')
    wallets.value = data
  } catch (error) {
    ElMessage.error('获取钱包列表失败')
  }
}

const fetchMembers = async () => {
  if (!queryForm.trip_id) return
  try {
    const { data } = await axios.get(`http://localhost:8000/api/members/trip/${queryForm.trip_id}`)
    members.value = data
  } catch (error) {
    ElMessage.error('获取成员列表失败')
  }
}

const fetchCategories = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/categories/')
    categories.value = data
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

const fetchData = async () => {
  if (!queryForm.trip_id) return
  try {
    const params = {
      trip_id: queryForm.trip_id,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    }
    const { data } = await axios.get('http://localhost:8000/api/transactions/', { params })
    tableData.value = data
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  const ratios = {}
  members.value.forEach(m => {
    ratios[m.id] = 0
  })
  Object.assign(form, {
    amount: 0,
    transaction_date: new Date().toISOString().split('T')[0],
    trip_id: queryForm.trip_id,
    wallet_id: null,
    category_id: null,
    split_method: 'equal',
    split_members: [],
    split_ratios: ratios,
    remark: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    amount: row.amount,
    transaction_date: row.transaction_date.split(' ')[0],
    trip_id: row.trip_id,
    wallet_id: row.wallet_id,
    category_id: row.category_id,
    split_method: row.split_method || 'equal',
    split_members: row.split_members || [],
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除这条记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axios.delete(`http://localhost:8000/api/transactions/${row.id}`)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleWalletChange = () => {
  if (form.split_method === 'equal') {
    form.split_members = []
  }
}

const handleSplitMethodChange = () => {
  if (form.split_method === 'equal') {
    form.split_members = []
  } else if (form.split_method === 'custom' && Object.keys(form.split_ratios).length === 0) {
    const ratios = {}
    members.value.forEach(m => {
      ratios[m.id] = 0
    })
    form.split_ratios = ratios
  }
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

const getWalletRatio = (memberId) => {
  if (!selectedWallet.value || !selectedWallet.value.balance_by_member) return 0
  const memberBalance = selectedWallet.value.balance_by_member[memberId] || 0
  const totalBalance = Object.values(selectedWallet.value.balance_by_member).reduce((sum, val) => sum + (val || 0), 0)
  if (totalBalance === 0) return 0
  return ((memberBalance / totalBalance) * 100).toFixed(1)
}

const getMemberSplit = (memberId) => {
  if (!selectedWallet.value || !selectedWallet.value.balance_by_member) return '0.00'
  const memberBalance = selectedWallet.value.balance_by_member[memberId] || 0
  const totalBalance = Object.values(selectedWallet.value.balance_by_member).reduce((sum, val) => sum + (val || 0), 0)
  if (totalBalance === 0) return '0.00'
  const split = (form.amount * memberBalance / totalBalance).toFixed(2)
  return split
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    // 处理自定义比例
    let payload = { ...form }
    if (form.split_method === 'custom') {
      // 过滤掉比例为0的成员
      const ratios = {}
      for (const [memberId, ratio] of Object.entries(form.split_ratios)) {
        if (ratio > 0) {
          ratios[parseInt(memberId)] = ratio
        }
      }
      payload.split_ratios = ratios
      payload.split_members = Object.keys(ratios).map(id => parseInt(id))
    } else {
      payload.split_ratios = null
    }
    
    try {
      if (isEdit.value) {
        await axios.put(`http://localhost:8000/api/transactions/${form.id}`, payload)
        ElMessage.success('更新成功')
      } else {
        await axios.post('http://localhost:8000/api/transactions/', payload)
        ElMessage.success('添加成功')
      }
      dialogVisible.value = false
      fetchData()
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
    }
  })
}

watch(() => queryForm.trip_id, (newVal) => {
  if (newVal) {
    fetchMembers()
    fetchData()
  }
})

onMounted(() => {
  fetchTrips()
  fetchWallets()
  fetchCategories()
})
</script>
