# Provider Data Quality Analytics - Complete Setup Guide

This guide will help you set up both the backend and frontend for the Provider Data Quality Analytics system.

## 🏗️ System Architecture

- **Backend**: Flask API with SQLite database
- **Frontend**: React web application (or simple HTML version)
- **Data Processing**: Pandas for data manipulation and fuzzy matching
- **Text-to-SQL**: AI-powered query generation

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for React frontend)
- Git (optional)

## 🚀 Quick Start

### Option 1: React Frontend (Recommended)

1. **Start the Backend**:
   ```bash
   # Install Python dependencies
   pip install pandas fastapi uvicorn phonenumbers fuzzywuzzy python-levenshtein vanna

   # Run the Flask backend
   python app.py
   ```

2. **Start the React Frontend**:
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install dependencies
   npm install

   # Start the development server
   npm start
   ```

3. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:5001

### Option 2: Simple HTML Frontend

1. **Start the Backend** (same as above)

2. **Open the HTML File**:
   - Simply open `frontend/simple/index.html` in your web browser
   - No additional setup required!

## 📁 Project Structure

```
hi-labs-hackathon/
├── data/                           # CSV data files
│   ├── provider_roster_with_errors.csv
│   ├── mock_npi_registry.csv
│   ├── ca_medical_license_database.csv
│   └── ny_medical_license_database.csv
├── frontend/                       # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── frontend/simple/                # Simple HTML frontend
│   └── index.html
├── app.py                         # Main Flask application
├── database_setup.py              # Database setup and validation
├── query_generator.py             # AI query generation
├── requirements.txt               # Python dependencies
└── SETUP_GUIDE.md                # This file
```

## 🔧 Backend Setup Details

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Data Processing Pipeline

The backend performs the following steps:

1. **Data Loading**: Loads CSV files from the `data/` directory
2. **Fuzzy Matching Validation**: 
   - Matches provider names against license databases
   - Validates NPI numbers against registry
   - Checks for expired licenses
3. **Database Creation**: Creates in-memory SQLite database
4. **API Server**: Starts Flask server on port 5001

### 3. API Endpoints

- `GET /` - Health check
- `POST /chat` - Process natural language queries

## 🎨 Frontend Setup Details

### React Frontend Features

- **Interactive Chat Interface**: Real-time conversation with the AI
- **Results Display**: Shows SQL queries and data in tables
- **Dashboard Overview**: Key metrics and statistics
- **Sample Questions**: Quick access to common queries
- **Responsive Design**: Works on desktop and mobile

### Simple HTML Frontend Features

- **No Build Process**: Just open the HTML file
- **Same Functionality**: All features of React version
- **Lightweight**: No dependencies to install

## 🔍 How It Works

### 1. Data Quality Validation

The system performs fuzzy matching to validate provider data:

```python
# Example validation process
def validate_provider(roster_row, license_map, npi_map):
    # Fuzzy match provider name against license database
    best_match = process.extractOne(roster_name, license_map.keys(), score_cutoff=85)
    
    # Check if license numbers match
    if roster_row['license_number'] == matched_license_data['license_number']:
        is_license_found = 1
        
    # Similar process for NPI validation
```

### 2. AI Query Generation

The system uses AI to convert natural language to SQL:

```python
# Example query generation
question = "How many providers have expired licenses?"
sql = generate_sql_query(question, db_schema)
# Returns: "SELECT COUNT(*) FROM provider_roster WHERE is_license_active = 0"
```

### 3. Real-time Results

- User asks question in natural language
- AI generates SQL query
- Query executes against database
- Results displayed in interactive table

## 📊 Sample Questions

Try these questions to test the system:

1. **Data Quality Questions**:
   - "How many providers have expired licenses?"
   - "What is the overall data quality score?"
   - "Show me providers with NPI issues"

2. **Analytics Questions**:
   - "Which specialty has the lowest quality score?"
   - "How many duplicate records were found?"
   - "Show me all providers from California"

3. **Specific Provider Queries**:
   - "Find providers with missing license information"
   - "Show me inactive licenses"
   - "List providers with name mismatches"

## 🐛 Troubleshooting

### Backend Issues

1. **Port Already in Use**:
   ```bash
   # Kill process using port 5001
   netstat -ano | findstr :5001
   taskkill /PID <PID> /F
   ```

2. **Missing Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Data Files Not Found**:
   - Ensure CSV files are in the `data/` directory
   - Check file names match exactly

### Frontend Issues

1. **React App Won't Start**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm start
   ```

2. **API Connection Failed**:
   - Ensure backend is running on port 5001
   - Check CORS settings in Flask app
   - Verify API_BASE_URL in frontend code

3. **Simple HTML Not Working**:
   - Open browser developer tools
   - Check for CORS errors
   - Ensure backend is running

## 🚀 Production Deployment

### Backend Deployment

1. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

2. **Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=your_database_url
   ```

### Frontend Deployment

1. **Build React App**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve Static Files**:
   - Use nginx, Apache, or any static file server
   - Point to the `build/` directory

## 📈 Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried columns
2. **Caching**: Implement Redis for query result caching
3. **Async Processing**: Use Celery for long-running tasks
4. **CDN**: Use CDN for static frontend assets

## 🔒 Security Considerations

1. **API Rate Limiting**: Implement rate limiting for API endpoints
2. **Input Validation**: Sanitize user inputs
3. **CORS Configuration**: Restrict CORS to specific domains
4. **Authentication**: Add user authentication if needed

## 📝 Customization

### Adding New Data Sources

1. Update `database_setup.py` to load new CSV files
2. Modify validation logic in `validate_provider()`
3. Update database schema and API responses

### Customizing the Frontend

1. **React Version**: Modify components in `frontend/src/`
2. **HTML Version**: Edit `frontend/simple/index.html`
3. **Styling**: Update CSS files for custom themes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the console logs for errors
3. Ensure all dependencies are installed correctly
4. Verify the backend is running and accessible

## 🎯 Next Steps

1. **Add More Data Sources**: Integrate additional provider databases
2. **Enhanced AI**: Implement more sophisticated query generation
3. **Data Visualization**: Add charts and graphs for better insights
4. **User Management**: Add authentication and user roles
5. **API Documentation**: Create comprehensive API documentation
