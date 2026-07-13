from typing import Literal, List, Union, Annotated, Optional
from pydantic import BaseModel, Field
from .inline import InlineNode

class BaseBlock(BaseModel):
    block_id: str

class ParagraphBlock(BaseBlock):
    type: Literal["paragraph"] = "paragraph"
    children: List[InlineNode]

class HeadingBlock(BaseBlock):
    type: Literal["heading"] = "heading"
    level: Literal[1, 2, 3, 4, 5, 6]
    children: List[InlineNode]

class CodeBlock(BaseBlock):
    type: Literal["code"] = "code"
    language: str
    code: str
    filename: Optional[str] = None
    highlight_lines: Optional[List[int]] = None

class CalloutBlock(BaseBlock):
    type: Literal["callout"] = "callout"
    severity: Literal["info", "warning", "danger", "success", "tip"]
    title: Optional[str] = None
    children: List['Block']

class TerminalLine(BaseModel):
    type: Literal["command", "output", "error", "success"]
    content: str

class TerminalBlock(BaseBlock):
    type: Literal["terminal"] = "terminal"
    lines: List[TerminalLine]
    typing_effect: bool = False

class FlagDefinition(BaseModel):
    name: str
    type: Optional[str] = None
    required: bool
    default: Optional[str] = None
    description: List['Block']

class FlagTableBlock(BaseBlock):
    type: Literal["flag_table"] = "flag_table"
    flags: List[FlagDefinition]

class TabItem(BaseModel):
    label: str
    children: List['Block']

class TabsBlock(BaseBlock):
    type: Literal["tabs"] = "tabs"
    tabs: List[TabItem]

class ImageBlock(BaseBlock):
    type: Literal["image"] = "image"
    asset_id: str
    alt: str
    caption: Optional[str] = None

class VideoBlock(BaseBlock):
    type: Literal["video"] = "video"
    asset_id: str
    alt: str
    caption: Optional[str] = None

class ListBlock(BaseBlock):
    type: Literal["list"] = "list"
    ordered: bool = False
    items: List[List['Block']]

class QuoteBlock(BaseBlock):
    type: Literal["quote"] = "quote"
    children: List['Block']

class WorkflowBlock(BaseBlock):
    type: Literal["workflow"] = "workflow"
    steps: List[List['Block']]

class TableRow(BaseModel):
    cells: List[List['Block']]

class TableBlock(BaseBlock):
    type: Literal["table"] = "table"
    headers: List[List[InlineNode]]
    rows: List[TableRow]

Block = Annotated[
    Union[
        ParagraphBlock,
        HeadingBlock,
        CodeBlock,
        CalloutBlock,
        TerminalBlock,
        FlagTableBlock,
        TabsBlock,
        ImageBlock,
        VideoBlock,
        ListBlock,
        QuoteBlock,
        WorkflowBlock,
        TableBlock
    ],
    Field(discriminator="type")
]
