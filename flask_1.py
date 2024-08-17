from flask import Flask, request, jsonify, make_response
import pandas as pd
import sqlite3
import io
import os

app = Flask(__name__)

# In-memory SQLite database
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store uploaded data
cursor.execute('''
    CREATE TABLE data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
''')
conn.commit()

# API Key for Basic Authentication
API_KEY = os.getenv("API_KEY", "mysecretapikey")

# Helper function to check API Key
def check_api_key(api_key):
    return api_key == API_KEY

# Endpoint to upload CSV file
@app.route('/upload', methods=['POST'])
def upload_csv():
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return make_response(jsonify({"message": "Unauthorized"}), 401)

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"message": "Invalid file format. Only CSV is allowed."}), 400

    try:
        df = pd.read_csv(file)
        df.to_sql('data', conn, if_exists='replace', index=False)
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to process file", "error": str(e)}), 500

# Endpoint to retrieve summary statistics
@app.route('/statistics', methods=['GET'])
def get_statistics():
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return make_response(jsonify({"message": "Unauthorized"}), 401)

    try:
        df = pd.read_sql_query("SELECT * FROM data", conn)
        summary = df.describe().to_dict()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve statistics", "error": str(e)}), 500

# Endpoint to query data
@app.route('/query', methods=['GET'])
def query_data():
    api_key = request.headers.get('API-Key')
    if not check_api_key(api_key):
        return make_response(jsonify({"message": "Unauthorized"}), 401)

    column = request.args.get('column')
    value = request.args.get('value')

    if not column or not value:
        return jsonify({"message": "Column and value parameters are required"}), 400

    try:
        df = pd.read_sql_query(f"SELECT * FROM data WHERE {column} = ?", conn, params=(value,))
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "Failed to query data", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
