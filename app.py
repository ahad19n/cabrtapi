from requests import post
from random import randint
from polyline import decode
from flask import Flask, request, render_template

sessions = {}
app = Flask(__name__)

# ---------------------------------------------------------------------------- #

def str2Coords(s: str) -> tuple:
    return tuple([float(c) for c in s.split(',')])

def getPolyline(srcLoc, dstLoc):
    response = post('https://valhalla1.openstreetmap.de/route', json={
        'locations': [
            { 'lat': srcLoc[0], 'lon': srcLoc[1], 'radius': 5 },
            { 'lat': dstLoc[0], 'lon': dstLoc[1], 'radius': 5 }
        ],
        'costing': 'auto',
        'directions_options': { 'units': 'km', 'language': 'en-GB' }
    })

    if response.status_code != 200: return ''
    return response.json()['trip']['legs'][0]['shape']

# ---------------------------------------------------------------------------- #

@app.route('/')
def index():
    sKey = request.args.get('sKey')
    zLvl = request.args.get('zLvl', 14)
    uLoc = str2Coords(request.args.get('uLoc'))
    dLoc = str2Coords(request.args.get('dLoc'))

    if sKey not in sessions:
        sessions[sKey] = {}
        sessions[sKey]['idx'] = 0
        sessions[sKey]['points'] = [(p[0] / 10, p[1] / 10) for p in decode(getPolyline(dLoc, uLoc))]

    else:
        sessions[sKey]['idx'] += randint(1, 5)
        if (sessions[sKey]['idx'] >= len(sessions[sKey]['points'])):
            sessions[sKey]['idx'] = len(sessions[sKey]['points']) - 2

    dLoc = sessions[sKey]['points'][sessions[sKey]['idx']]
    return render_template('map.html', uLoc=uLoc, dLoc=dLoc, zLvl=zLvl)

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
