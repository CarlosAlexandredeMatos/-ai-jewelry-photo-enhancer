from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

app = FastAPI()

bcrypt_context = CryptContext(['bcrypt'])

from src.routes import auth_router
app.include_router(auth_router)


