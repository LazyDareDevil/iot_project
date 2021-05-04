from flask import Flask, abort, request, jsonify
from Devices.system import SystemInfo
from Devices.status import SystemShapshot
from datetime import datetime

app = Flask(__name__)
system_data = SystemInfo()
system_snapshot = SystemShapshot()


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
    res = system_data.add_device(request.json['uid'])
    device = {"uid": request.json['uid'], "status": res, "rpi": system_snapshot.rpi}
    system_snapshot.update_info()
    return jsonify(device), 201


@app.route("/api/v1.0/info/device", methods=['POST'])
def update_info():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    uid = request.json["uid"]
    elem = None
    try:
        for element in system_snapshot.devices:
            if element.uid == uid:
                elem = element
                element.change(1, request.json["light"], request.json["lighter"])
    except Exception:
        pass
    return jsonify(elem.to_dict().add("rpi", system_snapshot.rpi)), 201


@app.route("/api/v1.0/update/device", methods=['GET'])
def update_device():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    uid = request.json["uid"]

    return jsonify({}), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3096)
