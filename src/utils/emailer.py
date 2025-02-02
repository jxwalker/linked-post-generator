import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import Settings

class EmailNotifier:
    def __init__(self):
        self.settings = Settings()
        
    async def send_notification(
        self,
        recipient: str,
        subject: str,
        content: str
    ) -> bool:
        """
        Send email notification
        
        Args:
            recipient: Email address of recipient
            subject: Email subject
            content: Email body content
            
        Returns:
            bool: Whether email was sent successfully
        """
        # Create message
        message = MIMEMultipart()
        message["From"] = self.settings.SMTP_USER
        message["To"] = recipient
        message["Subject"] = subject
        
        # Add body
        message.attach(MIMEText(content, "plain"))
        
        try:
            # Connect to SMTP server
            smtp = aiosmtplib.SMTP(
                hostname=self.settings.SMTP_HOST,
                port=self.settings.SMTP_PORT,
                use_tls=True
            )
            
            await smtp.connect()
            await smtp.login(
                self.settings.SMTP_USER,
                self.settings.SMTP_PASSWORD
            )
            
            # Send email
            await smtp.send_message(message)
            await smtp.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False 