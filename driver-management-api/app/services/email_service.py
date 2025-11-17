import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """邮件通知服务"""
    
    def __init__(self):
        self.smtp_server = getattr(settings, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_username = getattr(settings, 'SMTP_USERNAME', '')
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', '')
        self.from_email = getattr(settings, 'FROM_EMAIL', self.smtp_username)
        self.enabled = bool(self.smtp_username and self.smtp_password)
    
    def send_reminder_email(self, to_email: str, reminders: List[Dict[str, Any]]) -> bool:
        """发送提醒邮件"""
        if not self.enabled:
            logger.warning("邮件服务未配置，跳过发送")
            return False
            
        try:
            # 创建邮件内容
            subject = f"司机管理系统 - 到期提醒 ({datetime.now().strftime('%Y-%m-%d')})"
            
            # HTML邮件模板
            html_content = self._generate_reminder_html(reminders)
            text_content = self._generate_reminder_text(reminders)
            
            # 创建邮件消息
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # 添加文本和HTML内容
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"提醒邮件发送成功: {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"发送提醒邮件失败: {e}")
            return False
    
    def _generate_reminder_html(self, reminders: List[Dict[str, Any]]) -> str:
        """生成HTML格式的提醒内容"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>司机管理系统 - 到期提醒</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                .reminder-item {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #dc3545; border-radius: 3px; }}
                .certificate {{ border-left-color: #ffc107; }}
                .insurance {{ border-left-color: #17a2b8; }}
                .inspection {{ border-left-color: #28a745; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
                .urgent {{ color: #dc3545; font-weight: bold; }}
                .warning {{ color: #ffc107; font-weight: bold; }}
                .info {{ color: #17a2b8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>司机管理系统</h1>
                    <h2>到期提醒通知</h2>
                </div>
                
                <div class="content">
                    <p>您好！</p>
                    <p>以下是即将到期的项目提醒，请及时处理：</p>
                    
                    {''.join(self._generate_reminder_items_html(reminders))}
                    
                    <p style="margin-top: 20px;">
                        <strong>温馨提示：</strong><br>
                        • 请及时更新相关证件和信息<br>
                        • 确保所有司机和车辆都符合法规要求<br>
                        • 如有疑问，请联系系统管理员
                    </p>
                </div>
                
                <div class="footer">
                    <p>此邮件由司机管理系统自动发送</p>
                    <p>发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_reminder_items_html(self, reminders: List[Dict[str, Any]]) -> List[str]:
        """生成提醒项目的HTML"""
        items = []
        
        for reminder in reminders:
            days_before = reminder["days_before"]
            urgency_class = "urgent" if days_before <= 7 else "warning" if days_before <= 15 else "info"
            
            if reminder["type"] == "certificate_expiry":
                item_class = "reminder-item certificate"
                title = f"证书到期提醒 - {reminder['certificate_type']}"
                content = f"""
                    <strong>司机:</strong> {reminder['driver_name']} ({reminder['driver_phone']})<br>
                    <strong>证书类型:</strong> {reminder['certificate_type']}<br>
                    <strong>证书编号:</strong> {reminder['certificate_number']}<br>
                    <strong>到期日期:</strong> {reminder['expiry_date'].strftime('%Y-%m-%d')}<br>
                    <strong class="{urgency_class}">距离到期还有: {days_before} 天</strong>
                """
            elif reminder["type"] == "insurance_expiry":
                item_class = "reminder-item insurance"
                title = f"车辆保险到期提醒"
                content = f"""
                    <strong>车牌号:</strong> {reminder['vehicle_plate']}<br>
                    <strong>司机:</strong> {reminder['driver_name']} ({reminder['driver_phone']})<br>
                    <strong>到期日期:</strong> {reminder['expiry_date'].strftime('%Y-%m-%d')}<br>
                    <strong class="{urgency_class}">距离到期还有: {days_before} 天</strong>
                """
            elif reminder["type"] == "inspection_expiry":
                item_class = "reminder-item inspection"
                title = f"车辆年检到期提醒"
                content = f"""
                    <strong>车牌号:</strong> {reminder['vehicle_plate']}<br>
                    <strong>司机:</strong> {reminder['driver_name']} ({reminder['driver_phone']})<br>
                    <strong>到期日期:</strong> {reminder['expiry_date'].strftime('%Y-%m-%d')}<br>
                    <strong class="{urgency_class}">距离到期还有: {days_before} 天</strong>
                """
            else:
                continue
            
            item = f"""
                <div class="{item_class}">
                    <h4>{title}</h4>
                    <p>{content}</p>
                </div>
            """
            items.append(item)
        
        return items
    
    def _generate_reminder_text(self, reminders: List[Dict[str, Any]]) -> str:
        """生成纯文本格式的提醒内容"""
        lines = [
            "司机管理系统 - 到期提醒",
            "=" * 30,
            "",
            "您好！",
            "以下是即将到期的项目提醒，请及时处理：",
            ""
        ]
        
        for reminder in reminders:
            days_before = reminder["days_before"]
            
            if reminder["type"] == "certificate_expiry":
                lines.extend([
                    f"【证书到期提醒】",
                    f"司机: {reminder['driver_name']} ({reminder['driver_phone']})",
                    f"证书类型: {reminder['certificate_type']}",
                    f"证书编号: {reminder['certificate_number']}",
                    f"到期日期: {reminder['expiry_date'].strftime('%Y-%m-%d')}",
                    f"距离到期还有: {days_before} 天",
                    ""
                ])
            elif reminder["type"] == "insurance_expiry":
                lines.extend([
                    f"【车辆保险到期提醒】",
                    f"车牌号: {reminder['vehicle_plate']}",
                    f"司机: {reminder['driver_name']} ({reminder['driver_phone']})",
                    f"到期日期: {reminder['expiry_date'].strftime('%Y-%m-%d')}",
                    f"距离到期还有: {days_before} 天",
                    ""
                ])
            elif reminder["type"] == "inspection_expiry":
                lines.extend([
                    f"【车辆年检到期提醒】",
                    f"车牌号: {reminder['vehicle_plate']}",
                    f"司机: {reminder['driver_name']} ({reminder['driver_phone']})",
                    f"到期日期: {reminder['expiry_date'].strftime('%Y-%m-%d')}",
                    f"距离到期还有: {days_before} 天",
                    ""
                ])
        
        lines.extend([
            "温馨提示：",
            "• 请及时更新相关证件和信息",
            "• 确保所有司机和车辆都符合法规要求",
            "• 如有疑问，请联系系统管理员",
            "",
            f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "此邮件由司机管理系统自动发送"
        ])
        
        return "\n".join(lines)

# 全局邮件服务实例
email_service = EmailService()