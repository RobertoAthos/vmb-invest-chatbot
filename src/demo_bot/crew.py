from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from demo_bot.tools.custom_tool import MyJSONSearchTool

@CrewBase
class DemoBot():
    """VMB Invest DemoBot crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()

    @agent
    def agente_principal(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_principal'],
            verbose=True,
        )

    @agent
    def agente_atendimento(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_atendimento'],
            verbose=True,
        )

    @agent
    def agente_qa(self) -> Agent:
        json_file_path = os.path.join(os.path.dirname(__file__), "qa_data.json")
        json_config = {
            "embedding_model": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small",
                },
            },
            "persist_directory": "/tmp/chroma",  # use diretório temporário
            "chroma_db_impl": "duckdb",  # <- FORÇA a não usar sqlite
        }

        return Agent(
            config=self.agents_config['agente_qa'],
            tools=[MyJSONSearchTool(json_path=json_file_path, config=json_config)],
            verbose=True,
        )
    
    @task
    def agente_principal_task(self) -> Task:
        return Task(
            config=self.tasks_config['agente_principal_task'],
        )

    @task
    def agente_atendimento_task(self) -> Task:
        return Task(
            config=self.tasks_config['agente_atendimento_task'],
        )

    @task
    def agente_qa_task(self) -> Task:
        return Task(
            config=self.tasks_config['agente_qa_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
