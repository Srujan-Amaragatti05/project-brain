from typing import List, Optional, Literal
from pydantic import BaseModel

class NavNode(BaseModel):
    id: str
    label: str
    icon: Optional[str] = None
    target_id: Optional[str] = None
    external_url: Optional[str] = None
    children: Optional[List['NavNode']] = None

class NavigationRegistry(BaseModel):
    sidebar: List[NavNode]
    topbar: List[NavNode]
    footer: List[NavNode]
