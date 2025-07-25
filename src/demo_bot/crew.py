from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import JSONSearchTool
from typing import List
import os

@CrewBase
class DemoBot():
    """VMB Invest DemoBot crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self):
        super().__init__()

    @agent
    def agente_recepcionista(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_recepcionista'],
            verbose=True,
        )

    @agent
    def agente_orquestrador(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_orquestrador'],
            verbose=True,
            allow_delegation=True,
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
        }

        return Agent(
            config=self.agents_config['agente_qa'],
            tools=[JSONSearchTool(json_path=json_file_path, config=json_config)],
            verbose=True,
        )
    
    @task
    def agente_orquestrador_task(self) -> Task:
        return Task(
            config=self.tasks_config['agente_orquestrador_task'],
        )

    @task
    def agente_recepcionista_task(self) -> Task:
        return Task(
            config=self.tasks_config['agente_recepcionista_task'],
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
        # In hierarchical process, manager agent is separate from the working agents
        working_agents = [
            self.agente_recepcionista(),
            self.agente_atendimento(), 
            self.agente_qa()
        ]
        return Crew(
            agents=working_agents,
            tasks=[self.agente_orquestrador_task()],  # Manager's task
            manager_agent=self.agente_orquestrador(),  # Manager is separate
            manager_llm="gpt-4o",
            process=Process.hierarchical,
            verbose=True,
        )
