from .pipeline import CompilerPipeline, CompilationContext
from project_brain.docs.v4 import (
    Manifest, ManifestBuildMetadata, ManifestStatistics, 
    ManifestIntegrity, ManifestCapabilities, ManifestEndpoints
)
import hashlib
import time

class ManifestBuilderStage:
    def execute(self, ctx: CompilationContext):
        # We need to hash the registries if they exist
        def hash_registry(reg):
            if not reg: return ""
            return hashlib.sha256(reg.model_dump_json().encode()).hexdigest()
            
        ctx.manifest = Manifest(
            schema_version="4.0.0",
            build_id="build_fake_uuid",
            build_metadata=ManifestBuildMetadata(
                generated_at="2026-07-11T00:00:00Z",
                generator_version="4.0",
                cli_version="1.2.0",
                git_commit="unknown",
                build_duration_ms=100
            ),
            statistics=ManifestStatistics(
                total_documents=len(ctx.documents),
                total_assets=len(ctx.assets.assets) if ctx.assets else 0
            ),
            integrity=ManifestIntegrity(
                documents=hash_registry(ctx.document_registry),
                navigation=hash_registry(ctx.navigation),
                assets=hash_registry(ctx.assets),
                search=hash_registry(ctx.search)
            ),
            capabilities=ManifestCapabilities(
                supported_document_types=["command", "guide"],
                supported_block_types=["paragraph", "heading", "code", "terminal", "flag_table"],
                supported_inline_types=["text", "bold", "doc_link"],
                supported_languages=["en"]
            ),
            endpoints=ManifestEndpoints(
                documents="documents.json",
                navigation="navigation.json",
                assets="assets.json",
                search="search-index.json",
                redirects="redirects.json",
                capabilities="capabilities.json",
                content_base="content/"
            )
        )
