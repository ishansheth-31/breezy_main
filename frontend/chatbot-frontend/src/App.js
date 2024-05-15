import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Function to start the chat
  const startChat = async () => {
    try {
      const response = await axios.post('http://localhost:5000/start');
      console.log('Response:', response.data);  // Log the response data to see what is being returned
      setMessages([{ role: 'bot', content: response.data.response }]);
    } catch (error) {
      console.error('Error starting the chat:', error);
    }
};


  // Function to send a message
  const sendMessage = async () => {
    if(input.trim()) {
      const newMessages = messages.concat({ role: 'user', content: input });
      setMessages(newMessages);
      setInput('');

      try {
        const response = await axios.post('http://localhost:5000/chat', { message: input });
        setMessages(newMessages.concat({ role: 'bot', content: response.data.response }));
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  // Function to get the report
  const getReport = async () => {
    try {
      const response = await axios.get('http://localhost:5000/report');
      if(response.data.report_path) {
        alert(`Report saved at: ${response.data.report_path}`);
      } else {
        alert('No report available yet.');
      }
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  return (
    <div className="App">
      <h1>Chatbot Interface</h1>
      <button onClick={startChat}>Start Chat</button>
      <div>
        {messages.map((msg, index) => (
          <p key={index} className={msg.role}>{msg.role === 'bot' ? 'Virtual Nurse: ' : 'You: '}{msg.content}</p>
        ))}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && sendMessage()} />
      <button onClick={sendMessage}>Send</button>
      <button onClick={getReport}>Get Report</button>
    </div>
  );
}

export default App;
