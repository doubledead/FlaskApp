from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    TESTING = getenv("TESTING", "").lower() == "true"
    SECRET_KEY = getenv("SECRET_KEY")
    INVITE_CONFIRMATION_SALT = getenv("INVITE_CONFIRMATION_SALT")

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
