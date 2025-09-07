import ollama
from datetime import datetime

# --- Check if Ollama is running ---
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

    # --- PROMPT FOR 7B MODEL ---
    prompt = f"""You are a SQL expert. Return ONLY the SQL query, no explanations, understand the schema properly, understand which column might represent which one, here is the schema, if you think that the response can't be fulfilled then reply that we can't fulfill that response:

Schema: {schema}

Key columns:
- is_license_active = 0 means expired license
- is_license_found = 0 means license not found  
- is_npi_found = 0 means NPI not found

Examples:
Q: "How many providers have expired licenses?"
A: SELECT COUNT(*) FROM provider_roster WHERE is_license_active = 0;

Q: "Show providers with NPI issues"  
A: SELECT full_name, primary_specialty FROM provider_roster WHERE is_npi_found = 0;

Q: "What is the overall data quality score?"
A: SELECT AVG((is_license_found + is_license_active + is_npi_found) / 3.0) * 100 FROM provider_roster;


Question: "{question}"
SQL:"""
    
    # --- Generating the Query using Ollama ---
    try:
        print(f"🤖 Sending prompt to Ollama using qwen2.5-coder:7b for: '{question}'")
        
        response = ollama.generate(
            model='qwen2.5-coder:7b', 
            prompt=prompt,
            stream=False,
            options={
                'stop': ['\n\n', 'Question:', 'Q:', 'A:', 'SQL:']
            }
        )
        
        generated_sql = response['response'].strip()
        
        if generated_sql.startswith('```sql'):
            generated_sql = generated_sql.replace('```sql', '').strip()
        if generated_sql.startswith('```'):
            generated_sql = generated_sql.replace('```', '').strip()
        if generated_sql.endswith('```'):
            generated_sql = generated_sql.replace('```', '').strip()
        
        generated_sql = generated_sql.replace('```sql', '').replace('```', '').strip()
        
        # Extract SQL from explanatory text if present
        if 'SELECT' in generated_sql:
            select_start = generated_sql.find('SELECT')
            if select_start != -1:
                generated_sql = generated_sql[select_start:].strip()
                if ';' in generated_sql:
                    generated_sql = generated_sql[:generated_sql.find(';') + 1]
        
        if not generated_sql.startswith('SELECT'):
            generated_sql = "SELECT 'No valid SQL generated' as error;"
        
        if not generated_sql.endswith(';'):
            generated_sql += ';'
            
        print(f"✅ Generated SQL: {generated_sql}")
        return generated_sql

    except Exception as e:
        print(f"❌ Error during Ollama generation: {e}")
        return f"SELECT 'Error during SQL generation from Ollama: {e}' as error;"