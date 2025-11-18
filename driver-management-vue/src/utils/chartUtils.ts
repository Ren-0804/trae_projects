export interface ChartData {
  name: string
  value: number
}

export interface TimeSeriesData {
  date: string
  value: number
}

/**
 * 格式化统计数据为图表数据
 */
export function formatStatisticsToChartData(
  data: Array<{ name: string; count: number }>,
  limit: number = 10
): ChartData[] {
  return data
    .sort((a, b) => b.count - a.count)
    .slice(0, limit)
    .map(item => ({
      name: item.name,
      value: item.count
    }))
}

/**
 * 生成时间序列数据（用于趋势图）
 */
export function generateTimeSeriesData(
  months: number = 6,
  baseValue: number = 100,
  growthRate: number = 0.05,
  volatility: number = 0.1
): TimeSeriesData[] {
  const data: TimeSeriesData[] = []
  const currentDate = new Date()
  
  for (let i = months - 1; i >= 0; i--) {
    const date = new Date(currentDate)
    date.setMonth(date.getMonth() - i)
    
    const monthName = date.toLocaleDateString('zh-CN', { month: 'short' })
    const trendFactor = Math.pow(1 + growthRate, months - i - 1)
    const randomFactor = 1 + (Math.random() - 0.5) * volatility
    
    data.push({
      date: monthName,
      value: Math.floor(baseValue * trendFactor * randomFactor)
    })
  }
  
  return data
}

/**
 * 计算百分比分布
 */
export function calculatePercentageDistribution(data: ChartData[]): ChartData[] {
  const total = data.reduce((sum, item) => sum + item.value, 0)
  
  if (total === 0) return data
  
  return data.map(item => ({
    ...item,
    value: Math.round((item.value / total) * 100 * 100) / 100 // 保留两位小数
  }))
}

/**
 * 聚合数据（按名称分组）
 */
export function aggregateData(data: ChartData[]): ChartData[] {
  const aggregated: Record<string, number> = {}
  
  data.forEach(item => {
    const existingValue = aggregated[item.name]
    if (existingValue !== undefined) {
      aggregated[item.name] = existingValue + item.value
    } else {
      aggregated[item.name] = item.value
    }
  })
  
  return Object.entries(aggregated).map(([name, value]) => ({
    name,
    value
  }))
}

/**
 * 格式化大数据（转换为K/M/B格式）
 */
export function formatLargeNumber(num: number): string {
  if (num >= 1_000_000_000) {
    return (num / 1_000_000_000).toFixed(1) + 'B'
  } else if (num >= 1_000_000) {
    return (num / 1_000_000).toFixed(1) + 'M'
  } else if (num >= 1_000) {
    return (num / 1_000).toFixed(1) + 'K'
  }
  return num.toString()
}

/**
 * 生成颜色数组
 */
export function generateColors(count: number): string[] {
  const baseColors = [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
    '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1'
  ]
  
  const colors: string[] = []
  for (let i = 0; i < count; i++) {
    colors.push(baseColors[i % baseColors.length]!)
  }
  
  return colors
}

/**
 * 格式化图表标题
 */
export function formatChartTitle(title: string, total: number): string {
  return `${title} (总计: ${formatLargeNumber(total)})`
}

/**
 * 创建对比数据
 */
export function createComparisonData(
  current: ChartData[],
  previous: ChartData[]
): Array<{ name: string; current: number; previous: number; change: number }> {
  const currentMap = new Map(current.map(item => [item.name, item.value]))
  const previousMap = new Map(previous.map(item => [item.name, item.value]))
  
  const allNames = new Set([...currentMap.keys(), ...previousMap.keys()])
  
  return Array.from(allNames).map(name => {
    const currentValue = currentMap.get(name) || 0
    const previousValue = previousMap.get(name) || 0
    const change = previousValue === 0 ? 0 : ((currentValue - previousValue) / previousValue) * 100
    
    return {
      name,
      current: currentValue,
      previous: previousValue,
      change: Math.round(change * 100) / 100
    }
  })
}

/**
 * 数据过滤和排序
 */
export function filterAndSortData(
  data: ChartData[],
  minValue: number = 0,
  sortBy: 'value' | 'name' = 'value',
  order: 'asc' | 'desc' = 'desc'
): ChartData[] {
  const filtered = data.filter(item => item.value >= minValue)
  
  filtered.sort((a, b) => {
    if (sortBy === 'value') {
      return order === 'desc' ? b.value - a.value : a.value - b.value
    } else {
      return order === 'desc' ? b.name.localeCompare(a.name) : a.name.localeCompare(b.name)
    }
  })
  
  return filtered
}

/**
 * 创建堆叠数据
 */
export function createStackedData(
  categories: string[],
  series: Array<{ name: string; data: number[] }>
): any {
  return {
    categories,
    series: series.map(s => ({
      name: s.name,
      type: 'bar',
      stack: 'total',
      data: s.data
    }))
  }
}