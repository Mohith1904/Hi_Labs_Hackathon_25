
import json
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

from database_setup import setup_database, get_db_schema
from query_generator import generate_sql_query

app = Flask(__name__)
CORS(app) 


print("Setting up the database...")
db_connection = setup_database()
db_schema = get_db_schema(db_connection)
print("Database schema loaded.")

@app.route('/')
def index():
    return "<h1>Provider Data Quality Analytics API</h1><p>Send POST requests to /chat to ask questions.</p>"

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    """
    Directly executes SQL queries without AI generation - for dashboard use.
    """
    sql_query = request.json.get('sql')
    if not sql_query:
        return jsonify({"error": "No SQL query provided"}), 400

    print(f"\nExecuting SQL directly: {sql_query}")

    try:
        # Use pandas to execute query and get a DataFrame
        results_df = pd.read_sql_query(sql_query, db_connection)
        results_json = results_df.to_json(orient='records')
        # Parse it back to a Python object to be re-serialized by jsonify
        response_data = json.loads(results_json)
        
        print(f"Direct SQL execution successful. Returning {len(response_data)} records.")
        return jsonify({
            "sql_query": sql_query,
            "results": response_data
        })

    except Exception as e:
        print(f"Error executing direct SQL: {e}")
        return jsonify({
            "error": "Failed to execute SQL query.",
            "details": str(e),
            "sql_query": sql_query
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles incoming chat messages, generates SQL, executes it, and returns results.
    """
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    print(f"\nReceived question: {user_question}")

    #Generate SQL from the user's question
    sql_query = generate_sql_query(user_question, db_schema)
    print(f"Generated SQL: {sql_query}")

    #Execute the query and handle potential errors
    try:
        # Use pandas to execute query and get a DataFrame
        results_df = pd.read_sql_query(sql_query, db_connection)
        results_json = results_df.to_json(orient='records')
        response_data = json.loads(results_json)
        
        print(f"Query successful. Returning {len(response_data)} records.")
        return jsonify({
            "question": user_question,
            "sql_query": sql_query,
            "results": response_data
        })

    except Exception as e:
        print(f"Error executing query: {e}")
        return jsonify({
            "error": "Failed to execute query.",
            "details": str(e),
            "sql_query": sql_query
        }), 500

if __name__ == '__main__':
    # Runs the Flask server
    app.run(debug=True, port=5001)