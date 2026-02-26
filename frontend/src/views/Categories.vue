<template>
  <div class="p-0">
    <div class="mb-6">
      <h2 class="text-2xl font-semibold text-foreground flex items-center">
        <el-icon :size="28" class="mr-3 text-primary"><Grid /></el-icon>
        分类管理
      </h2>
    </div>
    
    <div class="bg-card rounded-xl border border-border shadow-sm">
      <div class="p-4 border-b border-border flex justify-between items-center">
        <el-button type="primary" size="default" @click="showAddDialog">
          <el-icon class="mr-2"><Plus /></el-icon>
          添加分类
        </el-button>
      </div>
      
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column label="图标" width="100">
          <template #default="{ row }">
            <div class="category-icon-wrapper">
              <component :is="getCategoryIcon(row)" :size="24" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="分类名称" min-width="150">
          <template #default="{ row }">
            <span class="font-medium">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.type === 'income' ? 'success' : 'danger'" size="default">
              {{ row.type === 'income' ? '收入' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="100" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

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
          <el-input-number v-model="form.sort_order" :min="0" class="w-full" size="large" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button size="large" @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" size="large" @click="handleSubmit">
          <el-icon class="mr-1.5"><Check /></el-icon>
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
.category-icon-wrapper {
  @apply w-10 h-10 rounded-lg flex items-center justify-center;
  background: linear-gradient(135deg, hsl(var(--primary)) 0%, hsl(199 80% 55%) 100%);
  color: white;
}

:deep(.el-radio.is-bordered) {
  @apply rounded-xl py-3 px-5;
}
</style>
