from flask import Flask, abort, request, jsonify

app = Flask(__name__)


@app.route("/api/v1.0/test", methods=['GET'])
def add_device():
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3096")
