from typing import List, Dict
from pydantic import BaseModel

class HeadingEntry(BaseModel):
    title: str
    block_id: str

class SearchEntry(BaseModel):
    document_id: str
    title: str
    keywords: List[str]
    headings: List[HeadingEntry]
    snippet: str

class SearchIndex(BaseModel):
    entries: List[SearchEntry]
