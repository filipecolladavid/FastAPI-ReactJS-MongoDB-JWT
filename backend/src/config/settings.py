from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    MONGO_INITDB_DATABASE: str = os.environ["MONGO_INITDB_DATABASE"]

    JWT_PUBLIC_KEY: str = os.environ["JWT_PUBLIC_KEY"]
    JWT_PRIVATE_KEY: str = os.environ["JWT_PRIVATE_KEY"]
    REFRESH_TOKEN_EXPIRES_IN: int = os.environ["REFRESH_TOKEN_EXPIRES_IN"]
    ACCESS_TOKEN_EXPIRES_IN: int = os.environ["ACCESS_TOKEN_EXPIRES_IN"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]

    CLIENT_ORIGIN: str = os.environ["CLIENT_ORIGIN"]

    MINIO_URL: str = os.environ["MINIO_URL"]
    MINIO_ROOT_USER: str = os.environ["MINIO_ROOT_USER"]
    MINIO_ROOT_PASSWORD: str = os.environ["MINIO_ROOT_PASSWORD"]
    MINIO_SECURE: bool = os.environ["MINIO_SECURE"]
        
settings = Settings()