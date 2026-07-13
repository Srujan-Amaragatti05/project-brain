from .pipeline import LinkerStage, CompilationContext
from project_brain.docs.v4.documents import Relation

class BaseLinker(LinkerStage):
    def execute(self, ctx: CompilationContext):
        # Reverse relationships resolution logic
        self.resolve_reverse_relations(ctx)

    def resolve_reverse_relations(self, ctx: CompilationContext):
        # For example, if A requires B, automatically add 'required_by' A to B
        pass
