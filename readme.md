# SynAI

This is a generic LLM API used for the writing assistant. As a more specific and tailored solution is being developed, this general API serves as a working tool for general use.

---

## Features

- Receive and process user input (`text` and `prompt`) via a POST request.
- Generate suggestions using OpenAI's API.
- Handle and respond to errors.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python python-3.12.6
- Flask
- OpenAI Python SDK
- dotenv for environment variable management

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/omarGIT123/writing-assistant.git
   ```

2. **Install dependencies**
   Use `pip` to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   - Create a `.env` file in the root directory by copying the provided `.env.example` file:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and add your OpenAI API key:
     ```
     OPENAI_KEY=KEY
     ```

4. **Run the application**
   Start the Flask server:
   ```bash
   python app.py
   ```
   The server will run at `http://0.0.0.0:5000` by default.

---

## API Usage

### Endpoint: `/suggestions`

- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "text": "Input text",
    "prompt": "System prompt"
  }
  ```
- **Response:**
  - **Success:**
    ```json
    {
      "suggestion": "Generated suggestion based on input"
    }
    ```
  - **Error:**
    ```json
    {
      "error": "Error message"
    }
    ```

### Example cURL Request

```bash
curl -X POST http://127.0.0.1:5000/suggestions \
-H "Content-Type: application/json" \
-d '{"text": "How can I improve productivity?", "prompt": "Provide actionable tips for productivity."}'
```

---

## Project Structure

```plaintext
├── app.py             # Main application file
├── requirements.txt   # List of dependencies
├── .env.example       # Example environment variable configuration
├── README.md          # Project documentation
```

---

## .env File

The `.env.example` file should contain the following environment variables:

```plaintext
OPENAI_KEY=KEY
```

---

## Notes

- Replace `"meta-llama/llama-3.2-3b-instruct:free"` with the appropriate OpenAI model name if required.
