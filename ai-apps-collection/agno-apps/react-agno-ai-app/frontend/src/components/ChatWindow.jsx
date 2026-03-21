import { useState, useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';

const SUGGESTIONS = [
  { icon: '💻', title: 'Write Code', text: 'Generate a Python script', prompt: 'Write a Python script that reads a CSV file and calculates summary statistics' },
  { icon: '🔍', title: 'Web Search', text: 'Find latest information', prompt: 'Search the web for the latest AI developments this week' },
  { icon: '📝', title: 'Explain Concepts', text: 'Break down complex topics', prompt: 'Explain how transformer neural networks work in simple terms' },
  { icon: '🚀', title: 'Debug Help', text: 'Fix code issues fast', prompt: 'Help me debug a React useEffect infinite loop issue' },
];

export function ChatWindow({ activeAgent, messages, setMessages }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEnd = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => scrollToBottom(), [messages]);
  useEffect(() => inputRef.current?.focus(), []);

  const sendMessage = async (overrideMsg) => {
    const msg = overrideMsg || input;
    if (!msg.trim() || loading) return;

    const userMsg = { role: 'user', content: msg, time: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: msg,
          agent_name: activeAgent?.name || 'Assistant'
        })
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = '';
      const assistantMsg = { role: 'assistant', content: '', time: new Date() };
      setMessages(prev => [...prev, assistantMsg]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n').filter(l => l.startsWith('data: '));

        for (const line of lines) {
          const data = line.slice(6).trim();
          if (data === '[DONE]') break;
          try {
            const parsed = JSON.parse(data);
            if (parsed.error) throw new Error(parsed.error);
            assistantContent += parsed.content;
            setMessages(prev => [
              ...prev.slice(0, -1),
              { ...assistantMsg, content: assistantContent }
            ]);
          } catch (e) {
            if (e.message && !e.message.includes('JSON')) {
              throw e;
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { role: 'error', content: `Connection failed: ${err.message}`, time: new Date() }
      ]);
    }
    setLoading(false);
    inputRef.current?.focus();
  };

  const handleSuggestion = (prompt) => {
    sendMessage(prompt);
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-header-title">
          <h2>{activeAgent?.icon || '🤖'} {activeAgent?.name || 'Assistant'}</h2>
          <span className="chat-header-badge">Claude Sonnet 4.6</span>
        </div>
      </div>

      <div className="messages">
        {messages.length === 0 ? (
          <div className="welcome-container">
            <div className="welcome-icon">⚡</div>
            <h1>How can I help you?</h1>
            <p>I'm powered by Claude Sonnet 4.6 with Agno Skills. Ask me anything or try a suggestion below.</p>
            <div className="welcome-cards">
              {SUGGESTIONS.map((s, i) => (
                <div key={i} className="welcome-card" onClick={() => handleSuggestion(s.prompt)}>
                  <div className="welcome-card-icon">{s.icon}</div>
                  <h3>{s.title}</h3>
                  <p>{s.text}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <MessageBubble key={i} message={msg} />
            ))}
            {loading && messages[messages.length - 1]?.role !== 'assistant' && (
              <div className="typing-indicator">
                <div className="message-avatar">🤖</div>
                <div className="typing-dots">
                  <span /><span /><span />
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEnd} />
      </div>

      <div className="input-bar">
        <input
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder={`Message ${activeAgent?.name || 'Assistant'}...`}
          disabled={loading}
        />
        <button className="send-btn" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          {loading ? '⏳' : '↑'}
        </button>
      </div>
    </div>
  );
}
