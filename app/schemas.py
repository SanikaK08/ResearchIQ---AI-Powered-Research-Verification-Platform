from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    query: str
    tasks: list[str]

class Source(BaseModel):
    title: str
    url: str
    content: str

class ResearchResult(BaseModel):
    task: str
    sources: list[Source]