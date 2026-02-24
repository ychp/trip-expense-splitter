<template>
  <div class="accounts">
    <div class="page-header">
      <h2>
        <el-icon :size="28" style="margin-right: 12px; color: var(--primary-color)"><CreditCard /></el-icon>
        账户管理
      </h2>
    </div>
    
    <el-button type="primary" size="large" @click="showAddDialog" class="add-btn">
      <el-icon style="margin-right: 8px"><Plus /></el-icon>
      添加账户
    </el-button>

    <el-row :gutter="20" class="accounts-grid">
      <el-col :span="8" v-for="account in tableData" :key="account.id">
        <div class="account-card" :class="getTypeClass(account.type)">
          <div class="account-header">
            <div class="account-icon">
              <component :is="getAccountIcon(account.type)" :size="36" />
            </div>
            <div class="account-actions">
              <el-button link type="primary" @click="handleEdit(account)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button link type="danger" @click="handleDelete(account)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="account-name">{{ account.name }}</div>
          <div class="account-type">{{ getTypeName(account.type) }}</div>
          <div class="account-balance">
            <span class="balance-label">余额</span>
            <span class="balance-value">¥{{ account.balance.toFixed(2) }}</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑账户' : '添加账户'"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="账户名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入账户名称" size="large" />
        </el-form-item>
        <el-form-item label="账户类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择账户类型" style="width: 100%" size="large">
            <el-option label="现金" value="cash" />
            <el-option label="银行卡" value="bank" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="微信" value="wechat" />
            <el-option label="投资账户" value="investment" />
          </el-select>
        </el-form-item>
        <el-form-item label="初始余额" prop="balance">
          <el-input-number v-model="form.balance" :min="0" :precision="2" style="width: 100%" size="large" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button size="large" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="large" @click="handleSubmit">
          <el-icon style="margin-right: 6px"><Check /></el-icon>
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Wallet, 
  CreditCard, 
  Coin, 
  ChatDotRound, 
  TrendCharts,
  Edit,
  Delete,
  Plus,
  Check
} from '@element-plus/icons-vue'
import { getAccounts, createAccount, updateAccount, deleteAccount } from '@/api/accounts'

const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  type: 'cash',
  balance: 0
})

const rules = {
  name: [{ required: true, message: '请输入账户名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择账户类型', trigger: 'change' }],
  balance: [{ required: true, message: '请输入初始余额', trigger: 'blur' }]
}

const getTypeName = (type) => {
  const typeMap = {
    cash: '现金',
    bank: '银行卡',
    alipay: '支付宝',
    wechat: '微信',
    investment: '投资账户'
  }
  return typeMap[type] || type
}

const getTypeClass = (type) => {
  const classMap = {
    cash: 'type-cash',
    bank: 'type-bank',
    alipay: 'type-alipay',
    wechat: 'type-wechat',
    investment: 'type-investment'
  }
  return classMap[type] || 'type-cash'
}

const getAccountIcon = (type) => {
  const iconMap = {
    cash: Wallet,
    bank: CreditCard,
    alipay: Coin,
    wechat: ChatDotRound,
    investment: TrendCharts
  }
  return iconMap[type] || Wallet
}

const fetchData = async () => {
  try {
    tableData.value = await getAccounts()
  } catch (error) {
    ElMessage.error('获取账户列表失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(form, {
    name: '',
    type: 'cash',
    balance: 0
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    name: row.name,
    type: row.type,
    balance: row.balance
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该账户吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteAccount(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async () => {
  await formRef.value.validate()
  try {
    if (isEdit.value) {
      await updateAccount(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createAccount(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.accounts {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.add-btn {
  margin-bottom: 24px;
}

.accounts-grid {
  margin-top: 20px;
}

.account-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.account-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 20px 20px 0 0;
}

.account-card.type-cash::before {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.account-card.type-bank::before {
  background: linear-gradient(90deg, #4facfe, #00f2fe);
}

.account-card.type-alipay::before {
  background: linear-gradient(90deg, #43e97b, #38f9d7);
}

.account-card.type-wechat::before {
  background: linear-gradient(90deg, #fa709a, #fee140);
}

.account-card.type-investment::before {
  background: linear-gradient(90deg, #f093fb, #f5576c);
}

.account-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.account-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.type-cash .account-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.type-bank .account-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.type-alipay .account-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.type-wechat .account-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.type-investment .account-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.account-actions {
  display: flex;
  gap: 8px;
}

.account-actions .el-button {
  font-size: 18px;
}

.account-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.account-type {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.account-balance {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.balance-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.balance-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}
</style>
