from requests import post
from random import randint
from polyline import decode
from flask import Flask, request, render_template, Response

app = Flask(__name__)

# ---------------------------------------------------------------------------- #

cLoc = []
dLoc = []
uLoc = []

idx = 0
points = []
complete = False

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

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/setClickCoordinates', methods=["POST"])
def recordUserClick():
    global cLoc

    data = request.get_json()
    cLoc = [data['latitude'], data['longitude']]

    return Response(f"OK", status=200, mimetype="text/plain"), 200

@app.route('/getClickCoordinates', methods=["GET"])
def getWhereUserClicked():
    global cLoc

    if len(cLoc):
        return Response(f"{cLoc[0]}, {cLoc[1]}", status=200, mimetype="text/plain"), 200
    else:
        return Response(f"None, None", status=200, mimetype="text/plain"), 200

# ---------------------------------------------------------------------------- #

@app.route('/initTracking', methods=["GET"])
def setTrackingPoints():
    global idx, points, dLoc, uLoc

    uLoc = str2Coords(request.args.get('uLoc'))
    dLoc = str2Coords(request.args.get('dLoc'))

    idx = 0
    points = [(p[0] / 10, p[1] / 10) for p in decode(getPolyline(dLoc, uLoc))]

    return Response(f"OK", status=200, mimetype="text/plain"), 200

@app.route('/showTrackingMap', methods=["GET"])
def showTrackingMap():
    global idx, points, dLoc, uLoc, complete

    idx += randint(1, 5)
    if idx >= len(points):
        complete = True
        idx = len(points) - 2

    dLoc = points[idx]
    return render_template('tracking.html', uLoc=uLoc, dLoc=dLoc)

@app.route('/isTrackingComplete', methods=["GET"])
def isTrackingComplete():
    global complete
    return Response(str(complete), status=200, mimetype="text/plain"), 200

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
