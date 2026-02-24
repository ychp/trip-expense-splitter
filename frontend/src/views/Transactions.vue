<template>
  <div class="transactions">
    <div class="page-header">
      <h2>
        <el-icon :size="28" style="margin-right: 12px; color: var(--primary-color)"><List /></el-icon>
        流水记录
      </h2>
    </div>
    
    <el-card class="filter-card">
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="类型">
          <el-select v-model="queryForm.type" placeholder="全部" clearable style="width: 140px">
            <el-option label="支出" value="expense" />
            <el-option label="收入" value="income" />
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
            style="width: 280px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">
            <el-icon style="margin-right: 6px"><Search /></el-icon>
            查询
          </el-button>
          <el-button type="success" @click="showAddDialog">
            <el-icon style="margin-right: 6px"><Plus /></el-icon>
            记一笔
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="transaction_date" label="日期" width="120" />
        <el-table-column label="类型" width="90">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'income' ? 'success' : 'danger'" size="large">
              {{ scope.row.type === 'income' ? '收入' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="account.name" label="账户" width="120" />
        <el-table-column prop="amount" label="金额" width="140">
          <template #default="scope">
            <span class="amount" :class="scope.row.type === 'income' ? 'income' : 'expense'">
              {{ scope.row.type === 'income' ? '+' : '-' }}¥{{ scope.row.amount }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">
              <el-icon style="margin-right: 4px"><Edit /></el-icon>
              编辑
            </el-button>
            <el-button link type="danger" @click="handleDelete(scope.row)">
              <el-icon style="margin-right: 4px"><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑流水' : '记一笔'"
      width="540px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="form.type" size="large">
            <el-radio label="expense" border>支出</el-radio>
            <el-radio label="income" border>收入</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number 
            v-model="form.amount" 
            :min="0" 
            :precision="2" 
            :step="100"
            style="width: 100%" 
            size="large"
          />
        </el-form-item>
        <el-form-item label="日期" prop="transaction_date">
          <el-date-picker
            v-model="form.transaction_date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            size="large"
          />
        </el-form-item>
        <el-form-item label="账户" prop="account_id">
          <el-select v-model="form.account_id" placeholder="选择账户" style="width: 100%" size="large">
            <el-option
              v-for="acc in accounts"
              :key="acc.id"
              :label="acc.name"
              :value="acc.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="选择分类" style="width: 100%" size="large">
            <el-option
              v-for="cat in filteredCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="form.remark" 
            type="textarea" 
            :rows="3"
            placeholder="添加备注..."
          />
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
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTransactions, createTransaction, updateTransaction, deleteTransaction } from '@/api/transactions'
import { getAccounts } from '@/api/accounts'
import { getCategories } from '@/api/categories'

const queryForm = reactive({
  type: ''
})

const dateRange = ref([])
const tableData = ref([])
const accounts = ref([])
const categories = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  type: 'expense',
  amount: 0,
  transaction_date: new Date().toISOString().split('T')[0],
  account_id: null,
  category_id: null,
  remark: ''
})

const rules = {
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  transaction_date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  account_id: [{ required: true, message: '请选择账户', trigger: 'change' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const filteredCategories = computed(() => {
  return categories.value.filter(c => c.type === form.type)
})

const fetchData = async () => {
  try {
    const params = {
      type: queryForm.type,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    }
    const res = await getTransactions(params)
    tableData.value = res
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

const fetchAccounts = async () => {
  try {
    accounts.value = await getAccounts()
  } catch (error) {
    ElMessage.error('获取账户失败')
  }
}

const fetchCategories = async () => {
  try {
    categories.value = await getCategories()
  } catch (error) {
    ElMessage.error('获取分类失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(form, {
    type: 'expense',
    amount: 0,
    transaction_date: new Date().toISOString().split('T')[0],
    account_id: accounts.value[0]?.id,
    category_id: null,
    remark: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    type: row.type,
    amount: row.amount,
    transaction_date: row.transaction_date,
    account_id: row.account_id,
    category_id: row.category_id,
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
      await deleteTransaction(row.id)
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
      await updateTransaction(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createTransaction(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  }
}

onMounted(() => {
  fetchAccounts()
  fetchCategories()
  fetchData()
})
</script>

<style scoped>
.transactions {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  overflow: hidden;
}

.amount {
  font-size: 16px;
  font-weight: 600;
}

.amount.income {
  color: var(--success-color);
}

.amount.expense {
  color: var(--danger-color);
}

:deep(.el-radio.is-bordered) {
  border-radius: 10px;
  padding: 12px 20px;
}

:deep(.el-input-number) {
  width: 100%;
}

:deep(.el-input-number .el-input__wrapper) {
  padding-left: 12px;
}
</style>
