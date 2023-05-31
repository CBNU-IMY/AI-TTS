import os
import requests
from flask import (
    Flask,
    request,
    send_file,
    render_template,
    jsonify,
    Response,
    redirect,
    url_for,
)

from synthesys import synthesize
from text_processer import normalize_text, normalize_multiline_text

app = Flask(__name__)


@app.after_request
def allow_cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

@app.route("/tts-server/api/process-text", methods=["POST"])
def text():
    text = request.json.get("text", "")
    texts = normalize_multiline_text(text)

    return jsonify(texts)


@app.route("/tts-server/api/glowtts")
def infer_glowtts():
    text = request.args.get("text", "")
    text = normalize_text(text).strip()

    if not text:
        return "text 입력은 필수입니다", 400

    try:
        wav = synthesize(text)
        return wav
    except Exception as e:
        return f"Cannot generate audio: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=os.environ.get("TTS_DEBUG", "0") == "1")
