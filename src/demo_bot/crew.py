from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import JSONSearchTool
import os

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
        return Agent(
            config=self.agents_config['agente_qa'],
            tools=[JSONSearchTool(json_path=json_file_path)],
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
