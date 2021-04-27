from flask import Flask, abort, request, jsonify

app = Flask(__name__)


@app.route("/api/v1.0/test", methods=['GET'])
def add_device():
    return jsonify({'device': "rpi"}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3096")
