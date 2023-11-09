from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from source.services.auth import auth_service
import logging

from pathlib import Path
from configs import settings


logger = logging.getLogger("uvicorn")

# Use gmail service!!!
email_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "../../front/templates",
)


async def send_email_confirm(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token(
            {"sub": email}, "confirm_email"
        )
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(email_config)

        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as e:
        logger.error(f"Something went wrong in registration email notification")
        logger.error(str(e))


async def send_email_reset(email: EmailStr, username: str, host: str):
    try:
        token_resetting = auth_service.create_email_token(
            {"sub": email}, "reset_password"
        )
        message = MessageSchema(
            subject="Reset your password",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_resetting},
            subtype=MessageType.html,
        )

        fm = FastMail(email_config)

        await fm.send_message(message, template_name="reset_password.html")
    except ConnectionErrors as e:
        logger.error(f"Something went wrong in reset password email")
        logger.error(str(e))
