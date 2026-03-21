import os
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.skills import Skills, LocalSkills
from agno.tools.tavily import TavilyTools

load_dotenv()

# Initialize model
model = OpenRouter(id="anthropic/claude-sonnet-4.6")

# Load skills from directory (using absolute path for reliability)
skills_dir = Path(__file__).parent / "skills"
skills = Skills(loaders=[LocalSkills(str(skills_dir))])

# Create agent with skills + tools
agent = Agent(
    name="Assistant",
    model=model,
    skills=skills,
    tools=[TavilyTools()],
    instructions=[
        "You are a helpful AI assistant powered by Claude Sonnet 4.6.",
        "You have access to specialized skills — use get_skill_instructions to load guidance when relevant.",
        "You can search the web using Tavily when the user needs current information.",
        "Format your responses with markdown for readability.",
        "Be helpful, concise, and accurate."
    ],
    markdown=True
)