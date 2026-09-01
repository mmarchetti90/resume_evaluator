#!/usr/bin/env python3

"""
Entrypoint for agent harness
"""

### IMPORTS -------------------------------- ###

from os import environ
environ["TOKENIZERS_PARALLELISM"] = "false"

import yaml

from datetime import datetime
from src.job_parser.job_parser import Job
from src.logging.log_trace import log_trace
from src.models.llm import LLM
from src.models.embedder import Embedder
from src.report_formatter.report_formatter import format_report
from src.resume_evaluator.resume_evaluator import ResumeEvaluator
from src.resume_parser.resume_parser import Resume
from sys import argv

### GLOBAL VARS ---------------------------- ###

CONFIG_FILE = 'config/config.yaml'

### FUNCTIONS ------------------------------ ###

def read_yaml(path: str) -> dict:

    """
    Parsing config file containing global vars
    """

    with open(path) as opened_config_file:
        config_data = yaml.safe_load(opened_config_file)

    return config_data

### ---------------------------------------- ###

def print_header_art(return_string_only: bool=False):

    header = """
┏━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓
┃ ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛ ┃
┃ >>> RESUME EVALUATOR <<< ┃
┃ ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓ ┃
┗━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━┛
"""
    if return_string_only:
        return header.strip()
    else:
        print(header.strip())

### MAIN ----------------------------------- ###

if __name__ == "__main__":
    
    # Header art
    print_header_art()
    
    # Init exectution toggle
    exec_toggle = True
    
    # Parse config file
    log_trace('Loading config file')
    config_data = read_yaml(CONFIG_FILE)
    log_trace(trace_message='  \u2714 Done')

    # Init models
    log_trace(trace_message='Initializing LLM')
    llm_instance = LLM(
        model_checkpoint=config_data['text_generation']['model'],
        max_new_tokens=config_data['text_generation']['max_new_tokens']
    )
    log_trace(trace_message='  \u2714 Done')
    log_trace(trace_message='Initializing Embedder')
    embedder_instance = Embedder(
        model_checkpoint=config_data['text_embedding']['model']
    )
    log_trace(trace_message='  \u2714 Done')

    # Parse candidate resume
    log_trace(trace_message='Parsing candidate resume')
    resume = Resume()
    ok_signal, error_msg = resume.parse(config_data['resume']['path'])
    if not ok_signal:
        exec_toggle = False
        log_trace(trace_message=error_msg, timestamp=False)
    log_trace(trace_message='  \u2714 Done')
    
    # Parse job info
    log_trace(trace_message='Parsing job info')
    job_uri = argv[argv.index('--job_uri') + 1] if '--job_uri' in argv else ''
    job = Job()
    ok_signal, error_msg = job.parse(job_uri)
    if not ok_signal:
        exec_toggle = False
        log_trace(trace_message=error_msg, timestamp=False)
    log_trace(trace_message='  \u2714 Done')
    
    # Compare jobs to the resume
    if exec_toggle:
        log_trace(trace_message="Initializing resume evaluator")
        evaluator = ResumeEvaluator(config_data, llm_instance, embedder_instance, config_data['skills']['skills_dir'])
        log_trace(trace_message='  \u2714 Done')
        ok_signal, error_msg, evaluated_job = evaluator.compare_job_to_resume(resume=resume.candidate_info, job=job.job_details)
        if not ok_signal:
            log_trace(trace_message=error_msg, timestamp=False)
        else:
            # Beautify as markdown
            markdown_report = format_report(evaluated_job)
            # Save to markdown
            log_trace(trace_message='Saving job report')
            timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M")
            report_name = f'job_report_{job.job_details["title"]}_{job.job_details["company"]}_{timestamp}.md'.replace(' ', '')
            with open(report_name, 'w') as md_out:
                md_out.write(markdown_report)
            log_trace(trace_message='Task completed')
