import uuid
from typing import List, Dict, Any
from project_brain.docs.v4.documents import Document

class CompilationContext:
    def __init__(self):
        self.raw_data: Dict[str, Any] = {}
        self.documents: Dict[str, Document] = {}
        self.assets: Dict[str, Any] = {}
        self.navigation = None
        self.search = None
        self.manifest = None
        self.redirects = None
        self.document_registry = None

class CollectorStage:
    def execute(self, ctx: CompilationContext):
        pass

class NormalizerStage:
    def execute(self, ctx: CompilationContext):
        pass

class ASTBuilderStage:
    def execute(self, ctx: CompilationContext):
        pass

class LinkerStage:
    def execute(self, ctx: CompilationContext):
        pass

class AssetResolverStage:
    def execute(self, ctx: CompilationContext):
        pass

class NavigationBuilderStage:
    def execute(self, ctx: CompilationContext):
        pass

class SearchBuilderStage:
    def execute(self, ctx: CompilationContext):
        pass

class ValidationCompilerStage:
    def execute(self, ctx: CompilationContext):
        pass

class PublisherStage:
    def execute(self, ctx: CompilationContext):
        pass

class PluginRegistry:
    def __init__(self):
        self.extractors = []
        self.normalizers = []
        self.validators = []
        self.emitters = []

    def register_extractor(self, fn): self.extractors.append(fn)
    def register_normalizer(self, fn): self.normalizers.append(fn)
    def register_validator(self, fn): self.validators.append(fn)
    def register_emitter(self, fn): self.emitters.append(fn)

class CompilerPipeline:
    def __init__(self):
        self.collectors: List[CollectorStage] = []
        self.normalizers: List[NormalizerStage] = []
        self.ast_builders: List[ASTBuilderStage] = []
        self.linkers: List[LinkerStage] = []
        self.asset_resolvers: List[AssetResolverStage] = []
        self.nav_builders: List[NavigationBuilderStage] = []
        self.search_builders: List[SearchBuilderStage] = []
        self.validators: List[ValidationCompilerStage] = []
        self.publishers: List[PublisherStage] = []
        self.plugins = PluginRegistry()

    def run(self) -> CompilationContext:
        ctx = CompilationContext()
        
        for fn in self.plugins.extractors: fn(ctx)
        
        for stage in self.collectors:
            stage.execute(ctx)
            
        for fn in self.plugins.normalizers: fn(ctx)
            
        for stage in self.normalizers:
            stage.execute(ctx)
            
        for stage in self.ast_builders:
            stage.execute(ctx)
            
        for stage in self.linkers:
            stage.execute(ctx)
            
        for stage in self.asset_resolvers:
            stage.execute(ctx)
            
        for stage in self.nav_builders:
            stage.execute(ctx)
            
        for stage in self.search_builders:
            stage.execute(ctx)
            
        for fn in self.plugins.validators: fn(ctx)
            
        for stage in self.validators:
            stage.execute(ctx)
            
        for fn in self.plugins.emitters: fn(ctx)
            
        for stage in self.publishers:
            stage.execute(ctx)
            
        return ctx
