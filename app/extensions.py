from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from rich.console import Console

# Instantiate extensions (no app yet)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
console = Console()
socketio = SocketIO(cors_allowed_origins="*")

login_manager.login_view = "admin.sign_in"
login_manager.login_message_category = "info"
