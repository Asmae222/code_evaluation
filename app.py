from flask import Flask, request, render_template
from math import sqrt
from datetime import datetime

app = Flask('my_distance')

distances = list()


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        # Si get, afficher la page vide
        return render_template('index.html', result=None)
    if request.method == 'POST':
        # Si post, calculer et afficher le résultat
        point_a = tuple(int(x) for x in request.form['point_a'].split(',')[:2])
        point_b = list(int(y) for y in request.form['point_b'].split(',')[:2])
        result_distance = sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
        result = {
            'requested_at': datetime.now(),
            'result_distance': result_distance,
            'point_a': list(point_a),
            'point_b': point_b,
        }
        distances.append(result)
        return render_template('index.html', result=result)


@app.route('/api')
def api_index():
    return {}


@app.route('/api/distances')
def get_distances():
    return list({
        'requested_at': x['requested_at'],
        'result_distance': x['result_distance'],
        'point_a': x['point_a'],
        'point_b': x['point_b'],
    } for x in distances)


@app.route('/api/distance', methods=['POST', 'GET', 'PUT'])
def calculate():
    point_a = list(int(y) for y in request.json['point_a'].split(',')[:2])
    point_b = tuple(int(x) for x in request.json['point_b'].split(',')[:2])
    result_distance = sqrt((point_b[0] - point_a[0])**2 + (point_b[1] - point_a[1])**2)
    result = {
        'requested_at': datetime.now(),
        'result_distance': result_distance,
        'point_a': point_a,
        'point_b': list(point_b),
    }
    return result
