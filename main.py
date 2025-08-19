from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import chainlit as cl
import httpx, os
from dotenv import load_dotenv

load_dotenv()

with open('system_prompt03.txt', 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read().strip()

model = OpenAIModel(
    'anthropic/claude-sonnet-4',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv("OPENROUTER_API_KEY"),
        http_client=httpx.AsyncClient(verify=False)
    ),
)

simple_agent = Agent(
    model=model,
    system_prompt = SYSTEM_PROMPT
)

@cl.on_chat_start
def on_start():
    cl.user_session.set("agent", simple_agent)
  
@cl.on_message # decorator
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.run_sync(message.content)
    await cl.Message(content=response.output).send()