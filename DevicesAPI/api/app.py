from flask import Flask, abort, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def index():
    return ""


@app.route("/api/v1.0/rpi", methods=['GET'])
def rpi():
    return "check"


@app.route("/api/v1.0/rpi/device", method=['POST'])
def add_device():
    return


if __name__ == '__main__':
    app.run(debug=True)
