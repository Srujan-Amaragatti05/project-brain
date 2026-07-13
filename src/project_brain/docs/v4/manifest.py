from typing import List, Optional, Literal
from pydantic import BaseModel

class ManifestEndpoints(BaseModel):
    documents: str
    navigation: str
    assets: str
    search: str
    redirects: str
    capabilities: str
    content_base: str

class ManifestCapabilities(BaseModel):
    supported_document_types: List[str]
    supported_block_types: List[str]
    supported_inline_types: List[str]
    supported_languages: List[str]

class ManifestIntegrity(BaseModel):
    documents: str
    navigation: str
    assets: str
    search: str

class ManifestStatistics(BaseModel):
    total_documents: int
    total_assets: int

class ManifestBuildMetadata(BaseModel):
    generated_at: str
    generator_version: str
    cli_version: str
    git_commit: str
    build_duration_ms: int

class Manifest(BaseModel):
    schema_version: Literal["4.0.0"] = "4.0.0"
    build_id: str
    build_metadata: ManifestBuildMetadata
    statistics: ManifestStatistics
    integrity: ManifestIntegrity
    capabilities: ManifestCapabilities
    endpoints: ManifestEndpoints
