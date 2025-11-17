#!/usr/bin/env python3
"""
测试驾照有效期自动提醒功能 - 简化版本
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models import Driver, DriverCertificate, Vehicle, User
from app.services.reminder_service import reminder_service

async def test_existing_data():
    """测试现有数据的提醒功能"""
    print("司机管理系统 - 驾照有效期自动提醒功能测试")
    print("="*60)
    
    async with AsyncSessionLocal() as session:
        # 查找现有的司机和证书数据
        from sqlalchemy import select
        
        # 获取第一个司机
        driver_result = await session.execute(select(Driver).limit(1))
        driver = driver_result.scalar_one_or_none()
        
        if not driver:
            print("⚠ 未找到司机数据，请先运行数据库初始化脚本")
            return
        
        print(f"✓ 找到司机: {driver.name} (电话: {driver.phone})")
        
        # 获取用户邮箱
        user_result = await session.execute(select(User).where(User.id == driver.user_id))
        user = user_result.scalar_one_or_none()
        
        if user:
            print(f"✓ 用户邮箱: {user.email}")
        
        # 获取司机的证书
        cert_result = await session.execute(
            select(DriverCertificate).where(DriverCertificate.driver_id == driver.id)
        )
        certificates = cert_result.scalars().all()
        
        if certificates:
            print(f"✓ 找到 {len(certificates)} 个证书:")
            for cert in certificates:
                print(f"  - {cert.certificate_type}: {cert.certificate_number} (到期: {cert.expiry_date})")
        else:
            print("⚠ 未找到证书，创建测试证书...")
            
            # 创建测试证书，设置为几天后到期
            today = datetime.now().date()
            test_cert = DriverCertificate(
                driver_id=driver.id,
                certificate_type="危险品运输证",
                certificate_number="TEST001",
                issue_date=today - timedelta(days=365),
                expiry_date=today + timedelta(days=15),  # 15天后到期
                issuing_authority="测试发证机构",
                status="valid"
            )
            session.add(test_cert)
            await session.commit()
            await session.refresh(test_cert)
            certificates = [test_cert]
            print(f"✓ 创建测试证书: {test_cert.certificate_type} (到期: {test_cert.expiry_date})")
        
        # 获取司机的车辆
        vehicle_result = await session.execute(
            select(Vehicle).where(Vehicle.current_driver_id == driver.id)
        )
        vehicles = vehicle_result.scalars().all()
        
        if vehicles:
            print(f"✓ 找到 {len(vehicles)} 辆车:")
            for vehicle in vehicles:
                print(f"  - {vehicle.plate_number}: 保险到期 {vehicle.insurance_expiry}, 年检到期 {vehicle.annual_inspection_date}")
        else:
            print("⚠ 未找到车辆，创建测试车辆...")
            
            # 创建测试车辆
            today = datetime.now().date()
            test_vehicle = Vehicle(
                plate_number="京ATEST001",
                vehicle_type="货车",
                brand="东风",
                model="天龙",
                year=2022,
                color="红色",
                engine_number="TESTENGINE001",
                vin_number="TESTVIN001",
                purchase_date=today - timedelta(days=365),
                registration_date=today - timedelta(days=365),
                insurance_expiry=today + timedelta(days=20),  # 20天后到期
                annual_inspection_date=today + timedelta(days=25),  # 25天后到期
                mileage=50000.0,
                fuel_type="柴油",
                fuel_consumption=25.0,
                status="active",
                current_driver_id=driver.id
            )
            session.add(test_vehicle)
            await session.commit()
            await session.refresh(test_vehicle)
            vehicles = [test_vehicle]
            print(f"✓ 创建测试车辆: {test_vehicle.plate_number}")
            print(f"  - 保险到期: {test_vehicle.insurance_expiry}")
            print(f"  - 年检到期: {test_vehicle.annual_inspection_date}")
    
    # 测试提醒检查
    print("\n" + "="*50)
    print("测试提醒检查功能")
    print("="*50)
    
    try:
        reminders = await reminder_service.check_expiring_licenses()
        
        print(f"\n✓ 发现 {len(reminders)} 个即将到期的项目:")
        
        # 按类型分组显示
        cert_reminders = [r for r in reminders if r['type'] == 'certificate_expiry']
        insurance_reminders = [r for r in reminders if r['type'] == 'insurance_expiry']
        inspection_reminders = [r for r in reminders if r['type'] == 'inspection_expiry']
        
        if cert_reminders:
            print(f"\n📄 证书到期提醒 ({len(cert_reminders)} 个):")
            for reminder in cert_reminders:
                print(f"  - {reminder['driver_name']} 的 {reminder['certificate_type']}: {reminder['days_before']} 天后到期")
        
        if insurance_reminders:
            print(f"\n🚗 车辆保险到期提醒 ({len(insurance_reminders)} 个):")
            for reminder in insurance_reminders:
                print(f"  - 车牌 {reminder['vehicle_plate']}: {reminder['days_before']} 天后到期")
        
        if inspection_reminders:
            print(f"\n🔧 车辆年检到期提醒 ({len(inspection_reminders)} 个):")
            for reminder in inspection_reminders:
                print(f"  - 车牌 {reminder['vehicle_plate']}: {reminder['days_before']} 天后到期")
        
        # 测试发送提醒
        if reminders:
            print("\n" + "="*50)
            print("测试发送提醒功能")
            print("="*50)
            
            results = await reminder_service.send_reminders(reminders)
            
            print(f"\n✓ 提醒发送结果:")
            print(f"  总计: {results['total']}")
            print(f"  成功: {results['sent']}")
            print(f"  失败: {results['failed']}")
            
            for detail in results.get('details', []):
                print(f"  - {detail.get('email', '未知')}: {detail.get('status', 'unknown')}")
                if 'error' in detail:
                    print(f"    错误: {detail['error']}")
        
        return reminders
        
    except Exception as e:
        print(f"✗ 提醒检查失败: {e}")
        import traceback
        traceback.print_exc()
        return []

async def main():
    """主测试函数"""
    await test_existing_data()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)

if __name__ == "__main__":
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 运行测试
    asyncio.run(main())