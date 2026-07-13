from typing import Literal, List, Union, Annotated
from pydantic import BaseModel, Field

class TextNode(BaseModel):
    type: Literal["text"] = "text"
    content: str

class BoldNode(BaseModel):
    type: Literal["bold"] = "bold"
    children: List['InlineNode']

class ItalicNode(BaseModel):
    type: Literal["italic"] = "italic"
    children: List['InlineNode']

class CodeNode(BaseModel):
    type: Literal["code"] = "code"
    content: str

class ExternalLinkNode(BaseModel):
    type: Literal["external_link"] = "external_link"
    url: str
    children: List['InlineNode']

class DocLinkNode(BaseModel):
    type: Literal["doc_link"] = "doc_link"
    target_id: str
    children: List['InlineNode']

class KeyboardNode(BaseModel):
    type: Literal["keyboard"] = "keyboard"
    keys: List[str]

class BadgeNode(BaseModel):
    type: Literal["badge"] = "badge"
    content: str
    variant: Literal["info", "warning", "error", "success", "tip"]

InlineNode = Annotated[
    Union[
        TextNode,
        BoldNode,
        ItalicNode,
        CodeNode,
        ExternalLinkNode,
        DocLinkNode,
        KeyboardNode,
        BadgeNode
    ],
    Field(discriminator="type")
]
