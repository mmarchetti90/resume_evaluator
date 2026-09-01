---
name: extract-job-requirements
description: Reads a job description and creates a list of job requirements
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

Read a job description and create a list of job requirements.

## Directions

- Consider the wide scope of the job to understand the needed background knowledge.
- Look for stated responsibilities, qualifications, and skills required.
- If technical skills are listed, report them.
- Format the reported info as plain text bullet points (not markdown).

## Workflow

1. Read the following job description and create a list of job requirements:\n <job_description> /no_think

## Completion message

<previous_output>
