"""
Test script to verify dashboard SQL queries work correctly
"""
import requests
import json

API_BASE_URL = 'http://127.0.0.1:5001'

def test_dashboard_queries():
    """Test all dashboard SQL queries"""
    
    dashboard_queries = [
        {
            'name': 'summary',
            'sql': '''SELECT 
                COUNT(*) AS total_providers,
                SUM(CASE WHEN is_license_active = 0 THEN 1 ELSE 0 END) AS expired_licenses,
                SUM(CASE WHEN is_npi_found = 0 THEN 1 ELSE 0 END) AS npi_issues,
                AVG((is_license_found + is_license_active + is_npi_found) / 3.0) * 100 AS overall_quality_score
            FROM provider_roster'''
        },
        {
            'name': 'duplicates',
            'sql': '''SELECT 
                COUNT(*) AS potential_duplicates,
                COUNT(DISTINCT full_name) AS unique_names,
                COUNT(*) - COUNT(DISTINCT full_name) AS name_variations
            FROM provider_roster'''
        },
        {
            'name': 'license_validation',
            'sql': '''SELECT 
                SUM(CASE WHEN is_license_found = 1 AND is_license_active = 1 THEN 1 ELSE 0 END) AS valid_licenses,
                SUM(CASE WHEN is_license_found = 1 AND is_license_active = 0 THEN 1 ELSE 0 END) AS expired_licenses,
                SUM(CASE WHEN is_license_found = 0 THEN 1 ELSE 0 END) AS invalid_licenses,
                SUM(CASE WHEN license_number IS NULL OR license_number = '' THEN 1 ELSE 0 END) AS missing_license_numbers
            FROM provider_roster'''
        }
    ]
    
    print("🧪 Testing Dashboard SQL Queries...")
    print("=" * 50)
    
    for query in dashboard_queries:
        try:
            print(f"\n📊 Testing {query['name']} query...")
            response = requests.post(f"{API_BASE_URL}/execute_sql", 
                                   json={'sql': query['sql']},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                if results:
                    print(f"✅ {query['name']}: {len(results)} results")
                    print(f"   Sample data: {results[0]}")
                else:
                    print(f"⚠️  {query['name']}: No results returned")
            else:
                print(f"❌ {query['name']}: HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {query['name']}: Connection error - {e}")
        except Exception as e:
            print(f"❌ {query['name']}: Unexpected error - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Dashboard query testing complete!")

if __name__ == "__main__":
    test_dashboard_queries()
