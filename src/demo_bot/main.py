#!/usr/bin/env python
import warnings
import os
from pathlib import Path
from dotenv import load_dotenv

from demo_bot.crew import DemoBot

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    
    try:
        question = input("Insira a sua pergunta")
        result = DemoBot().crew().kickoff(inputs={"question": question})
        print("Resposta do DemoBot:", result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
