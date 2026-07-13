from typing import Literal, List, Optional, Dict
from pydantic import BaseModel

class AssetDimensions(BaseModel):
    width: int
    height: int

class Asset(BaseModel):
    id: str
    type: Literal["image", "video", "document"]
    mime: str
    storage_key: str
    checksum_sha256: str
    size_bytes: int
    dimensions: Optional[AssetDimensions] = None
    alt_fallback: str
    caption_fallback: Optional[str] = None
    referenced_by: List[str]

class AssetRegistry(BaseModel):
    assets: Dict[str, Asset]
