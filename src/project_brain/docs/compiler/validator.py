from .pipeline import ValidationCompilerStage, CompilationContext

class BaseValidator(ValidationCompilerStage):
    def execute(self, ctx: CompilationContext):
        self.validate(ctx)
        
    def validate(self, ctx: CompilationContext):
        # 1. Duplicate IDs, Aliases, Slugs
        seen_ids = set()
        seen_slugs = set()
        seen_aliases = set()
        
        for doc_id, doc in ctx.documents.items():
            if doc_id in seen_ids:
                raise ValueError(f"Duplicate document ID: {doc_id}")
            seen_ids.add(doc_id)
            
            if doc.slug in seen_slugs:
                raise ValueError(f"Duplicate slug: {doc.slug}")
            seen_slugs.add(doc.slug)
            
            for alias in doc.aliases:
                if alias in seen_aliases or alias in seen_slugs:
                    raise ValueError(f"Duplicate or conflicting alias: {alias}")
                seen_aliases.add(alias)
                
            # 2. Duplicate block IDs
            seen_blocks = set()
            for block in doc.blocks:
                self._validate_block(block, seen_blocks, ctx)
                
            # 3. Broken References (Graph)
            for relation in doc.graph.get("relations", []):
                if relation.target_id not in ctx.documents:
                    raise ValueError(f"Broken relation: {doc_id} points to missing {relation.target_id}")
                    
        # 4. Broken Navigation
        if ctx.navigation:
            self._validate_nav(ctx.navigation.sidebar, ctx)
            self._validate_nav(ctx.navigation.topbar, ctx)
            self._validate_nav(ctx.navigation.footer, ctx)
            
        # 5. Missing Assets
        if ctx.assets:
            for asset_id, asset in ctx.assets.assets.items():
                if not asset.referenced_by:
                    raise ValueError(f"Orphan asset: {asset_id}")

    def _validate_block(self, block, seen_blocks, ctx):
        if block.block_id in seen_blocks:
            raise ValueError(f"Duplicate block ID: {block.block_id}")
        seen_blocks.add(block.block_id)
        
        if block.type in ["image", "video"]:
            if not ctx.assets or block.asset_id not in ctx.assets.assets:
                raise ValueError(f"Missing asset referenced in block: {block.asset_id}")
                
        if hasattr(block, "children"):
            for child in block.children:
                # Basic recursive validation placeholder
                pass

    def _validate_nav(self, nodes, ctx):
        for node in nodes:
            if node.target_id and node.target_id not in ctx.documents:
                raise ValueError(f"Broken navigation target: {node.target_id}")
            if node.children:
                self._validate_nav(node.children, ctx)
