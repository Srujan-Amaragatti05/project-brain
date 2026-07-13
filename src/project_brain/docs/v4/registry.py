from typing import List
from pydantic import BaseModel

class DocumentRegistryEntry(BaseModel):
    id: str
    slug: str
    type: str
    title: str
    summary: str
    checksum: str
    size_bytes: int
    last_modified: str

class DocumentRegistry(BaseModel):
    documents: List[DocumentRegistryEntry]
