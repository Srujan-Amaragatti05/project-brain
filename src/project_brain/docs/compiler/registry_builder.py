from .pipeline import CompilerPipeline, CompilationContext
from project_brain.docs.v4 import DocumentRegistry, DocumentRegistryEntry
import hashlib

class RegistryBuilderStage:
    def execute(self, ctx: CompilationContext):
        entries = []
        for doc_id, doc in ctx.documents.items():
            json_dump = doc.model_dump_json()
            checksum = hashlib.sha256(json_dump.encode()).hexdigest()
            entries.append(DocumentRegistryEntry(
                id=doc.id,
                slug=doc.slug,
                type=doc.type,
                title=doc.title,
                summary=doc.summary,
                checksum=checksum,
                size_bytes=len(json_dump),
                last_modified="2026-07-11T00:00:00Z"
            ))
        ctx.document_registry = DocumentRegistry(documents=entries)
