import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [initialQuestions, setInitialQuestions] = useState({
    "What is your name?": "",
    "What is your approximate height?": "",
    "What is your approximate weight?": "",
    "Are you currently taking any medications?": "",
    "Have you had any recent surgeries?": "",
    "Do you have any known drug allergies?": "",
    "Finally, what are you in for today?": ""
  });
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [isConversationStarted, setIsConversationStarted] = useState(false);
  const [isConversationFinished, setIsConversationFinished] = useState(false);

  const handleInitialQuestionsChange = (e) => {
    setInitialQuestions({ ...initialQuestions, [e.target.name]: e.target.value });
  };

  const startConversation = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/start', initialQuestions, {
        headers: { 'Content-Type': 'application/json' }
      });
      setChatHistory([{ role: 'assistant', content: response.data.initial_response }]);
      setIsConversationStarted(true);
    } catch (error) {
      console.error('Error starting conversation:', error);
    }
  };

  const sendMessage = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', { message: userMessage }, {
        headers: { 'Content-Type': 'application/json' }
      });
      setChatHistory([...chatHistory, { role: 'user', content: userMessage }, { role: 'assistant', content: response.data.response }]);
      setUserMessage("");
      if (response.data.finished) {
        setIsConversationFinished(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const fetchReport = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/report');
      console.log('Report:', response.data);
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  return (
    <div className="App">
      <h1>Virtual Nurse Assistant Chatbot</h1>
      {!isConversationStarted ? (
        <div>
          <h2>Initial Questions</h2>
          {Object.keys(initialQuestions).map((question, index) => (
            <div key={index}>
              <label>{question}</label>
              <input
                type="text"
                name={question}
                value={initialQuestions[question]}
                onChange={handleInitialQuestionsChange}
              />
            </div>
          ))}
          <button onClick={startConversation}>Start Conversation</button>
        </div>
      ) : (
        <div>
          <div className="chat-history">
            {chatHistory.map((msg, index) => (
              <div key={index} className={msg.role}>
                <strong>{msg.role === 'user' ? 'You' : 'Virtual Nurse'}:</strong> {msg.content}
              </div>
            ))}
          </div>
          {!isConversationFinished && (
            <div className="message-input">
              <input
                type="text"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Type your message..."
              />
              <button onClick={sendMessage}>Send</button>
            </div>
          )}
          {isConversationFinished && (
            <div>
              <h2>Conversation Finished</h2>
              <button onClick={fetchReport}>Get Report</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
