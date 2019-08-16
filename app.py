from flask import Flask, request, redirect, url_for, render_template
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


@app.route('/', methods=['GET'])
def index():
    error_flag = request.args.get('error_flag')
    message = request.args.get('message')
    logs_list = request.args.get('logs_list')

    if message or error_flag:
        if not message:
            message = []
        return render_template('index.html', message=message, error_flag=error_flag)
    elif logs_list:
        return render_template('index.html', logs_list=logs_list)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
