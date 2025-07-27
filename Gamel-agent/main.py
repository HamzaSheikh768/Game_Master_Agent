import os

from agents import (
    Agent,
    Runner,
    AsyncOpenAI, # pyright: ignore[reportPrivateImportUsage]
    OpenAIChatCompletionsModel
)
from agents.run import RunConfig
from dotenv import load_dotenv
from game_tools import roll_dice, generate_event

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client, # type: ignore
    tracing_disabled = True
)

# Narrator Agent
narrator_agent = Agent(
    name="NarratorAgent",
    instructions="You narrate the advanture. Ask the player for choices.",
    model=model
)

# Monster Agent
monster_agent = Agent(
    name="MonsterAgent",
    instructions="You handle monster enconter using roll_dice and generate_events.",
    model=model
)

# Item Agent
item_agent = Agent(
    name="ItemAgent",
    instructions="You provide rewards or items to the player.",
    model=model
)

def main():
    print("\U0001F3AE Welcome to Fantasy Adventure Game!")
    choice = input("Do you enter the forest or turn back?")

    result1 = Runner.run_sync(narrator_agent, choice,run_config=config)
    print("\n Story:", result1.final_output)

    result2 = Runner.run_sync(monster_agent, "Start encounter", run_config=config)
    print("\n Encounter:", result2.final_output)

    result3 = Runner.run_sync(item_agent, "Give Reward", run_config=config)
    print("\n Reward:", result3.final_output)

    
if __name__ == "__main__":
    main()
