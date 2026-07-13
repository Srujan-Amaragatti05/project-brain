from .pipeline import CollectorStage, CompilationContext
from typing import Dict, Any

class LegacyCollectorStage(CollectorStage):
    def execute(self, ctx: CompilationContext):
        import json
        from pathlib import Path
        
        web_dir = Path("docs-generated/web")
        if not web_dir.exists():
            raise FileNotFoundError("docs-generated/web not found. Legacy build must run first.")
            
        def safe_load(filename):
            file_path = web_dir / filename
            if file_path.exists():
                return json.loads(file_path.read_text(encoding="utf-8"))
            return None
            
        ctx.raw_data["docs"] = safe_load("docs.json") or {}
        ctx.raw_data["sidebar"] = safe_load("sidebar.json") or {}
        ctx.raw_data["search"] = safe_load("search-index.json") or {}
        ctx.raw_data["version"] = safe_load("version.json") or {}

