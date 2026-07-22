from .pipeline import PublisherStage, CompilationContext
import json
from pathlib import Path

class BasePublisher(PublisherStage):
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def execute(self, ctx: CompilationContext):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.publish(ctx)

    def publish(self, ctx: CompilationContext):
        # Load previous registry to determine what changed before overwriting it
        prev_registry_path = self.output_dir / "documents.json"
        prev_checksums = {}
        if prev_registry_path.exists():
            try:
                prev_data = json.loads(prev_registry_path.read_text())
                if isinstance(prev_data, dict) and "documents" in prev_data:
                    for doc in prev_data["documents"]:
                        prev_checksums[doc["id"]] = doc.get("checksum")
            except Exception:
                pass # Proceed with full rebuild if corrupted

        # 1. Write the registries
        if ctx.manifest:
            (self.output_dir / "manifest.json").write_text(ctx.manifest.model_dump_json(indent=2))
        
        if ctx.document_registry:
            (self.output_dir / "documents.json").write_text(ctx.document_registry.model_dump_json(indent=2))
            
        if ctx.navigation:
            (self.output_dir / "navigation.json").write_text(ctx.navigation.model_dump_json(indent=2))
            
        if ctx.assets:
            (self.output_dir / "assets.json").write_text(ctx.assets.model_dump_json(indent=2))
            
        if ctx.search:
            (self.output_dir / "search-index.json").write_text(ctx.search.model_dump_json(indent=2))
            
        if ctx.redirects:
            (self.output_dir / "redirects.json").write_text(ctx.redirects.model_dump_json(indent=2))
            
        # 2. Write the content payload incrementally
        content_dir = self.output_dir / "content"
        content_dir.mkdir(exist_ok=True)
        
        skipped_count = 0
        written_count = 0
        
        for doc_id, doc in ctx.documents.items():
            uuid_part = doc_id.split(":")[-1]
            out_file = content_dir / f"{uuid_part}.json"
            
            # Find the new checksum from the context's document registry
            new_checksum = None
            if ctx.document_registry:
                for entry in ctx.document_registry.documents:
                    if entry.id == doc_id:
                        new_checksum = entry.checksum
                        break
                        
            # Incremental check
            if new_checksum and prev_checksums.get(doc_id) == new_checksum and out_file.exists():
                skipped_count += 1
                continue
                
            out_file.write_text(doc.model_dump_json(indent=2))
            written_count += 1
            
        print(f"Incremental Build: Wrote {written_count} files, skipped {skipped_count} unchanged files.")
