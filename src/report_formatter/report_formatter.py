#!/bin/bash python3

### FUNCTIONS ------------------------------ ###

def format_report(report: dict) -> str:

    """
    Formats list[dict] into a markdown.
    """

    md_report = f"""
# {report["title"]}

## Info
* **Company:** {report["company"]}
* **Industry:** {report["industry"]}
* **Employment type:** {report["employment_type"]}
* **Location:** {report["location"]}
* **Seniority:** {report["seniority_level"]}
* **Function:** {report["job_function"]}
* **Time posted:** {report["time"]}
* **Link:** [job_posting]({report["link"]})

## Full description
{report["description"]}

## AI Scoring
* **Broad:** {report["broad_score"]}
* **Skills:** {report["skills_score"]}

## AI Summary
{report["generated_summary"]}

### Requirements
[REQUIREMENTS]

### Resume improvements
{report["proposed_resume_improvements"]}
"""

    md_report = md_report.replace("[REQUIREMENTS]", "\n".join(report["inferred_requirements"]))

    return md_report.strip()
