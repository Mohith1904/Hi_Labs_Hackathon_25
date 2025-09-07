import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MessageCircle, Database, BarChart3, Users, AlertTriangle, CheckCircle, LayoutDashboard, Bot } from 'lucide-react';
import DataVisualization from './components/DataVisualization';
import Dashboard from './components/Dashboard';
import './App.css';

const API_BASE_URL = 'http://127.0.0.1:5001';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [stats, setStats] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard'); // 'dashboard' or 'chatbot'

  // Sample questions for quick access
  const sampleQuestions = [
    "How many providers have expired licenses?",
    "What is the overall data quality score?",
    "Show me providers with NPI issues",
    "Which specialty has the lowest quality score?",
    "How many duplicate records were found?",
    "Show me all providers from California"
  ];

  useEffect(() => {
    // Load initial stats
    loadInitialStats();
  }, []);

  const loadInitialStats = async () => {
    try {
      // This would be a new endpoint to get summary stats
      // For now, we'll use a sample query
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question: "Show me summary statistics"
      });
      
      if (response.data.results && response.data.results.length > 0) {
        setStats(response.data.results[0]);
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question: inputMessage
      });

      const assistantMessage = {
        type: 'assistant',
        content: `Found ${response.data.results.length} results`,
        sqlQuery: response.data.sql_query,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setResults({
        sqlQuery: response.data.sql_query,
        data: response.data.results
      });

    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: error.response?.data?.error || 'Failed to process your request',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const askSampleQuestion = (question) => {
    setInputMessage(question);
    setCurrentView('chatbot'); // Switch to chatbot view when asking a question
  };

  const handleAskQuestion = (question) => {
    setInputMessage(question);
    setCurrentView('chatbot');
    // Automatically send the question
    setTimeout(() => {
      sendMessage();
    }, 100);
  };

  const safeStringify = (value) => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string') return value;
    if (typeof value === 'number') return value.toString();
    if (typeof value === 'boolean') return value.toString();
    if (typeof value === 'object') return JSON.stringify(value);
    return String(value);
  };

  const renderResults = () => {
    if (!results) return null;

    return (
      <div className="results-container">
        <div className="results-header">
          <Database className="icon" size={24} />
          <h2>Query Results</h2>
        </div>
        
        <div className="sql-query">
          <strong>SQL Query:</strong>
          <pre>{results.sqlQuery}</pre>
        </div>

        {results.data && results.data.length > 0 ? (
          <div className="table-container">
            <table className="results-table">
              <thead>
                <tr>
                  {Object.keys(results.data[0]).map((key, index) => (
                    <th key={index}>{key.replace(/_/g, ' ').toUpperCase()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.data.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, cellIndex) => (
                      <td key={cellIndex}>
                        {safeStringify(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-results">No results found</div>
        )}
      </div>
    );
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Provider Data Quality Analytics</h1>
        <p>Comprehensive analysis of provider data quality, license validation, and entity resolution</p>
        
        {/* Navigation Tabs */}
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            <LayoutDashboard size={20} />
            Dashboard
          </button>
          <button 
            className={`nav-tab ${currentView === 'chatbot' ? 'active' : ''}`}
            onClick={() => setCurrentView('chatbot')}
          >
            <Bot size={20} />
            Ask Questions
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="main-content">
        {currentView === 'dashboard' ? (
          <Dashboard onAskQuestion={handleAskQuestion} />
        ) : (
          <div className="chatbot-view">
            <div className="chatbot-layout">
              {/* Chat Interface */}
              <div className="card chat-card">
                <div className="chat-container">
                  <div className="chat-header">
                    <MessageCircle className="icon" size={24} />
                    <h2>Ask Questions</h2>
                  </div>

                <div className="messages">
                  {messages.map((message, index) => (
                    <div key={index} className={`message ${message.type}`}>
                      <div>{message.content}</div>
                      <div className="message-time">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="message assistant">
                      <div className="loading">
                        <div className="spinner"></div>
                        Processing your question...
                      </div>
                    </div>
                  )}
                </div>

                <div className="input-container">
                  <input
                    type="text"
                    className="input-field"
                    placeholder="Ask about provider data quality..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                  />
                  <button
                    className="send-button"
                    onClick={sendMessage}
                    disabled={isLoading || !inputMessage.trim()}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>

              {/* Results Display */}
              <div className="card results-card">
                {renderResults()}
                {results && results.data && results.data.length > 0 && (
                  <div style={{ marginTop: '20px' }}>
                    <DataVisualization 
                      data={results.data.slice(0, 10)} 
                      type="bar" 
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Sample Questions */}
            <div className="card">
              <h3 style={{ marginBottom: '20px', color: '#333' }}>Try These Questions:</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '10px' }}>
                {sampleQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => askSampleQuestion(question)}
                    style={{
                      padding: '12px 16px',
                      background: '#f8f9fa',
                      border: '1px solid #dee2e6',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s',
                      fontSize: '14px'
                    }}
                    onMouseOver={(e) => {
                      e.target.style.background = '#e9ecef';
                      e.target.style.borderColor = '#007bff';
                    }}
                    onMouseOut={(e) => {
                      e.target.style.background = '#f8f9fa';
                      e.target.style.borderColor = '#dee2e6';
                    }}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
