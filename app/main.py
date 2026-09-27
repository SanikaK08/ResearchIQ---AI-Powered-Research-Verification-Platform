from django.contrib.gis import db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from streamlit import json
from app.schemas import ResearchRequest, ResearchResponse
from app.ai import create_research_plan, parse_tasks, generate_report, verify_report
from app.research import search_web
from app.database import get_db
from app.models import Research
from app.research import research_all_tasks
from app.models import Research, ResearchSource
import json

app= FastAPI(
    title="ResearchIQ",
    description="Multi-Agent AI Research & Competitive Intelligence System",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "welcome"
    }




@app.post("/research")
def create_research(request: ResearchRequest, db: Session = Depends(get_db)):
    try:
        research = Research(
        query=request.query,
        report="",
        verification="",
        status="planning"
    )

        db.add(research)
        db.commit()
        db.refresh(research)
        plan = create_research_plan(request.query)
        tasks = parse_tasks(plan)


        research.status = "researching"
        db.commit()


        research_results = research_all_tasks(tasks)
        research.status = "generating"
        db.commit()

        report = generate_report(
        request.query,
        research_results
    )
        research.status = "verifying"
        db.commit()

        

        verification_text = verify_report(
        request.query,
        report,
        research_results
    )

        verification_text = verification_text.strip()

        if verification_text.startswith("```"):
            verification_text = (
                verification_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        verification = json.loads(verification_text)
        research.report = report
        research.verification = json.dumps(verification)
        research.status = "completed"

        
        seen_urls = set()

        for result in research_results:

            for source in result["sources"]:

                if source.url in seen_urls:
                    continue

                seen_urls.add(source.url)

                research.sources.append(
                    ResearchSource(
                        title=source.title,
                        url=source.url
                    )
                )
      
        db.commit()
        db.refresh(research)

        sources = [
        {
            "title": source.title,
            "url": source.url
        }
        for source in research.sources
    ]
        

        return {
            "research_id": research.research_id,
            "query": research.query,
            "report": research.report,
            "verification": research.verification,
            "sources": sources
            
        }
    except Exception:
        research.status = "failed"
        db.commit()
        raise

@app.get("/research")
def get_research_history(
    db: Session = Depends(get_db)
):
    researches = db.scalars(
        select(Research).order_by(
            Research.created_at.desc()
        )
    ).all()

    return researches

@app.get("/research/{research_id}")
def get_research(
    research_id: int,
    db: Session = Depends(get_db)
):

    research = db.scalar(
        select(Research).where(
            Research.research_id == research_id
        )
    )

    if not research:
        raise HTTPException(
            status_code=404,
            detail="Research not found"
        )

    return {
    "research_id": research.research_id,
    "status": research.status,
    "query": research.query,
    "report": research.report,
    "verification": research.verification,
    "sources": [
        {
            "title": source.title,
            "url": source.url
        }
        for source in research.sources
    ]
}
