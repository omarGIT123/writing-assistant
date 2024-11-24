from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from db_handler import PGhandler

load_dotenv()
app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_KEY"),
)

# Initialize db
db_handler = PGhandler()


@app.route("/suggestions", methods=["POST"])
def get_suggestions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data is required"}), 400

    text = data.get("text")
    prompt = data.get("prompt")
    file_id = data.get("file_id") # file_id here is the id of the docs file ! 

    # Check for missing fields
    if not text or not prompt or not file_id:
        return jsonify({"error": "'text', 'prompt', and 'file_id' are required"}), 400

    try:
        # Add input to history
        db_handler.add_history(file_id, text)
        db_handler.clean_history(file_id, max_records=20)

        # Fetch user history for pattern recognition
        user_history = db_handler.get_user_history(file_id, limit=20)
        history_pattern = " ".join(user_history)

        # Generate suggestions using OpenAI
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": f"{prompt}. \nAnalyze the following previous textual entries to identify key writing patterns, thought processes, habits, and unique characteristics of the user. 
                    Use these insights to tailor your suggestions for maximum relevance and personalization: {history_pattern}",
                },
                {"role": "user", "content": text},
            ],
        )
        suggestion = response.choices[0].message.content

        return jsonify({"suggestion": suggestion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
