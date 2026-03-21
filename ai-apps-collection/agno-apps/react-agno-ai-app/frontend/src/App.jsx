import { useState, useEffect } from 'react';
import './App.css';
import { Sidebar } from './components/Sidebar';
import { ChatWindow } from './components/ChatWindow';

function App() {
  const [agents, setAgents] = useState([]);
  const [activeAgent, setActiveAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/agents');
        const data = await res.json();
        setAgents(data.agents);
        if (data.agents.length > 0) {
          setActiveAgent(data.agents[0]);
        }
        setIsConnected(true);
      } catch (err) {
        console.error('Failed to load agents:', err);
        setIsConnected(false);
        // Set a default agent even if backend is down
        setAgents([{ name: 'Assistant', description: 'General AI assistant', icon: '🤖' }]);
        setActiveAgent({ name: 'Assistant', description: 'General AI assistant', icon: '🤖' });
      }
    };
    fetchAgents();
  }, []);

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="app-container">
      <Sidebar
        agents={agents}
        activeAgent={activeAgent}
        onAgentSelect={setActiveAgent}
        onNewChat={handleNewChat}
        isConnected={isConnected}
      />
      <main className="main-content">
        <ChatWindow
          activeAgent={activeAgent}
          messages={messages}
          setMessages={setMessages}
        />
      </main>
    </div>
  );
}

export default App;