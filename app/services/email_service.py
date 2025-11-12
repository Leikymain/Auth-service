"""Servicio de envío de emails con Resend"""

import logging
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class EmailService:
    @staticmethod
    async def send_password_email(email: str, password: str) -> bool:
        """Envía email con contraseña usando Resend API"""
        try:
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

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {settings.resend_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": "Automatiza tu PYME <no-reply@automapymes.com>",
                        "to": [email],
                        "subject": "Tu contraseña de acceso a Demos IA",
                        "html": html_body
                    }
                )

            if response.status_code == 200:
                logger.info(f"✅ Email enviado correctamente a {email}")
                return True
            else:
                logger.error(f"❌ Error enviando email a {email}: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False
