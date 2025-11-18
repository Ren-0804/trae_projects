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
  smooth?: boolean
  showArea?: boolean
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  xAxisName: '',
  yAxisName: '',
  width: '100%',
  height: '300px',
  smooth: true,
  showArea: false,
  color: '#3b82f6'
})

const chartContainer = ref<HTMLDivElement>()
let chartInstance: echarts.ECharts | null = null

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
  
  const seriesData = props.data.map(item => item.value)
  const xAxisData = props.data.map(item => item.name)
  
  const series: echarts.LineSeriesOption[] = [
    {
      type: 'line',
      data: seriesData,
      smooth: props.smooth,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: props.color
      },
      itemStyle: {
        color: props.color
      },
      emphasis: {
        focus: 'series'
      }
    }
  ]
  
  if (props.showArea) {
    series[0] = {
      ...series[0],
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: props.color + '40' },
          { offset: 1, color: props.color + '10' }
        ])
      }
    }
  }
  
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
      formatter: '{b}: {c}'
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
      boundaryGap: false,
      data: xAxisData,
      axisLabel: {
        interval: 0,
        rotate: xAxisData.length > 10 ? 45 : 0
      }
    },
    yAxis: {
      type: 'value',
      name: props.yAxisName
    },
    series
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