# ResearchIQ

## AI-Powered Research and Verification Platform

ResearchIQ is a full-stack AI research application that converts a broad
research query into focused tasks, performs web research, generates a
structured report, and verifies important claims against collected
sources.

The goal is to make AI-assisted research more structured, traceable, and
easier to inspect.

## Problem Statement

Traditional research often requires searching multiple sources,
collecting relevant information, comparing findings, and manually
organizing the results.

AI can make this process faster, but AI-generated reports may contain
unsupported or inaccurate claims. ResearchIQ addresses this by combining
automated research, source tracking, report generation, and claim-level
verification in one workflow.

## Objectives

-   Convert a broad research query into focused research tasks.
-   Perform web research using multiple sources.
-   Collect and preserve source information.
-   Generate a structured research report.
-   Verify important claims against collected evidence.
-   Store research history for later access.
-   Provide a simple web interface for interacting with the system.

## Key Features

### AI Research Planning

The system analyzes the user's query and creates multiple focused
research tasks.

### Parallel Web Research

The generated tasks are researched using the Tavily API. Multiple tasks
can be processed independently to collect relevant web sources.

### Source Tracking

Research sources are stored with their titles and URLs so that users can
inspect the evidence used during research.

### Structured Report Generation

The collected research results are passed to Gemini to generate a
readable Markdown research report.

### Claim Verification

Important claims in the generated report are checked against the
collected research evidence.

Verification results are returned in structured JSON and can classify
claims as:

-   Supported
-   Partially supported
-   Unsupported

### Research History

Research records, reports, verification data, and source references are
stored in MySQL.

### Progress and Status Tracking

The research workflow tracks stages such as:

-   Planning
-   Researching
-   Generating
-   Verifying
-   Completed
-   Failed

## System Architecture

```text
                         User
                           |
                           v
                    +--------------+
                    | Streamlit UI |
                    +--------------+
                           |
                           v
                    +--------------+
                    | FastAPI      |
                    | Backend      |
                    +--------------+
                           |
                           v
                 +---------------------+
                 |   Planner Agent     |
                 | Query -> Tasks      |
                 +---------------------+
                           |
                           v
                    Research Tasks
                           |
                           v
                 +---------------------+
                 |  Researcher Agent   |
                 | Web Search & Sources |
                 +---------------------+
                           |
                           v
                      Tavily API
                           |
                           v
                      Web Sources
                           |
                           |
                           v
                 +---------------------+
                 |     Writer Agent     |
                 | Research -> Report   |
                 +---------------------+
                           |
                           v
                      Gemini API
                           |
                           v
                   Research Report
                           |
                           v
                 +---------------------+
                 |   Verifier Agent     |
                 | Claim Verification   |
                 +---------------------+
                           |
                           v
                  Structured Claims
                           |
                           v
                    +--------------+
                    |    MySQL     |
                    |   Database   |
                    +--------------+
                           |
                           v
                  Research History
                           |
                           v
                    Streamlit UI


And immediately after it, add:

```markdown
### Agent Responsibilities

| Agent | Responsibility |
|---|---|
| Planner Agent | Breaks the user's research query into focused research tasks. |
| Researcher Agent | Executes research tasks and collects relevant web sources using Tavily. |
| Writer Agent | Combines collected research and generates the final research report using Gemini. |
| Verifier Agent | Checks important claims in the generated report against the collected research evidence. |

### Workflow

```text
User Query
    |
    v
Planner Agent
    |
    v
Research Tasks
    |
    v
Researcher Agent
    |
    v
Tavily + Web Sources
    |
    v
Writer Agent
    |
    v
Research Report
    |
    v
Verifier Agent
    |
    v
Structured Verification
    |
    v
MySQL
    |
    v
Final Result

1.  The user enters a research query through the Streamlit interface.
2.  Streamlit sends the query to the FastAPI backend.
3.  The backend creates a research record with an initial status.
4.  The research planner converts the query into focused tasks.
5.  Each task is researched using the Tavily API.
6.  The collected sources and research results are passed to the report
    generator.
7.  Gemini generates the research report.
8.  The verification module checks important claims against the
    collected evidence.
9.  Verification results are converted from JSON text into structured
    Python data.
10. The report, verification results, and sources are stored in MySQL.
11. The final result is returned to the Streamlit frontend.
12. The user can view the report, verification information, and sources.

## Technology Stack

### Frontend

-   Streamlit

### Backend

-   Python
-   FastAPI
-   Uvicorn

### AI

-   Google Gemini API

### Web Research

-   Tavily API

### Database

-   MySQL
-   SQLAlchemy

### Data Format

-   JSON
-   Markdown

## Project Structure

``` text
researchIQ/
|
├── app/
│   ├── main.py
│   ├── ai.py
│   ├── research.py
│   ├── models.py
│   ├── database.py
│   └── ...
|
├── frontend/
│   └── streamlit_app.py
|
├── requirements.txt
├── README.md
└── ...
```



## Running the Project

### 1. Clone the repository

``` bash
git clone <repository-url>
cd researchIQ
```

### 2. Create and activate a virtual environment

Windows PowerShell:

``` powershell
python -m venv python39
.\python39\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add the required API keys and database
configuration.

Example:

``` env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

DATABASE_URL=mysql+pymysql://username:password@localhost/fastapi_db
```

Do not commit `.env` or API keys to the repository.

### 5. Start the FastAPI backend

``` bash
uvicorn app.main:app --reload
```

The API will be available at:

``` text
http://127.0.0.1:8000
```

FastAPI documentation:

``` text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit frontend

From the project directory:

``` bash
streamlit run frontend/streamlit_app.py
```

The Streamlit interface will then open in the browser.

## Future Improvements

-   Improve progress updates during long-running research.
-   Improve report formatting and visualization.
-   Expand structured claim verification.
-   Add stronger source-quality evaluation.
-   Add authentication if multi-user access becomes necessary.
-   Add document-based RAG for private research material.
-   Add caching to reduce repeated web searches.
-   Add automated testing for research workflows.
-   Containerize the application using Docker.
-   Deploy the application to a cloud platform.


