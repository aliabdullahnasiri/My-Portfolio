from __future__ import annotations

import os
import pathlib
import re

from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "Flask Portfolio")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "12345678")

    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    APP_DIR: str = "app"

    DEFAULT_AVATAR: str = "assets/img/default-avatar.png"

    UPLOAD_FOLDER: str = os.path.join("app", "static", "uploads")

    FLASKY_ADMIN: str = "nasiri.aliabdullah@gmail.com"

    ADMINISTRATOR: str = "ADMINISTRATOR"

    ADMINISTER: str = "ADMINISTER"

    CURRENCY_SYMBOL: str = chr(36)

    DEFAULT_AVATAR: str = "admin/assets/img/default-avatar.png"

    DEVELOPER: str = "Ali Abdullah Nasiri"

    TD_DIR = f"{APP_DIR}/templates/admin/components/tables/td"

    TD_TEMPS = [TEMP for TEMP in pathlib.Path(TD_DIR).glob("*html")]

    VIEWS_TEMPS_DIR = f"{APP_DIR}/templates/admin/views"

    VIEWS_TEMPS = [TEMP for TEMP in pathlib.Path(VIEWS_TEMPS_DIR).glob("*html")]

    UID_PATTERN: re.Pattern = re.compile(r"^..\d{6}$")
