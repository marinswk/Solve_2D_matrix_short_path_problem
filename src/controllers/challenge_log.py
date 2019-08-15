from flask import Blueprint, jsonify
from src.models.puzzle_solver_log import PuzzleSolverLog

challenge_log_endpoints = Blueprint('challenge_log_endpoints', __name__, template_folder='templates')


@challenge_log_endpoints.route('/api/v1/challenge_log/getlogentries', methods=['GET'])
def solve_puzzle():
    try:
        logs = PuzzleSolverLog.query.all()
        logs_list = [dict(
            id=l.id,
            n=l.n,
            grid=l.grid,
            paths=l.paths,
            error_flag=l.error_flag,
            request_time=l.request_time
        ) for l in logs]
        return jsonify(logs_list)
    except Exception as e:
        return jsonify(error_flag=True)
