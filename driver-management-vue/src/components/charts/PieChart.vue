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
  width?: string
  height?: string
  showLegend?: boolean
  radius?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  width: '100%',
  height: '300px',
  showLegend: true,
  radius: () => ['40%', '70%']
})

const chartContainer = ref<HTMLDivElement>()
let chartInstance: echarts.ECharts | null = null

const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316']

const initChart = async () => {
  await nextTick()
  
  if (!chartContainer.value) {
    console.warn('Chart container not found, retrying...')
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
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      show: props.showLegend && props.data.length <= 10
    },
    series: [
      {
        name: props.title,
        type: 'pie',
        radius: props.radius,
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: props.data.map((item, index) => ({
          name: item.name,
          value: item.value,
          itemStyle: {
            color: colors[index % colors.length]
          }
        }))
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