<template>
  <div class="statistics">
    <div class="page-header">
      <h2>
        <el-icon :size="28" style="margin-right: 12px; color: var(--primary-color)"><DataAnalysis /></el-icon>
        统计分析
      </h2>
    </div>
    
    <el-card class="filter-card">
      <el-form :inline="true">
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
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" class="summary-cards">
      <el-col :span="8">
        <div class="stat-card income-card">
          <div class="card-icon">
            <el-icon :size="48"><TrendCharts /></el-icon>
          </div>
          <div class="card-content">
            <div class="label">总收入</div>
            <div class="value">¥{{ summary.income }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card expense-card">
          <div class="card-icon">
            <el-icon :size="48"><ShoppingCart /></el-icon>
          </div>
          <div class="card-content">
            <div class="label">总支出</div>
            <div class="value">¥{{ summary.expense }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="stat-card balance-card">
          <div class="card-icon">
            <el-icon :size="48"><Wallet /></el-icon>
          </div>
          <div class="card-content">
            <div class="label">结余</div>
            <div class="value">¥{{ summary.balance }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon style="margin-right: 8px"><PieChart /></el-icon>
              <span>支出分类统计</span>
            </div>
          </template>
          <div ref="expensePieChart" style="height: 320px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon style="margin-right: 8px"><PieChart /></el-icon>
              <span>收入分类统计</span>
            </div>
          </template>
          <div ref="incomePieChart" style="height: 320px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <el-icon style="margin-right: 8px"><LineChart /></el-icon>
              <span>收支趋势</span>
            </div>
          </template>
          <div ref="trendChart" style="height: 320px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getSummary, getByCategory, getTrend } from '@/api/statistics'

const dateRange = ref([])
const summary = reactive({
  income: '0.00',
  expense: '0.00',
  balance: '0.00'
})

const expensePieChart = ref(null)
const incomePieChart = ref(null)
const trendChart = ref(null)

let expenseChart = null
let incomeChart = null
let trendChartInstance = null

const fetchData = async () => {
  try {
    const params = {
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    }
    
    const [summaryData, expenseData, incomeData, trendData] = await Promise.all([
      getSummary(params),
      getByCategory({ type: 'expense', ...params }),
      getByCategory({ type: 'income', ...params }),
      getTrend({ type: 'expense', ...params })
    ])
    
    Object.assign(summary, summaryData)
    
    await nextTick()
    renderExpensePie(expenseData)
    renderIncomePie(incomeData)
    renderTrend(trendData)
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

const renderExpensePie = (data) => {
  if (!expensePieChart.value) return
  
  if (!expenseChart) {
    expenseChart = echarts.init(expensePieChart.value)
  }
  
  const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3']
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: ¥{c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: '#64748b'
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold',
            color: '#1e293b'
          },
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map((item, index) => ({ 
          value: item.amount, 
          name: item.category,
          itemStyle: {
            color: colors[index % colors.length]
          }
        }))
      }
    ]
  }
  
  expenseChart.setOption(option)
}

const renderIncomePie = (data) => {
  if (!incomePieChart.value) return
  
  if (!incomeChart) {
    incomeChart = echarts.init(incomePieChart.value)
  }
  
  const colors = ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5', '#059669', '#047857', '#065f46', '#064e3b', '#022c22']
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: ¥{c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: '#64748b'
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold',
            color: '#1e293b'
          },
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map((item, index) => ({ 
          value: item.amount, 
          name: item.category,
          itemStyle: {
            color: colors[index % colors.length]
          }
        }))
      }
    ]
  }
  
  incomeChart.setOption(option)
}

const renderTrend = (data) => {
  if (!trendChart.value) return
  
  if (!trendChartInstance) {
    trendChartInstance = echarts.init(trendChart.value)
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br />支出: ¥{c}',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: {
        color: '#1e293b'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.month),
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#e2e8f0'
        }
      },
      axisLabel: {
        color: '#64748b'
      }
    },
    yAxis: {
      type: 'value',
      name: '金额',
      nameTextStyle: {
        color: '#64748b'
      },
      axisLine: {
        lineStyle: {
          color: '#e2e8f0'
        }
      },
      axisLabel: {
        color: '#64748b'
      },
      splitLine: {
        lineStyle: {
          color: '#f1f5f9',
          type: 'dashed'
        }
      }
    },
    series: [
      {
        name: '支出',
        type: 'line',
        data: data.map(item => item.amount),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: '#667eea' },
              { offset: 1, color: '#764ba2' }
            ]
          }
        },
        itemStyle: {
          color: '#667eea',
          borderColor: '#fff',
          borderWidth: 2,
          shadowColor: 'rgba(102, 126, 234, 0.5)',
          shadowBlur: 10
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(102, 126, 234, 0.4)' },
              { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
            ]
          }
        }
      }
    ]
  }
  
  trendChartInstance.setOption(option)
}

const handleResize = () => {
  expenseChart?.resize()
  incomeChart?.resize()
  trendChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  expenseChart?.dispose()
  incomeChart?.dispose()
  trendChartInstance?.dispose()
})
</script>

<style scoped>
.statistics {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.filter-card {
  margin-bottom: 24px;
}

.summary-cards {
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.income-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.income-card .card-icon {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.income-card .card-content {
  color: #fff;
}

.expense-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.expense-card .card-icon {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.expense-card .card-content {
  color: #fff;
}

.balance-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.balance-card .card-icon {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.balance-card .card-content {
  color: #fff;
}

.card-content {
  flex: 1;
}

.card-content .label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.card-content .value {
  font-size: 32px;
  font-weight: 700;
}

.charts-row {
  margin-bottom: 24px;
}

.chart-card {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: 600;
}
</style>
