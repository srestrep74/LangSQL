import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config.constants import Settings


class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = Settings.GMAIL_USERNAME
        self.password = Settings.GMAIL_APP_PASSWORD
        self.from_email = self.username

    async def send_email(self, recipients: list, alert_condition: str):
        print("Sending email...")
        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = recipient
            msg["Subject"] = "Inventory Alert!"
            msg.attach(MIMEText(
                f"<p>{alert_condition} condition has been met. Check your inventory!</p>",
                "html"
            ))

            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.sendmail(self.from_email, recipient, msg.as_string())
            except Exception as e:
                print(f"Failed to send email to {recipient}: {str(e)}")
