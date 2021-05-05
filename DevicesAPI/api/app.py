from flask import Flask, abort, request, jsonify
from Devices.system import SystemInfo
from Devices.status import SystemSnapshot

app = Flask(__name__)
system_snapshot = SystemSnapshot(SystemInfo())


@app.route("/api/v1.0/test", methods=['GET'])
def test_device():
    return jsonify([
        {
            "rpi": "010skdfksh0fsdvknd",
            "uid": "001kfdsvlkdfnk-sdkd21737",
            "timestamp": "1619541760.804093",
            "ph1": "213",
            "lig": "100"
        },
        {
            "rpi": "010skdfksh0fsdvknd",
            "uid": "002kfd23435fnk-sdkd21737",
            "timestamp": "1619541809.18361",
            "ph1": "200",
            "lig": "200"
        },
        {
            "rpi": "010skdfksh0fsdvknd",
            "uid": "001kfdsvlkdfnk-sdkd21737",
            "timestamp": "1619541870.025674",
            "ph1": "70",
            "lig": "400"
        },
        {
            "rpi": "010skdfksh0fsdvknd",
            "uid": "002kfd23435fnk-sdkd21737",
            "timestamp": "1619541887.945385",
            "ph1": "80",
            "lig": "300"
        }
    ]), 201


@app.route("/api/v1.0/system/device", methods=['POST'])
def add_device():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    res = system_snapshot.system_info.add_device(request.json['uid'])
    system_snapshot.update_system()
    device = {"uid": request.json['uid'], "status": res, "rpi": system_snapshot.rpi}
    return jsonify(device), 201


@app.route("/api/v1.0/info/device", methods=['POST'])
def update_info():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    element = system_snapshot.update_info(request.json)
    if element is not None:
        resp = {"uid": element.uid, "status": 1, "rpi": system_snapshot.rpi}
        system_snapshot.save_to_file()
        return jsonify(resp), 201
    else:
        res, code = add_device()
        if code == 201:
            element = system_snapshot.update_info(request.json)
            if element is not None:
                resp = {"uid": element.uid, "status": 1, "rpi": system_snapshot.rpi}
                return jsonify(resp), 201
        system_snapshot.save_to_file()
        abort(400)


@app.route("/api/v1.0/update/device", methods=['GET'])
def update_device():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    uid = request.json["uid"]
    return jsonify({}), 201


@app.route("/api/v1.0/system/snapshot", methods=['GET'])
def get_snapshot():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    return jsonify(system_snapshot.to_dict()), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3096)
    # app.run(debug=True)
