from typing import Optional
from fastapi import APIRouter, Query
import httpx
import asyncio

router = APIRouter()

# In-memory caches
_china_meta_cache: Optional[dict] = None
_china_provinces_cache: Optional[list] = None
_china_cities_cache_by_province: dict[str, list] = {}

_central_asia_data = {
    "哈萨克斯坦": {
        "divisions": ["阿拉木图州", "阿斯塔纳市"],
        "cities": ["阿拉木图", "努尔苏丹", "奇姆肯特"],
    },
    "乌兹别克斯坦": {
        "divisions": ["塔什干州", "撒马尔罕州"],
        "cities": ["塔什干", "撒马尔罕", "布哈拉"],
    },
    "土库曼斯坦": {
        "divisions": ["阿哈尔州"],
        "cities": ["阿什哈巴德", "土库曼纳巴特"],
    },
    "吉尔吉斯斯坦": {
        "divisions": ["楚河州"],
        "cities": ["比什凯克", "奥什"],
    },
    "塔吉克斯坦": {
        "divisions": ["索格特州"],
        "cities": ["杜尚别", "苦盏"],
    },
}


async def _fetch_json(url: str) -> dict:
    async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


@router.get("/regions/china/meta")
async def china_meta():
    global _china_meta_cache
    if _china_meta_cache is None:
        _china_meta_cache = await _fetch_json("https://geojson.cn/api/china/_meta.json")
    return _china_meta_cache


@router.get("/regions/china/provinces")
async def china_provinces(q: Optional[str] = Query(None)):
    global _china_meta_cache, _china_provinces_cache
    if _china_meta_cache is None:
        _china_meta_cache = await _fetch_json("https://geojson.cn/api/china/_meta.json")
    if _china_provinces_cache is None:
        _china_provinces_cache = _china_meta_cache.get("provinces", [])
        if not _china_provinces_cache:
            # fallback static provinces
            names = [
                "北京","上海","天津","重庆","河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","台湾","内蒙古","广西","西藏","宁夏","新疆"
            ]
            _china_provinces_cache = [{"name": n, "code": None} for n in names]
    items = _china_provinces_cache
    if q:
        ql = q.lower()
        items = [p for p in items if ql in str(p.get("name", "")).lower() or ql in str(p.get("code", "")).lower()]
    return {"data": items}


@router.get("/regions/china/cities")
async def china_cities(province_code: str = Query(...), q: Optional[str] = Query(None)):
    global _china_cities_cache_by_province
    cities = _china_cities_cache_by_province.get(province_code)
    if cities is None:
        # Attempt to fetch province file if meta provides url pattern
        # Fallback: return empty list when source not directly available
        cities = []
        _china_cities_cache_by_province[province_code] = cities
    result = cities
    if q:
        ql = q.lower()
        result = [c for c in cities if ql in str(c.get("name", "")).lower() or ql in str(c.get("code", "")).lower()]
    return {"data": result}


@router.get("/regions/china/search")
async def china_search(name: Optional[str] = None, code: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None):
    # Basic search across cached provinces
    resp = await china_provinces()
    items = resp["data"]
    out = items
    if name:
        nl = name.lower()
        out = [x for x in out if nl in str(x.get("name", "")).lower()]
    if code:
        out = [x for x in out if str(x.get("code", "")) == str(code)]
    # lat/lon matching would require geometry; meta may not include — return provinces as basic response
    return {"data": out}


@router.get("/regions/central-asia/countries")
async def ca_countries(q: Optional[str] = Query(None)):
    data = []
    for k, v in _central_asia_data.items():
        data.append({"country": k, "divisions": v["divisions"], "cities": v["cities"]})
    if q:
        ql = q.lower()
        data = [d for d in data if ql in d["country"].lower() or any(ql in c.lower() for c in d["cities"])]
    return {"data": data}