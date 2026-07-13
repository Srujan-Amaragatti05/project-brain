from typing import Dict
from pydantic import BaseModel

class Redirects(BaseModel):
    redirects: Dict[str, str]
