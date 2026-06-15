from flask import Flask, request, render_template, jsonify
from math import sqrt
from datetime import datetime

app = Flask('my_distance')

distances = []


def parse_point(point_str):
    if not point_str or not point_str.strip():
        raise ValueError("Le point ne peut pas etre vide")
    parts = point_str.strip().split(',')
    if len(parts) < 2:
        raise ValueError(f"Format invalide '{point_str}' : attendu 'x,y'")
    try:
        return tuple(float(c.strip()) for c in parts[:2])
    except ValueError:
        raise ValueError(f"Coordonnees invalides dans '{point_str}' : attendu des nombres")


def calculate_distance(point_a, point_b):
    return sqrt((point_b[0] - point_a[0])**2 + (point_b[1] - point_a[1])**2)


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None, error=None)

    try:
        point_a = parse_point(request.form.get('point_a', ''))
        point_b = parse_point(request.form.get('point_b', ''))
    except ValueError as e:
        return render_template('index.html', result=None, error=str(e))

    result = {
        'requested_at': datetime.now().isoformat(),
        'result_distance': calculate_distance(point_a, point_b),
        'point_a': list(point_a),
        'point_b': list(point_b),
    }
    distances.append(result)
    return render_template('index.html', result=result, error=None)


@app.route('/api/distances', methods=['GET'])
def get_distances():
    return jsonify(distances)


@app.route('/api/distance', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Corps JSON requis'}), 400

    try:
        point_a = parse_point(data.get('point_a', ''))
        point_b = parse_point(data.get('point_b', ''))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    result = {
        'requested_at': datetime.now().isoformat(),
        'result_distance': calculate_distance(point_a, point_b),
        'point_a': list(point_a),
        'point_b': list(point_b),
    }
    distances.append(result)
    return jsonify(result), 201
