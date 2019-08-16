from flask import Blueprint, jsonify, request, redirect, url_for
from src.modules.challenge.helper import PuzzleSolver
import time


challenge_endpoints = Blueprint('challenge_endpoints', __name__, template_folder='templates')


@challenge_endpoints.route('/form/solvepuzzle', methods=['POST'])
def solve_puzzle():
    try:
        start = time.time()
        n = int(request.form.get('n'))
        grid = eval(request.form.get('grid').strip())
        solver = PuzzleSolver(n, grid)
        if not solver.error_flag:
            solver.solve_puzzle()
            end = time.time()
            time_elapsed = int(round((end - start) * 1000))
            solver.log(time_elapsed)
            return redirect(url_for('index', message=solver.shortest_paths, error_flag=solver.error_flag))
        else:
            end = time.time()
            time_elapsed = int(round((end - start) * 1000))
            solver.log(time_elapsed)
            return redirect(url_for('index', error_flag=solver.error_flag))

    except Exception as e:
        return redirect(url_for('index', error_flag=True))


@challenge_endpoints.route('/api/v1/challenge/solvepuzzle', methods=['POST'])
def solve_puzzle_endpoint():
    try:
        start = time.time()
        n = request.json.get('N')
        grid = request.json.get('grid')
        solver = PuzzleSolver(n, grid)
        if not solver.error_flag:
            solver.solve_puzzle()
            end = time.time()
            time_elapsed = int(round((end - start) * 1000))
            solver.log(time_elapsed)
            return jsonify(error_flag=solver.error_flag, paths=solver.shortest_paths)
        else:
            end = time.time()
            time_elapsed = int(round((end - start) * 1000))
            solver.log(time_elapsed)
            return jsonify(error_flag=solver.error_flag)

    except Exception:
        return jsonify(error_flag=True, paths=[])