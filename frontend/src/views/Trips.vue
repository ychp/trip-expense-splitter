<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-foreground">行程管理</h1>
        <p class="text-muted-foreground mt-1">管理您的旅行行程</p>
      </div>
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon class="mr-1"><Plus /></el-icon>
        新建行程
      </el-button>
    </div>

    <el-card v-if="trips.length === 0" class="text-center py-12">
      <el-empty description="暂无行程，点击右上角创建新行程" />
    </el-card>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <el-card v-for="trip in trips" :key="trip.id" class="hover:shadow-lg transition-shadow cursor-pointer" @click="viewTrip(trip.id)">
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-semibold text-lg">{{ trip.name }}</span>
            <div class="flex items-center space-x-2" @click.stop>
              <el-tag :type="trip.status === 'planning' ? 'warning' : trip.status === 'ongoing' ? 'success' : 'info'" size="small">
                {{ statusMap[trip.status] || trip.status }}
              </el-tag>
              <el-dropdown @command="(cmd) => handleAction(cmd, trip)">
                <el-icon class="cursor-pointer"><MoreFilled /></el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </template>
        <div class="space-y-2 text-sm">
          <div v-if="trip.description" class="text-muted-foreground line-clamp-2">{{ trip.description }}</div>
          <div v-if="trip.start_date || trip.end_date" class="flex items-center text-muted-foreground">
            <el-icon class="mr-1"><Calendar /></el-icon>
            {{ formatDateRange(trip.start_date, trip.end_date) }}
          </div>
        </div>
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="editingTrip ? '编辑行程' : '新建行程'" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="行程名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入行程名称" />
        </el-form-item>
        <el-form-item label="行程描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入行程描述（可选）" />
        </el-form-item>
        <el-form-item label="参与成员" prop="members" v-if="!editingTrip">
          <el-input 
            v-model="form.members" 
            type="textarea" 
            :rows="2" 
            placeholder="请输入成员名称，用逗号或换行分隔&#10;例如：张三, 李四, 王五" 
          />
          <div class="text-xs text-muted-foreground mt-1">每个成员名称占一行</div>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" placeholder="选择开始日期" class="w-full" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" placeholder="选择结束日期" class="w-full" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="选择状态" class="w-full">
            <el-option label="计划中" value="planning" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已完成" value="completed" />
          </el-select>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, MoreFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

const trips = ref([])
const dialogVisible = ref(false)
const editingTrip = ref(null)
const formRef = ref(null)

const form = ref({
  name: '',
  description: '',
  members: '',
  start_date: '',
  end_date: '',
  status: 'planning'
})

const statusMap = {
  planning: '计划中',
  ongoing: '进行中',
  completed: '已完成'
}

const rules = {
  name: [{ required: true, message: '请输入行程名称', trigger: 'blur' }]
}

const fetchTrips = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/trips/')
    trips.value = data
  } catch (error) {
    ElMessage.error('获取行程列表失败')
  }
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      if (editingTrip.value) {
        await axios.put(`http://localhost:8000/api/trips/${editingTrip.value.id}`, form.value)
        ElMessage.success('行程更新成功')
      } else {
        const members = form.value.members
        delete form.value.members
        
        const { data: trip } = await axios.post('http://localhost:8000/api/trips/', form.value)
        
        if (members && members.trim()) {
          const memberNames = members
            .split(/[,\n]/)
            .map(name => name.trim())
            .filter(name => name.length > 0)
          
          if (memberNames.length > 0) {
            const memberPromises = memberNames.map(name =>
              axios.post('http://localhost:8000/api/members/', {
                name,
                trip_id: trip.id
              })
            )
            await Promise.all(memberPromises)
            ElMessage.success(`行程创建成功，已添加 ${memberNames.length} 位成员`)
          } else {
            ElMessage.success('行程创建成功')
          }
        } else {
          ElMessage.success('行程创建成功')
        }
      }
      dialogVisible.value = false
      fetchTrips()
    } catch (error) {
      ElMessage.error(editingTrip.value ? '更新失败' : '创建失败')
    }
  })
}

const viewTrip = (tripId) => {
  router.push(`/trips/${tripId}`)
}

const handleAction = async (command, trip) => {
  if (command === 'edit') {
    editingTrip.value = trip
    form.value = { ...trip }
    dialogVisible.value = true
  } else if (command === 'delete') {
    try {
      await ElMessageBox.confirm('确定要删除这个行程吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await axios.delete(`http://localhost:8000/api/trips/${trip.id}`)
      ElMessage.success('删除成功')
      fetchTrips()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
      }
    }
  }
}

const formatDateRange = (start, end) => {
  if (!start && !end) return ''
  if (!start) return `至 ${end}`
  if (!end) return `${start} 起`
  return `${start} 至 ${end}`
}

onMounted(() => {
  fetchTrips()
})
</script>
