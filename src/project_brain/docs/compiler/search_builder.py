from .pipeline import SearchBuilderStage, CompilationContext

from project_brain.docs.v4 import SearchIndex, SearchEntry, HeadingEntry

class LegacySearchBuilderStage(SearchBuilderStage):
    def execute(self, ctx: CompilationContext):
        entries = []
        for doc_id, doc in ctx.documents.items():
            entries.append(SearchEntry(
                document_id=doc_id,
                title=doc.title,
                keywords=doc.aliases,
                headings=[],
                snippet=doc.summary
            ))
        ctx.search = SearchIndex(entries=entries)
