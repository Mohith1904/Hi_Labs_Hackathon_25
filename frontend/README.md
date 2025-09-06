# Provider Data Quality Analytics Frontend

A modern React-based frontend for the Provider Data Quality Analytics system.

## Features

- 🤖 **Interactive Chat Interface** - Ask questions about provider data quality
- 📊 **Real-time Results** - View SQL queries and data results instantly
- 📈 **Dashboard Overview** - Key metrics and statistics at a glance
- 💡 **Sample Questions** - Quick access to common queries
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Backend Flask server running on http://127.0.0.1:5001

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and go to http://localhost:3000

## Usage

1. **Ask Questions**: Type your questions about provider data quality in the chat interface
2. **View Results**: See the generated SQL queries and data results in real-time
3. **Try Sample Questions**: Click on the provided sample questions to get started quickly
4. **Monitor Stats**: View key metrics in the dashboard overview

## Sample Questions

- "How many providers have expired licenses?"
- "What is the overall data quality score?"
- "Show me providers with NPI issues"
- "Which specialty has the lowest quality score?"
- "How many duplicate records were found?"

## API Integration

The frontend communicates with the Flask backend API at `http://127.0.0.1:5001`. Make sure your backend server is running before using the frontend.

## Technologies Used

- React 18
- Axios for API calls
- Lucide React for icons
- CSS3 for styling
- Responsive design principles

## Development

To modify the frontend:

1. Edit files in the `src` directory
2. The app will automatically reload when you save changes
3. Check the browser console for any errors

## Building for Production

To create a production build:

```bash
npm run build
```

This will create an optimized build in the `build` directory.
