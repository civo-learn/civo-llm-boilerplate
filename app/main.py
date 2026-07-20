import os

from flask import Flask, jsonify
from openai import OpenAI

app = Flask(__name__)

OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_BASE_URL",
    "http://ollama.ollama.svc.cluster.local:11434"
)
MODEL = os.environ.get("MODEL", "llama3.3:latest")

client = OpenAI(base_url=f"{OLLAMA_BASE_URL}/v1", api_key="ollama")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/")
def generate():
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a motivational quote."},
            ],
            timeout=30,
        )
        return response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
