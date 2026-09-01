#!/bin/bash python3

### IMPORTS -------------------------------- ###

from src.logging.log_trace import log_trace
from src.models.llm import LLM
from src.models.embedder import Embedder
from src.skills_manager.skills_manager import SkillsManager

### CLASSES -------------------------------- ###

class ResumeEvaluator:

    """
    Class to evaluate a resume based against a job description.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing all necessary parameters
    text_generator: Callable
        LLM class instance for running prompts
    text_embedder: Callable
        Embedder class instance running similarity analysis
    """

    ### ------------------------------------ ###

    def __init__(self, config: dict, text_generator: LLM, text_embedder: Embedder, skills_dir: str) -> None:
        
        # Store LLM tools
        self.text_generator = text_generator
        self.text_embedder = text_embedder

        # Init skills manager
        self.skills_manager = SkillsManager(skills_dir)
        log_trace(trace_message='Added skills')

    ### ------------------------------------ ###
    ### PROCESS JOBS                         ###
    ### ------------------------------------ ###

    def compare_job_to_resume(self, resume: dict, job: dict) -> tuple[bool, str, dict]:

        """
        Compares job listings to the candidate's resume

        Parameters
        ----------
        resume: dict
            Dictionary of resume information
        job: Dict
            Dictionary of job information
        """
        
        # Init updated job dictionary
        updated_job = job.copy()
        log_trace(trace_message='Comparing resume to job')
        
        # Generate a summary of the job description
        skill_exec_status, skill_outputs, skill_execution_log = self.skills_manager.execute_skill(
            llm_call=self.text_generator.forward,
            skill_name='summarize-job-description',
            job_description=job['description']
        )
        if not skill_exec_status:
            #log_trace(trace_message=f'  \u2717 Failed to generate a job summary:\n'+'\n'.join(skill_execution_log))
            return False, f'  \u2717 Failed to generate a job summary:\n'+'\n'.join(skill_execution_log), {}
        job_summary = skill_outputs[-1]
        updated_job['generated_summary'] = job_summary
        log_trace(trace_message='  * Generated job summary')

        # Compare job summary to resume summary
        summary_score = self.embed_and_compare(
            query=[job_summary],
            reference=[resume['summary']]
        )
        updated_job['broad_score'] = round(summary_score, 3)
        log_trace(trace_message=f'  * Computed similarity score of job and resume summaries: {summary_score:.3f}')

        # Extract job requirements
        skill_exec_status, skill_outputs, skill_execution_log = self.skills_manager.execute_skill(
            llm_call=self.text_generator.forward,
            skill_name='extract-job-requirements',
            job_description=job['description']
        )
        if not skill_exec_status:
            #log_trace(trace_message=f'  \u2717 Failed to extract job requirements:\n'+'\n'.join(skill_execution_log))
            return False, f'  \u2717 Failed to extract job requirements:\n'+'\n'.join(skill_execution_log), {}
        job_requirements = [s for s in skill_outputs[-1].split('\n') if len(s)]
        updated_job['inferred_requirements'] = job_requirements
        log_trace(trace_message='  * Extracted job requirements')

        # Compare job requirements and resume skills
        skills_score = self.embed_and_compare(
            query=job_requirements,
            reference=[resume['skills']]
        )
        updated_job['skills_score'] = round(skills_score, 3)
        log_trace(trace_message=f"  * Computed similarity of job requirements and candidate's skills: {skills_score:.3f}")
        
        # Analyze how to improve the resume
        skill_exec_status, skill_outputs, skill_execution_log = self.skills_manager.execute_skill(
            llm_call=self.text_generator.forward,
            skill_name='evaluate-candidate',
            job_description=job['description'],
            candidate_description=resume['summary'],
            candidate_experience=resume['work_experience'],
            candidate_skills=resume['skills']
        )
        if not skill_exec_status:
            #log_trace(trace_message=f'  \u2717 Failed to generate resume improvements:\n'+'\n'.join(skill_execution_log))
            return False, f'  \u2717 Failed to generate resume improvements:\n'+'\n'.join(skill_execution_log), {}
        proposed_resume_improvements = skill_outputs[-1]
        updated_job['proposed_resume_improvements'] = proposed_resume_improvements
        log_trace(trace_message='  * Generated suggestions for resume improvements')
        
        log_trace(trace_message='  \u2714 Done')
        
        return True, '', updated_job
    
    ### ------------------------------------ ###

    def embed_and_compare(self, query: list[str], reference: list[str]) -> None:

        # Embed query and reference
        query_embeddings = self.text_embedder.transform(query)
        reference_embeddings = self.text_embedder.transform(reference)

        # Compare and return top 1 hit
        top_hits = self.text_embedder.compare(query_embeddings, reference_embeddings, 1, 0.)

        # Compute similarity average
        #scores = [max([s for t,s in ts]) if len(ts) else 0 for q,ts in top_hits.items()]
        scores = [max([s for t,s in ts]) for q,ts in top_hits.items() if len(ts)]
        average_score = float(sum(scores) / len(scores)) if len(scores) else 0

        return average_score
