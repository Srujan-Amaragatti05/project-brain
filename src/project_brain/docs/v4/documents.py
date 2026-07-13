from typing import Literal, List, Optional, Annotated, Union
from pydantic import BaseModel, Field
from .blocks import Block

class Relation(BaseModel):
    target_id: str
    type: Literal[
        "requires",
        "required_by",
        "uses",
        "used_by",
        "produces",
        "consumes",
        "see_also",
        "previous",
        "next",
        "workflow_step",
        "implements"
    ]

class VersioningInfo(BaseModel):
    introduced_in: str
    deprecated_in: Optional[str] = None
    stability: Literal["stable", "beta", "deprecated", "experimental"]

class BaseDocument(BaseModel):
    id: str
    slug: str
    aliases: List[str]
    title: str
    summary: str
    locale: str
    versioning: VersioningInfo
    blocks: List[Block]
    graph: dict = Field(default_factory=lambda: {"relations": []})

class CommandMetadata(BaseModel):
    command_name: str
    category: str
    is_plugin: bool
    examples: List[str] = []
    related: List[str] = []
    outputs: List[str] = []
    consumes: List[str] = []
    produces: List[str] = []
    prerequisites: List[str] = []
    use_cases: List[str] = []
    personas: List[str] = []
    tags: List[str] = []
    gifs: List[str] = []
    errors: List[str] = []
    notes: List[str] = []
    edge_cases: List[str] = []
    workflow: List[str] = []

class CommandDocument(BaseDocument):
    type: Literal["command"] = "command"
    metadata: CommandMetadata

class GuideMetadata(BaseModel):
    difficulty: Literal["beginner", "intermediate", "advanced"]
    estimated_minutes: int
    personas: List[str]

class GuideDocument(BaseDocument):
    type: Literal["guide"] = "guide"
    metadata: GuideMetadata

class ArchitectureMetadata(BaseModel):
    system: str
    components: List[str]

class ArchitectureDocument(BaseDocument):
    type: Literal["architecture"] = "architecture"
    metadata: ArchitectureMetadata

class ReleaseNotesMetadata(BaseModel):
    version: str
    release_date: str
    breaking_changes: bool

class ReleaseNotesDocument(BaseDocument):
    type: Literal["release"] = "release"
    metadata: ReleaseNotesMetadata

class ReferenceMetadata(BaseModel):
    module: str
    is_public_api: bool

class ReferenceDocument(BaseDocument):
    type: Literal["reference"] = "reference"
    metadata: ReferenceMetadata

Document = Annotated[
    Union[
        CommandDocument,
        GuideDocument,
        ArchitectureDocument,
        ReleaseNotesDocument,
        ReferenceDocument
    ],
    Field(discriminator="type")
]
