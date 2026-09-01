---
name: evaluate-candidate
description: Compares a candidate resume with a job description to determine compatibility
---

## Inputs

```json
{
  "job_description" : "Description of the job",
  "candidate_description" : "Brief description of the candidate",
  "candidate_experience" : "Experience of the candidate",
  "candidate_skills" : "Skills of the candidate"
}
```

## Default inputs

```json
{
  "job_description" : "None",
  "candidate_description" : "None",
  "candidate_experience" : "None",
  "candidate_skills" : "None"
}
```

## Purpose

Read a job description and candidate resume, comment on fitness, and provide suggestions of improvements.

## Directions

- Be honest in your assessment.
- Thoroughly evaluate the candidate's skills and experience against the job requirements.
- Be specific in how the candidate's resume can be improved to emphasize their strengths related to the job.
- When suggesting resume changes, base yourself on the current contents of the resume, DO NOT invent skills/experience not stated by the candidate.
- Structure the final report as plain text (not markdown) with the following sections:
  - **Overall Assessment**: High level description of the candidate's fitness for the job.
  - **Candidate's strenghts**: Bullet list of where the candidate's skills/experience overlap with the job.
  - **Candidate's weaknesses**: Bullet list of where the candidate's skills/experience do not overlap with the job.
  - **Suggested resume improvements**: Description of changes that would increase the candidate's chances at an interview.

## Workflow

1. Analyze the following job opening:\n<job_description> /no_think
2. Compare the job opening to the following candidate resume:\nCandidate description: <candidate_description>\n\nCandidate experience: <candidate_experience>\n\nCandidate skills: <candidate_skills> /no_think
3. Summarize how the candidate fits the job opening and what improvements can be made to the resume /no_think

## Completion message

<previous_output>

