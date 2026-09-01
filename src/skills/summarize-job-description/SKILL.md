---
name: summarize-job-description
description: Reads a job description and creates a summary
---

## Inputs

```json
{
  "job_description" : "Description of the job"
}
```

## Default inputs

```json
{
  "job_description" : "None"
}
```

## Purpose

Read a job description and create a summary

## Directions

- Summary should include the wider scope of the job.
- Do not repeat all technical requirements, just report them in wide strokes.
- Only focus on the job iteself, not the company or any other context.
- Do report the salary range, if available.
- Comment on whether the job is remote or hybrid or on-site.
- Structure the summary as plain text (not markdown) with the following 3 sections:
  - **Overview**: High level description of the job.
  - **Scope & Requirements**: Description of the main tasks and requirements.
  - **Logistics**: Describe if the work is remote, hybrid, or in person and discuss the salary range.

## Workflow

1. Read the following job description and create a short summary:\n <job_description> /no_think

## Completion message

<previous_output>
