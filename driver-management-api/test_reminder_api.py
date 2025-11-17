#!/usr/bin/env python3
"""
测试提醒API端点
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 登录获取token
def login():
    """登录获取访问令牌"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 20000:
            return result["data"]["access_token"]
    
    print(f"登录失败: {response.status_code}")
    return None

def test_reminder_endpoints():
    """测试提醒API端点"""
    print("测试提醒API端点")
    print("="*50)
    
    # 获取访问令牌
    token = login()
    if not token:
        print("无法获取访问令牌，跳过测试")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试1: 获取提醒设置
    print("\n1. 获取提醒设置")
    response = requests.get(f"{BASE_URL}/reminders/settings", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 成功获取设置: {json.dumps(result.get('data', {}), ensure_ascii=False, indent=2)}")
    else:
        print(f"✗ 获取设置失败: {response.status_code}")
    
    # 测试2: 检查即将到期的项目
    print("\n2. 检查即将到期的项目 (30天)")
    response = requests.get(f"{BASE_URL}/reminders/check?days_ahead=30", headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', {})
        print(f"✓ 检查发现 {data.get('total_count', 0)} 个即将到期的项目")
        if data.get('reminders'):
            for reminder in data['reminders'][:3]:  # 只显示前3个
                print(f"  - {reminder.get('type', 'unknown')}: {reminder.get('days_before')} 天后到期")
    else:
        print(f"✗ 检查失败: {response.status_code}")
    
    # 测试3: 获取提醒仪表板
    print("\n3. 获取提醒仪表板 (30天)")
    response = requests.get(f"{BASE_URL}/reminders/dashboard?days_ahead=30", headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', {})
        print(f"✓ 仪表板数据获取成功")
        print(f"  - 总计到期项目: {data.get('total_count', 0)}")
        stats = data.get('statistics', {})
        print(f"  - 证书到期: {stats.get('certificate_expiry', 0)}")
        print(f"  - 保险到期: {stats.get('insurance_expiry', 0)}")
        print(f"  - 年检到期: {stats.get('inspection_expiry', 0)}")
    else:
        print(f"✗ 获取仪表板失败: {response.status_code}")
    
    # 测试4: 获取后台任务状态
    print("\n4. 获取后台任务状态")
    response = requests.get(f"{BASE_URL}/reminders/tasks/status", headers=headers)
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', {})
        print(f"✓ 任务状态获取成功")
        print(f"  - 运行状态: {data.get('is_running', False)}")
        print(f"  - 任务数量: {data.get('job_count', 0)}")
        jobs = data.get('jobs', [])
        for job in jobs:
            print(f"  - {job.get('name')}: 下次运行 {job.get('next_run_time', '未知')}")
    else:
        print(f"✗ 获取任务状态失败: {response.status_code}")
    
    # 测试5: 手动触发每日检查
    print("\n5. 手动触发每日检查")
    response = requests.post(f"{BASE_URL}/reminders/tasks/trigger?task_type=daily", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✓ 每日检查触发成功")
        print(f"  结果: {json.dumps(result.get('data', {}), ensure_ascii=False)}")
    else:
        print(f"✗ 触发每日检查失败: {response.status_code}")

if __name__ == "__main__":
    test_reminder_endpoints()
    print("\n" + "="*50)
    print("API测试完成!")
    print("="*50)