import os
from google.adk.agents import LlmAgent
from typing import List

from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent


print("AGENT_CARD_WELL_KNOWN_PATH:", AGENT_CARD_WELL_KNOWN_PATH)    # /.well-known/agent-card.json

# Agents
illustration_agent = RemoteA2aAgent(
    name="illustration_agent",
    description="Agent that generates illustrations.",
    #agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
    #agent_card=f"https://illustration-agent-485230244166.us-central1.run.app/a2a/illustration_agent{AGENT_CARD_WELL_KNOWN_PATH}",
    agent_card="https://illustration-agent-485230244166.us-central1.run.app/a2a/illustration_agent/.well-known/agent-card.json",
)

root_agent = LlmAgent(
    model=os.getenv("MODEL"),
    name='ad_content_agent',
    description='An agent that writes content for advertisement.',
    instruction="""
        A user will ask you to create content for an ad to communicate an idea.
        Write a short headline about this idea.
        Write 1-2 sentences of body text about this idea.
        Share these with the user.
        Then transfer to the 'illustration_agent' to generate an illustration related to this idea.
        """,
    sub_agents=[illustration_agent]
)


# For debugging - print confirmation when module loads
print(f"\n🎼 🎶 🎵 Music class ad generation - Ad Content agent")
print(f"\tName: {root_agent.name}")
print(f"\tModel: {root_agent.model}")
print(f"\tInstructions length: {len(root_agent.instruction)} characters")
