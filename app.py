from flask import Flask, request, jsonify
import transformers
import torch

app = Flask(__name__)


@app.route("/suggestions", methods=["POST"])
def get_suggestions():
    data = request.get_json()
    text = data.get("text")
    prompt = data.get("prompt")

    # Get suggestions from your AI model (LLaMA or any other NLP model)
    model_id = "meta-llama/Meta-Llama-3-8B"
    pipeline = transformers.pipeline(
        prompt,
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )
    suggestions = pipeline(text)

    return jsonify({"suggestion": suggestions})


if __name__ == "__main__":
    app.run(debug=True)
