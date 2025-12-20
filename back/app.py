from flask import Flask, jsonify, request
import os
import psycopg2 
import time

app = Flask(__name__)

# --- Improved Connection Logic ---
def get_db_connection():
    """Attempts to connect to the database with retries."""
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                connect_timeout=5
            )
            conn.autocommit = True
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database not ready ({e}). Retrying in 2 seconds...")
            time.sleep(2)

# Initial connection check
conn = get_db_connection()

def increment_count():
    global conn
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE word_stats SET total_words = total_words + 1 WHERE id = 1")
    except psycopg2.OperationalError:
        # If connection died, reconnect and try once more
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("UPDATE word_stats SET total_words = total_words + 1 WHERE id = 1")
def get_count_val():
    global conn
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT total_words FROM word_stats WHERE id = 1")
            result = cur.fetchone()
            # result is a tuple like (0,), so we need result[0]
            return result[0] if result else 0 
    except (psycopg2.OperationalError, TypeError):
        conn = get_db_connection()
        return get_count_val()

# --- Routes ---

@app.route("/")
def home():
   return jsonify({"msg": "Hello from backend!"})

@app.route("/count", methods=["GET"])
def count():
   return jsonify({"total_words": get_count_val()})

@app.route("/analyze", methods=["POST"])
def analyze():
   payload = request.json or {}
   text = payload.get("text", "")
   
   # 1. Analyze text
   length = len(text)
   words = len(text.split())
   
   # 2. Save to File (Volume check)
   save_word(text)
   
   # 3. Save to Database (Postgres check)
   increment_count()
   
   return jsonify({"length": length, "words": words})

# --- File Operations ---
DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "words.txt")

def save_word(word):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    with open(DATA_FILE, "a") as f:
        f.write(word + "\n")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

