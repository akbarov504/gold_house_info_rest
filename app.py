from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_limiter import Limiter
from utils.utils import super_admin_create
from models import db, bcrypt, jwt, migrate
from flask_limiter.util import get_remote_address

from routes.auth_route import auth_bp
from routes.user_route import user_bp
from routes.contact_route import contact_bp
from routes.product_route import product_bp
from routes.language_route import language_bp
from routes.certificate_route import certificate_bp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = "retyj5667452aerftgerw43"
app.config["JWT_SECRET_KEY"] = "qwefeqwhrtyj657245t34ghq3jh5"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://sammy:akbarov@127.0.0.1:5432/gold_house_info_db"
app.config["RATELIMIT_HEADERS_ENABLED"] = True
app.config["RATELIMIT_STRATEGY"] = "moving-window"

Swagger(app, template={
    "info": {
        "title": "Gold House Information API",
        "description": "API documentation for Gold House Information platform",
        "version": "1.0.0"
    }
})
CORS(app)
Limiter(app=app, key_func=get_remote_address, default_limits=["200000 per day", "50000 per hour"])

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(product_bp)
app.register_blueprint(language_bp)
app.register_blueprint(certificate_bp)

with app.app_context():
    db.create_all()
    super_admin_create()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
