<template>
  <div ref="chartContainer" :style="{ width: width, height: height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

interface ChartData {
  name: string
  value: number
}

interface Props {
  data: ChartData[]
  title?: string
  xAxisName?: string
  yAxisName?: string
  width?: string
  height?: string
  color?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  xAxisName: '',
  yAxisName: '',
  width: '100%',
  height: '300px',
  color: () => ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
})

const chartContainer = ref<HTMLDivElement>()
let chartInstance: echarts.ECharts | null = null

const initChart = async () => {
  await nextTick()
  
  if (!chartContainer.value) {
    console.warn('Chart container not found, retrying...')
    // 如果容器不存在，延迟重试
    setTimeout(() => {
      if (chartContainer.value) {
        initChart()
      }
    }, 100)
    return
  }
  
  try {
    if (chartInstance) {
      chartInstance.dispose()
    }
    
    chartInstance = echarts.init(chartContainer.value)
    updateChart()
  } catch (error) {
    console.error('Failed to initialize chart:', error)
  }
}

const updateChart = () => {
  if (!chartInstance) return
  
  const option: echarts.EChartsOption = {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
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
      name: props.xAxisName,
      data: props.data.map(item => item.name),
      axisLabel: {
        interval: 0,
        rotate: props.data.length > 10 ? 45 : 0
      }
    },
    yAxis: {
      type: 'value',
      name: props.yAxisName
    },
    series: [
      {
        type: 'bar',
        data: props.data.map((item, index) => ({
          value: item.value,
          itemStyle: {
            color: props.color[index % props.color.length]
          }
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
  }
})

watch(() => props.data, () => {
  updateChart()
}, { deep: true })
</script>