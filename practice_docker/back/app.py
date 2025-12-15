from flask import Flask, jsonify, request
import os # Import the os module

app = Flask(__name__)

# Define the file path within the container
DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "words.txt")

@app.route("/")
def home():
   return jsonify({"msg": "Hello from backend!"})

@app.route("/analyze", methods=["POST"])
def analyze():
   payload = request.json or {}
   text = payload.get("text", "")
   # simple demo analysis: length and word count
   length = len(text)
   words = len(text.split())
   save_word(text)
   return jsonify({"length": length, "words": words}) # Added return statement

def save_word(word):
    # Ensure the directory exists before attempting to open the file
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")
        
    with open(DATA_FILE, "a") as f:
        f.write(word + "\n")
    # You were calling read_words() here, removed for simplicity
    print(f"Saved word: {word} to {DATA_FILE}")


def read_words():
    try:
        with open(DATA_FILE, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []
 

if __name__ == "__main__":
   # bind to 0.0.0.0 so container exposes the port to the network
   app.run(host="0.0.0.0", port=5000)

