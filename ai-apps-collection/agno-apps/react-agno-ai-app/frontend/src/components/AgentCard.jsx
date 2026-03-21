export function AgentCard({ agent, isActive, onClick }) {
  return (
    <div
      className={`agent-card ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      <div className="agent-card-icon">{agent.icon || '🤖'}</div>
      <div className="agent-card-info">
        <h3>{agent.name}</h3>
        <p>{agent.description}</p>
      </div>
    </div>
  );
}
