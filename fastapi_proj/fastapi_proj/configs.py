from pydantic import EmailStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL_LOCAL: str
    SQLALCHEMY_DATABASE_URL_DOCKER: str
    REDIS_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file: str = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
