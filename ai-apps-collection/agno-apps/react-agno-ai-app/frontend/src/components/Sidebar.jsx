import { AgentCard } from './AgentCard';

export function Sidebar({ agents, activeAgent, onAgentSelect, onNewChat, isConnected }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">⚡</div>
          <h1>Agno AI</h1>
        </div>
        <div className="sidebar-brand-sub">Powered by Claude Sonnet 4.6</div>
      </div>

      <div className="sidebar-actions">
        <button className="new-chat-btn" onClick={onNewChat}>
          <span>＋</span> New Chat
        </button>
      </div>

      <div className="sidebar-section-title">Agents</div>

      <div className="agent-list">
        {agents.map((agent) => (
          <AgentCard
            key={agent.name}
            agent={agent}
            isActive={activeAgent?.name === agent.name}
            onClick={() => onAgentSelect(agent)}
          />
        ))}
      </div>

      <div className="sidebar-footer">
        <div className="status-indicator">
          <div className={`status-dot ${isConnected ? '' : 'offline'}`} />
          <span>{isConnected ? 'Backend connected' : 'Backend offline'}</span>
        </div>
      </div>
    </div>
  );
}
