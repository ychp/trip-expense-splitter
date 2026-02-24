<template>
  <div class="categories">
    <div class="page-header">
      <h2>
        <el-icon :size="28" style="margin-right: 12px; color: var(--primary-color)"><Grid /></el-icon>
        分类管理
      </h2>
    </div>
    
    <el-button type="primary" size="large" @click="showAddDialog" class="add-btn">
      <el-icon style="margin-right: 8px"><Plus /></el-icon>
      添加分类
    </el-button>

    <el-row :gutter="20" class="categories-grid">
      <el-col :span="8" v-for="category in tableData" :key="category.id">
        <div class="category-card" :class="category.type === 'income' ? 'income-card' : 'expense-card'">
          <div class="category-header">
            <div class="category-icon">
              <component :is="getCategoryIcon(category)" :size="32" />
            </div>
            <div class="category-actions">
              <el-button link type="primary" @click="handleEdit(category)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button link type="danger" @click="handleDelete(category)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="category-name">{{ category.name }}</div>
          <div class="category-type">
            <el-tag :type="category.type === 'income' ? 'success' : 'danger'" size="small">
              {{ category.type === 'income' ? '收入' : '支出' }}
            </el-tag>
          </div>
          <div class="category-order">
            <span class="order-label">排序</span>
            <span class="order-value">{{ category.sort_order }}</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑分类' : '添加分类'"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" size="large" />
        </el-form-item>
        <el-form-item label="分类类型" prop="type">
          <el-radio-group v-model="form.type" size="large">
            <el-radio label="income" border>收入</el-radio>
            <el-radio label="expense" border>支出</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" style="width: 100%" size="large" />
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
  Coffee,
  Van,
  ShoppingBag,
  Film,
  FirstAidKit,
  Reading,
  House,
  Phone,
  More,
  Wallet,
  Present,
  TrendCharts,
  Coin,
  Grid,
  Plus,
  Edit,
  Delete,
  Check
} from '@element-plus/icons-vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'

const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  type: 'expense',
  sort_order: 0
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择分类类型', trigger: 'change' }],
  sort_order: [{ required: true, message: '请输入排序', trigger: 'blur' }]
}

const getCategoryIcon = (category) => {
  const expenseIcons = {
    '餐饮': Coffee,
    '交通': Van,
    '购物': ShoppingBag,
    '娱乐': Film,
    '医疗': FirstAidKit,
    '教育': Reading,
    '居住': House,
    '通讯': Phone,
    '其他支出': More
  }
  
  const incomeIcons = {
    '工资': Wallet,
    '奖金': Present,
    '投资收益': TrendCharts,
    '其他收入': Coin
  }
  
  if (category.type === 'income') {
    return incomeIcons[category.name] || Coin
  }
  return expenseIcons[category.name] || More
}

const fetchData = async () => {
  try {
    tableData.value = await getCategories()
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(form, {
    name: '',
    type: 'expense',
    sort_order: 0
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    name: row.name,
    type: row.type,
    sort_order: row.sort_order
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该分类吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteCategory(row.id)
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
      await updateCategory(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createCategory(form)
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
.categories {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.add-btn {
  margin-bottom: 24px;
}

.categories-grid {
  margin-top: 20px;
}

.category-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.category-card.income-card::before {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.category-card.expense-card::before {
  background: linear-gradient(90deg, #f093fb, #f5576c);
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.category-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.income-card .category-icon {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.expense-card .category-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.category-actions {
  display: flex;
  gap: 8px;
}

.category-actions .el-button {
  font-size: 18px;
}

.category-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.category-type {
  margin-bottom: 12px;
}

.category-order {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.order-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.order-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color);
}

:deep(.el-radio.is-bordered) {
  border-radius: 10px;
  padding: 12px 20px;
}
</style>
