from .pipeline import NormalizerStage, CompilationContext

class BaseNormalizer(NormalizerStage):
    def execute(self, ctx: CompilationContext):
        pass
