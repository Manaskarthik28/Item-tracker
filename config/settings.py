import os 
from dotenv import load_dotenv

# load the variables
load_dotenv()

# .env shape
class Settings:
    USER_NAME: str = os.getenv("USER_NAME")
    PASSWORD: str = os.getenv("PASSWORD")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGO: str = os.getenv("ALGO")

