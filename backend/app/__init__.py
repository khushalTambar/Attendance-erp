from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt
from app.models import User
from app.routes.auth import auth_bp
from app.routes.department import department_bp
from app.routes.employee import employee_bp
from app.routes.attendance import attendance_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models import User, Department, Employee, Attendance
    
    @app.route("/")
    def home():
        return {
            "message": "Attendance Management API is running!",
            "status": "success"
        }

    app.register_blueprint(auth_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)

    return app