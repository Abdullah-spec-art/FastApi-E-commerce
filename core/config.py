import os
from dotenv import dotenv_values,load_dotenv

load_dotenv()
class Settings:
    PROJECT_NAME:str = "E-Commerce 🤖"
    PROJECT_VERSION:str = "1.0.0"
    PROJECT_DESCRIPTION:str = "An simple E-commerce"
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST : str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
    DATABASE_URL = "postgresql://postgres:System@localhost:5432/E-commerce"
settings = Settings()

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
