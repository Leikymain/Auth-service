"""Servicio de envío de emails"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class EmailService:
    @staticmethod
    async def send_password_email(email: str, password: str) -> bool:
        """Envía email con contraseña"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Tu contraseña de acceso a Demos IA"
            msg['From'] = settings.smtp_user
            msg['To'] = email
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; }}
                    .password-box {{ background: white; border: 2px solid #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .password {{ font-size: 24px; font-weight: bold; color: #667eea; letter-spacing: 2px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Bienvenido a las Demos IA</h1>
                    </div>
                    <div class="content">
                        <p>Tu contraseña de acceso:</p>
                        <div class="password-box">
                            <p class="password">{password}</p>
                        </div>
                        <p><strong>Válido por 3 días con 60 requests gratuitos</strong></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email enviado a {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False