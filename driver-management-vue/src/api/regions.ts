import api from './auth'

export async function getCountries(): Promise<string[]> {
  const res = await api.get('/regions/central-asia/countries')
  const ca = (res.data?.data || []).map((d: any) => d.country)
  return ['中国', ...ca]
}

export async function getProvinces(country: string, q?: string): Promise<string[]> {
  if (country === '中国') {
    const res = await api.get('/regions/china/provinces', { params: { q } })
    const list = res.data?.data || []
    return list.map((p: any) => p.name || p.code)
  } else {
    const res = await api.get('/regions/central-asia/countries', { params: { q } })
    const list = res.data?.data || []
    const item = list.find((d: any) => d.country === country)
    const divs = item?.divisions || []
    const cities = item?.cities || []
    return [...divs, ...cities]
  }
}