from flask import Flask, jsonify, request

from src.model import predict_risk

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy"
        }
    )


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    result = predict_risk(
        data["text"]
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=False
    )