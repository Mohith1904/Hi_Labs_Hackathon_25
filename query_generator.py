# query_generator.py
import ollama
from datetime import datetime

# --- 1. Check if Ollama is running ---
try:
    ollama.list() 
    print("✅ Ollama server is running and accessible.")
except Exception as e:
    print(f"❌ Could not connect to Ollama server. Please ensure it is running. Error: {e}")


def generate_sql_query(question: str, schema: str) -> str:
    """
    Dynamically generates an SQL query from a natural language question using Ollama.
    """
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # --- THIS IS THE NEW, MORE DETAILED PROMPT ---
    prompt = f"""
[INST]
You are an expert SQL data analyst. Your task is to convert natural language questions into executable SQLite queries based on the provided database schema.

### DATABASE SCHEMA
{schema}

### CRITICAL RULES
1.  **You MUST only use the column names available in the schema provided.** Do not invent or assume column names. For example, the roster only has `practice_phone`, so DO NOT use non-existent columns like `mailing_phone`.
2.  **Respond with ONLY the SQL query.** Do not add any explanations, introductions, or markdown. Just the code.
3.  Ensure the query is valid for SQLite.

### CONCEPT DEFINITIONS
- A **"phone number formatting issue"** means the `phone_number_clean` column does not have a length of 10.
- **"Unverified licenses"** or **"unverified NPIs"** mean the `is_license_found` or `is_npi_found` columns are 0.
- **"Expired licenses"** means the `is_license_active` column is 0.
- The **"data quality score"** is calculated by averaging the `is_license_found`, `is_license_active`, and `is_npi_found` columns.

### EXAMPLES
- Question: "How many providers have expired licenses in our network?"
- SQL: SELECT COUNT(*) FROM provider_roster WHERE is_license_active = 0;

- Question: "Which providers are missing NPI numbers?"
- SQL: SELECT full_name, primary_specialty FROM provider_roster WHERE npi IS NULL;

- Question: "Show me a summary of all data quality problems by state"
- SQL: SELECT practice_state, COUNT(*) AS total_providers, SUM(CASE WHEN is_license_found = 0 THEN 1 ELSE 0 END) AS unverified_licenses, SUM(CASE WHEN is_npi_found = 0 THEN 1 ELSE 0 END) AS unverified_npis, SUM(CASE WHEN is_license_active = 0 THEN 1 ELSE 0 END) as inactive_licenses FROM provider_roster GROUP BY practice_state;

- Question: "List all cardiologists in New York"
- SQL: SELECT full_name, practice_address_line1 FROM provider_roster WHERE primary_specialty = 'Cardiology' AND practice_state = 'NY';

### USER QUESTION
Question: "{question}"
[/INST]
SQL:
"""
    
    # --- Generate the Query using Ollama ---
    try:
        print(f"🤖 Sending prompt to Ollama using codellama:13b-instruct for: '{question}'")
        
        response = ollama.generate(
            model='codellama:13b-instruct', 
            prompt=prompt,
            stream=False,
            options={
                'stop': ['###', ';', '[/SQL]']
            }
        )
        
        generated_sql = response['response'].strip()
        
        if not generated_sql.endswith(';'):
            generated_sql += ';'
            
        print(f"✅ Generated SQL: {generated_sql}")
        return generated_sql

    except Exception as e:
        print(f"❌ Error during Ollama generation: {e}")
        return f"SELECT 'Error during SQL generation from Ollama: {e}' as error;"