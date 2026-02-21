from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "Flask Portfolio")

    SECRET_KEY = os.getenv("SECRET_KEY", "12345678")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    APP_DIR = "app"

    DEFAULT_AVATAR = "assets/img/default-avatar.png"

    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")

    FLASKY_ADMIN: str = "nasiri.aliabdullah@gmail.com"

    ADMINISTRATOR: str = "ADMINISTRATOR"

    ADMINISTER: str = "ADMINISTER"
