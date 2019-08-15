from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.controllers.challenge import challenge_endpoints
from src.controllers.challenge_log import challenge_log_endpoints
from src.models import puzzle_solver_log

app.register_blueprint(challenge_endpoints)
app.register_blueprint(challenge_log_endpoints)

if __name__ == '__main__':
    app.run()
