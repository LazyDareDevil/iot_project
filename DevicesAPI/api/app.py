from flask import Flask, abort, request, jsonify
from Devices.system import SystemInfo
from Devices.status import SystemSnapshot
from Devices.decision import DecisionBlock

app = Flask(__name__)
system_info = SystemInfo()
system_snapshot = SystemSnapshot(system_info)
decision = DecisionBlock(system_snapshot)


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
        return jsonify(resp), 201
    else:
        abort(400)


@app.route("/api/v1.0/update/device", methods=['POST'])
def update_device():
    if (not request.get_json(force=True)) or (not ('uid' in request.json)):
        abort(400)
    if system_snapshot.auto_decision:
        decision.analyse()
        decision.decision()
    else:
        decision.parse_change()
    uid = request.json["uid"]
    res = None
    for device in decision.devices_to_change:
        if device.uid == uid:
            res = device.to_dict_change()
    if res is not None:
        res["change"] = 1
        return jsonify(res), 201
    else:
        res = {"uid": uid, "change": 0}
        return jsonify(res), 201


@app.route("/api/v1.0/system/automatic", methods=['POST'])
def change_automatic():
    if (not request.get_json(force=True)) or (not ('type' in request.json)):
        abort(400)
    des_type = request.json["type"]
    # if 1 - automatic, 2 - handle
    if des_type == 1:
        system_snapshot.auto_decision = True
    if des_type == 2:
        system_snapshot.auto_decision = False
    return jsonify({"type": des_type}), 201


@app.route("/api/v1.0/change/device", methods=['POST'])
def change_devices():
    if not request.get_json(force=True):
        abort(400)
    res = decision.add_change(request.json)
    if res == 1:
        return jsonify({"apply": 1}), 201
    else:
        return jsonify({"apply": 0, "reason": "wrong data in json"}), 201


@app.route("/api/v1.0/system/snapshot", methods=['GET'])
def get_snapshot():
    return jsonify(system_snapshot.to_dict()), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3096, debug=True)
    # app.run(debug=True)
