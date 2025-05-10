import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.constants import Settings


def get_base64_logo() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "assets", "logo.png")
    try:
        with open(logo_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error loading logo: {e}")
        return ""


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = Settings.GMAIL_USERNAME
        self.password = Settings.GMAIL_APP_PASSWORD
        self.from_email = self.username

    async def send_email(self, recipients: list, alert_condition: str):
        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = recipient
            msg["Subject"] = "Inventory Alert!"
            logo_base64 = get_base64_logo()
            msg.attach(MIMEText(f"""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="data:image/png;base64,{logo_base64}" alt="LangSQL Logo" style="height: 50px;">
                            <h2 style="color: #6a1b9a;">LangSQL Inventory Alert</h2>
                        </div>
                        <p style="font-size: 16px; color: #333;">
                            <strong>Alert:</strong> {alert_condition} condition has been met.
                        </p>
                        <p style="font-size: 16px; color: #333;">Please check your inventory status.</p>
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="https://yourapp.com/login" style="background-color: #6a1b9a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px;">Go to Dashboard</a>
                        </div>
                        <p style="font-size: 12px; color: #999; text-align: center; margin-top: 20px;">&copy; 2025 LangSQL. All rights reserved.</p>
                        </div>
                    </body>
                </html>
                """, "html")
                       )

            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.sendmail(self.from_email, recipient, msg.as_string())
            except Exception as e:
                print(f"Failed to send email to {recipient}: {str(e)}")
