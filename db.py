from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(app)
