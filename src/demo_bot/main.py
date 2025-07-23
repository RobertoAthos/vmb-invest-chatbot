#!/usr/bin/env python
import warnings

from demo_bot.crew import DemoBot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    
    try:
        question = input("Insira a sua pergunta")
        result = DemoBot().crew().kickoff(inputs={"question": question})
        print("Resposta do DemoBot:", result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    while True:
        run()
