from app import db


class PuzzleSolverLog(db.Model):
    """
    the model representing one run of the challenge
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    n = db.Column(db.Integer, nullable=False)
    grid = db.Column(db.String(), nullable=False)
    paths = db.Column(db.String(), nullable=True)
    error_flag = db.Column(db.Boolean, nullable=False)
    request_time = db.Column(db.Integer, nullable=False)

