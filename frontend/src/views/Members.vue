<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold">成员管理</h3>
      <el-button type="primary" size="small" @click="dialogVisible = true">
        <el-icon class="mr-1"><Plus /></el-icon>
        添加成员
      </el-button>
    </div>

    <div v-if="members.length === 0" class="text-center py-8 text-muted-foreground">
      暂无成员
    </div>

    <div v-else class="flex flex-wrap gap-2">
      <el-tag v-for="member in members" :key="member.id" closable size="large" @close="handleDelete(member)">
        {{ member.name }}
      </el-tag>
    </div>

    <el-dialog v-model="dialogVisible" title="添加成员" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="成员名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入成员名称" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  tripId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update'])

const members = ref([])
const dialogVisible = ref(false)
const formRef = ref(null)

const form = ref({
  name: '',
  trip_id: props.tripId
})

const rules = {
  name: [{ required: true, message: '请输入成员名称', trigger: 'blur' }]
}

const fetchMembers = async () => {
  try {
    const data = await apiClient.members.listByTrip(props.tripId)
    members.value = data
    emit('update', data)
  } catch (error) {
    ElMessage.error('获取成员列表失败')
  }
}

const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      await apiClient.members.create(form.value)
      ElMessage.success('成员添加成功')
      dialogVisible.value = false
      form.value.name = ''
      fetchMembers()
    } catch (error) {
      ElMessage.error('添加失败')
    }
  })
}

const handleDelete = async (member) => {
  try {
    await ElMessageBox.confirm(`确定要删除成员"${member.name}"吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await apiClient.members.delete(member.id)
    ElMessage.success('删除成功')
    fetchMembers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchMembers()
})

defineExpose({
  fetchMembers
})
</script>
