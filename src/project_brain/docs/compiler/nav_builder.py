from .pipeline import NavigationBuilderStage, CompilationContext

from project_brain.docs.v4 import NavigationRegistry, NavNode

class LegacyNavBuilderStage(NavigationBuilderStage):
    def execute(self, ctx: CompilationContext):
        # Build sidebar from ctx.documents based on categories
        sidebar = []
        categories = {}
        for doc_id, doc in ctx.documents.items():
            if hasattr(doc, "metadata") and getattr(doc.metadata, "category", None):
                cat = doc.metadata.category
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(NavNode(
                    id=doc_id,
                    label=doc.title,
                    target_id=doc_id
                ))
                
        for cat, nodes in categories.items():
            sidebar.append(NavNode(
                id=f"cat_{cat}",
                label=cat,
                children=nodes
            ))
            
        ctx.navigation = NavigationRegistry(
            sidebar=sidebar,
            topbar=[],
            footer=[]
        )
