from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_KEY"),
)


@app.route("/suggestions", methods=["POST"])
def get_suggestions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data is required"}), 400

    text = data.get("text")
    prompt = data.get("prompt")

    # Check for missing fields
    if not text or not prompt:
        return jsonify({"error": "Both 'text' and 'prompt' are required"}), 400

    # Call OpenAI's GPT-3.5 Turbo model for text generation
    try:
        print(text)
        print(prompt)
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
        )
        print("\n here \n")
        suggestion = response.choices[0].message.content
        print(suggestion)
        return jsonify({"suggestion": suggestion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
