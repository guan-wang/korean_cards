from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task
from models import Syllabus, LessonPlan, EvaluationResult

@CrewBase
class KoreanTutorCrew:
    """The Korean Tutor Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- AGENTS ---
    @agent
    def morphological_analyst(self) -> Agent:
        return Agent(config=self.agents_config['morphological_analyst'], verbose=True)

    @agent
    def contextual_linguist(self) -> Agent:
        return Agent(config=self.agents_config['contextual_linguist'], verbose=True)

    @agent
    def scenario_director(self) -> Agent:
        return Agent(config=self.agents_config['scenario_director'], verbose=True)

    @agent
    def evaluator_coach(self) -> Agent:
        return Agent(config=self.agents_config['evaluator_coach'], verbose=True)

    # --- TASKS ---
    @task
    def segmentation_task(self) -> Task:
        return Task(config=self.tasks_config['segmentation_task'], output_pydantic=Syllabus)

    @task
    def enrichment_task(self) -> Task:
        return Task(
            config=self.tasks_config['enrichment_task'],
            context=[self.segmentation_task()],
            output_pydantic=Syllabus
        )

    @task
    def scenario_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['scenario_generation_task'],
            # This task now consumes the enrichment output and produces the Master Plan
            context=[self.enrichment_task()], 
            output_pydantic=LessonPlan 
        )

    @task
    def evaluation_task(self) -> Task:
        return Task(config=self.tasks_config['evaluation_task'], output_pydantic=EvaluationResult)

    # --- WORKFLOWS ---

    # 1. The Unified "Lesson Creator" Flow
    def run_tutor(self, korean_text: str):
        return Crew(
            agents=[self.morphological_analyst(), self.contextual_linguist(), self.scenario_director()],
            tasks=[self.segmentation_task(), self.enrichment_task(), self.scenario_generation_task()],
            process=Process.sequential,
            verbose=True
        ).kickoff(inputs={'korean_text': korean_text})

        # 2. The Interactive Evaluation Flow
    def run_evaluation(self, scenario_obj, user_input_str):
        return Crew(
            agents=[self.evaluator_coach()],
            tasks=[self.evaluation_task()],
            verbose=True
        ).kickoff(inputs={
            'scenario_description': scenario_obj.scenario_description,
            'user_role': scenario_obj.user_role,
            'required_tone': scenario_obj.required_tone,
            'user_input': user_input_str,
            'target_items': ", ".join(scenario_obj.target_items)
        })