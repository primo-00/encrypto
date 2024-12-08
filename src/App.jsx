import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [method, setMethod] = useState('caesar');
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [isTypingDone, setIsTypingDone] = useState(false);

  const handleRequest = async (decrypt) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/cipher', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method, text, decrypt }),
      });
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      setResult('Error communicating with the server!');
    }
  };

  useEffect(() => {
    // Typing animation timeout
    const timeout = setTimeout(() => setIsTypingDone(true), 4000); // Animation duration
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="app-container">
      {/* Logo Section with Falling Animation */}
      <div className="logo-container animate-fall">
        <img src="/logo-app.jpg" alt="App Logo" className="logo" />
      </div>

      {/* Typing Animation for Heading */}
      <h1 className={`heading ${isTypingDone ? '' : 'typing-animation'}`}>
        {!isTypingDone ? '' : 'Welcome to Encrypto'}
      </h1>

      {/* Cipher Form Section */}
      <div className="form-container">
        <label htmlFor="cipher-method">Choose Cipher Method:</label>
        <select
          id="cipher-method"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
        >
          <option value="caesar">Caesar Cipher</option>
          <option value="vigenere">Vigenère Cipher</option>
          <option value="affine">Affine Cipher</option>
          <option value="reverse">Reverse Cipher</option>
          <option value="railfence">Rail Fence Cipher</option>
        </select>
      </div>

      {/* Textarea for Input */}
      <textarea
        placeholder="Enter your message here"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="text-area"
      />

      {/* Buttons for Encrypt/Decrypt */}
      <div className="button-container">
        <button onClick={() => handleRequest(false)} className="btn">Encrypt</button>
        <button onClick={() => handleRequest(true)} className="btn">Decrypt</button>
      </div>

      {/* Result Display */}
      <div className="result-panel">

        <textarea
          value={result}
          onChange={(e) => setResult(e.target.value)}
          className="result-area"
          placeholder="Result will appear here..."
        />
      </div>
    </div>
  );
}

export default App;
