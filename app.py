from flask import Flask, request, render_template, jsonify
from datetime import datetime
from distance import parse_point, calculate_distance

app = Flask('my_distance')

distances = []


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
