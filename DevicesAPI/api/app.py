from flask import Flask, abort, request, jsonify
from Devices.system import SystemInfo
from Devices.status import SystemShapshot

app = Flask(__name__)
system_data = SystemInfo()
system_snapshot = SystemShapshot()


@app.route("/api/v1.0/system/device", methods=['POST'])
def add_device():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    res = system_data.add_device(request.json['uid'])
    device = {"uid": request.json['uid'], "status": res}
    system_snapshot.update_info()
    return jsonify({'device': device}), 201


@app.route("/api/v1.0/info/device", methods=['POST'])
def update_info():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    uid = request.json["uid"]
    try:
        for element in system_snapshot.devices:
            if element.uid == uid:
                element.change(1, request.json["light"], request.json["lighter"], request.json["motor"])
    except Exception:
        pass
    device = {"uid": request.json["uid"], "change": 1, "lighter": "100 100 100", "motor": -1}
    return jsonify({'device': device}), 201


if __name__ == '__main__':
    app.run(debug=True)
