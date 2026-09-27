import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def create_research_plan(query: str):

    prompt = f"""
You are the Research Planner Agent.

Research topic:
{query}

Create 5 to 7 specific research tasks.

Each task must:
- be specific
- be independently researchable
- help answer the original question
- focus on factual information

Return ONLY the tasks.

Format:
TASK: <task>

Do not number the tasks.
Do not provide explanations.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

def parse_tasks(plan: str):

    tasks = []

    for line in plan.splitlines():

        line = line.strip()

        if line.startswith("TASK:"):
            task = line.replace("TASK:", "", 1).strip()

            if task:
                tasks.append(task)

    return tasks

def generate_report(query: str, research_results):

    research_text = ""

    for result in research_results:

        research_text += f"\n\nTASK:\n{result['task']}\n"

        for source in result["sources"]:
            research_text += f"""
SOURCE TITLE: {source.title}
SOURCE URL: {source.url}
SOURCE CONTENT:
{source.content}
"""

    prompt = f"""
You are the Report Generator Agent for ResearchIQ.

The user asked:

{query}

Below is information collected from web sources:

{research_text}

Generate a professional smallresearch report in Markdown.

Follow this exact structure:

# Executive Summary
Give a concise overview of the research findings.

# Key Findings
List the most important findings as bullet points.

# Detailed Analysis
Explain the findings using information from the collected sources.
Use appropriate ## subheadings.

# Comparison
If the query compares entities, provide a Markdown comparison table.
If a comparison table is not appropriate, omit this section.

# Conclusion
Summarize the evidence-based conclusions without introducing information
that was not present in the research sources.

# Sources
List every source actually used in the research.
For each source, provide its title as a clickable Markdown link.

Important:
- Use only information from the provided research results.
- Do not invent facts, statistics, URLs, or sources.
- Do not mention that you are an AI.
- Return only the Markdown report.

Write a clear professional report.

"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text




def verify_report(query: str, report: str, research_results):

    research_text = ""

    for result in research_results:

        research_text += f"\n\nTASK:\n{result['task']}\n"

        for source in result["sources"]:
            research_text += f"""
SOURCE TITLE: {source.title}
SOURCE URL: {source.url}
SOURCE CONTENT:
{source.content}
"""

    prompt = f"""
You are the Verification Agent for ResearchIQ.

Original research question:
{query}

Generated report:
{report}

Available source material:
{research_text}

Return ONLY valid JSON.

The JSON must be an array of verification claims.

Each claim must have:

{{
    "claim": "The factual claim being checked",
    "status": "supported",
    "explanation": "Why the available evidence supports or does not support the claim",
    "supporting_sources": [
        {{
            "title": "Source title",
            "url": "Source URL"
        }}
    ]
}}

Allowed status values:
- supported
- partially_supported
- unsupported

Rules:
- Verify claims ONLY against the provided research sources.
- Do not invent sources.
- Do not invent evidence.
- If the evidence is insufficient, use "unsupported" or "partially_supported".
- Keep the explanation concise.
- Return ONLY JSON.
"""
    
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    verification_text = response.text.strip()
        
    

    return verification_text


