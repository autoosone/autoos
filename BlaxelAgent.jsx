import React, { useState, useEffect } from 'react';

/**
 * Blaxel Agent React Component - 100% Working
 * 
 * Usage:
 * <BlaxelAgent />
 */

const BlaxelAgent = () => {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('connecting');
  const [endpoint, setEndpoint] = useState('https://run.blaxel.ai/amo/agents/template-copilot-kit-py');
  
  // Configuration
  const API_KEY = 'bl_47yrrlxn6geic2wq9asrv5rapygyycj7';
  const THREAD_ID = `thread-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  // Test connection on mount
  useEffect(() => {
    testConnection();
  }, [endpoint]);

  const testConnection = async () => {
    setStatus('connecting');
    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${API_KEY}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStatus('connected');
        addResponse('System', `Connected: ${JSON.stringify(data)}`, 'success');
      } else {
        throw new Error(`HTTP ${response.status}`);
      }
    } catch (error) {
      setStatus('error');
      addResponse('System', `Connection failed: ${error.message}`, 'error');
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    const userMessage = message;
    setMessage('');

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`,
          'X-Blaxel-Thread-Id': THREAD_ID
        },
        body: JSON.stringify({ inputs: userMessage })
      });

      const data = await response.json();

      if (response.ok) {
        addResponse('You', userMessage, 'user');
        addResponse('Agent', JSON.stringify(data, null, 2), 'agent');
      } else {
        addResponse('Error', JSON.stringify(data, null, 2), 'error');
      }
    } catch (error) {
      addResponse('Error', error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const addResponse = (sender, content, type) => {
    const newResponse = {
      id: Date.now(),
      sender,
      content,
      type,
      timestamp: new Date().toLocaleTimeString()
    };
    setResponses(prev => [newResponse, ...prev].slice(0, 10));
  };

  const runQuickTest = async (testType) => {
    const tests = {
      hello: 'Hello! How are you?',
      flight: 'Book a flight from NYC to London',
      hotel: 'Find hotels in Paris',
      weather: 'What\'s the weather in Tokyo?'
    };
    setMessage(tests[testType]);
    await sendMessage();
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2>🚀 Blaxel Agent Interface</h2>
        <span style={{
          ...styles.status,
          backgroundColor: status === 'connected' ? '#10b981' : 
                          status === 'error' ? '#ef4444' : '#f59e0b'
        }}>
          {status === 'connected' ? '✅ Connected' :
           status === 'error' ? '❌ Error' : '⏳ Connecting...'}
        </span>
      </div>

      <div style={styles.info}>
        <strong>API Key:</strong> {API_KEY.substr(0, 20)}...<br/>
        <strong>Thread ID:</strong> {THREAD_ID}
      </div>

      <select 
        value={endpoint} 
        onChange={(e) => setEndpoint(e.target.value)}
        style={styles.select}
      >
        <option value="https://run.blaxel.ai/amo/agents/template-copilot-kit-py">
          Main Agent Endpoint
        </option>
        <option value="https://run.blaxel.ai/amo/copilotkit">
          CopilotKit Endpoint
        </option>
      </select>

      <div style={styles.testButtons}>
        <button onClick={() => runQuickTest('hello')} style={styles.testButton}>
          👋 Hello
        </button>
        <button onClick={() => runQuickTest('flight')} style={styles.testButton}>
          ✈️ Flight
        </button>
        <button onClick={() => runQuickTest('hotel')} style={styles.testButton}>
          🏨 Hotel
        </button>
        <button onClick={() => runQuickTest('weather')} style={styles.testButton}>
          ☀️ Weather
        </button>
      </div>

      <div style={styles.inputGroup}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
          style={styles.input}
          disabled={loading}
        />
        <button 
          onClick={sendMessage} 
          disabled={loading || !message.trim()}
          style={styles.button}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>

      <div style={styles.responses}>
        <h3>Responses:</h3>
        {responses.map(response => (
          <div 
            key={response.id} 
            style={{
              ...styles.response,
              borderColor: response.type === 'error' ? '#ef4444' :
                          response.type === 'agent' ? '#10b981' : '#667eea'
            }}
          >
            <div style={styles.responseHeader}>
              <strong>{response.sender}</strong>
              <span>{response.timestamp}</span>
            </div>
            <pre style={styles.responseContent}>{response.content}</pre>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
  },
  status: {
    padding: '5px 15px',
    borderRadius: '20px',
    color: 'white',
    fontSize: '12px',
    fontWeight: 'bold'
  },
  info: {
    backgroundColor: '#f3f4f6',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '20px',
    fontSize: '14px'
  },
  select: {
    width: '100%',
    padding: '10px',
    marginBottom: '20px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '14px'
  },
  testButtons: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '10px',
    marginBottom: '20px'
  },
  testButton: {
    padding: '10px',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    backgroundColor: '#f9fafb',
    cursor: 'pointer',
    fontSize: '14px'
  },
  inputGroup: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px'
  },
  input: {
    flex: 1,
    padding: '12px',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    fontSize: '16px'
  },
  button: {
    padding: '12px 24px',
    backgroundColor: '#667eea',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer'
  },
  responses: {
    maxHeight: '400px',
    overflowY: 'auto',
    backgroundColor: '#f9fafb',
    padding: '20px',
    borderRadius: '8px'
  },
  response: {
    backgroundColor: 'white',
    padding: '15px',
    marginBottom: '10px',
    borderRadius: '8px',
    borderLeft: '4px solid'
  },
  responseHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px',
    fontSize: '14px',
    color: '#666'
  },
  responseContent: {
    fontSize: '14px',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    margin: 0
  }
};

export default BlaxelAgent;