from .pipeline import ASTBuilderStage, CompilationContext
from project_brain.docs.v4.blocks import Block
from project_brain.docs.v4.inline import InlineNode

class LegacyASTBuilderStage(ASTBuilderStage):
    def execute(self, ctx: CompilationContext):
        import uuid
        from project_brain.docs.v4 import (
            CommandDocument, CommandMetadata, VersioningInfo,
            ParagraphBlock, TextNode, HeadingBlock, CodeBlock, TerminalBlock, TerminalLine,
            FlagTableBlock, FlagDefinition
        )
        
        raw_docs = ctx.raw_data.get("docs", {})
        
        for category, commands in raw_docs.items():
            for cmd_id, raw_cmd in commands.items():
                meta = raw_cmd.get("metadata", {})
                
                # We need a stable UUID based on the command name to avoid churn
                # (e.g. UUIDv5 based on DNS, but for simplicity here we'll fake a stable one)
                import hashlib
                h = hashlib.md5(raw_cmd["command"].encode()).hexdigest()
                stable_uuid = f"{h[:8]}-{h[8:12]}-4{h[13:16]}-8{h[17:20]}-{h[20:32]}"
                doc_urn = f"urn:brain:doc:{stable_uuid}"
                
                blocks = []
                
                # 1. Help text block
                help_text = raw_cmd.get("help", "")
                blocks.append(ParagraphBlock(
                    block_id=f"blk_{hashlib.md5(help_text.encode()).hexdigest()[:8]}",
                    children=[TextNode(content=help_text)]
                ))
                
                # 2. Parameters block
                params = raw_cmd.get("parameters", [])
                if params:
                    flags = []
                    for p in params:
                        flags.append(FlagDefinition(
                            name=p.get("name", ""),
                            type=p.get("type", "str"),
                            required=p.get("required", False),
                            default=str(p.get("default", "")) if p.get("default") is not None else None,
                            description=[ParagraphBlock(
                                block_id=f"blk_param_{p.get('name')}",
                                children=[TextNode(content=p.get("help", ""))]
                            )]
                        ))
                    blocks.append(FlagTableBlock(
                        block_id=f"blk_{hashlib.md5(b'params').hexdigest()[:8]}",
                        flags=flags
                    ))
                
                doc = CommandDocument(
                    id=doc_urn,
                    type="command",
                    slug=category + "/" + raw_cmd["command"].replace(" ", "-"),
                    aliases=[raw_cmd["command"]],
                    title=raw_cmd["command"],
                    summary=help_text.split('\n')[0] if help_text else "",
                    locale="en",
                    versioning=VersioningInfo(
                        introduced_in=meta.get("introduced", "0.1.0"),
                        stability=meta.get("stability", "stable")
                    ),
                    blocks=blocks,
                    metadata=CommandMetadata(
                        command_name=raw_cmd["command"],
                        category=category,
                        is_plugin=False,
                        examples=meta.get("examples", []),
                        related=meta.get("related", []),
                        outputs=meta.get("outputs", []),
                        consumes=meta.get("consumes", []),
                        produces=meta.get("produces", []),
                        prerequisites=meta.get("prerequisites", []),
                        use_cases=meta.get("use_cases", []),
                        personas=meta.get("personas", []),
                        tags=meta.get("tags", []),
                        gifs=meta.get("gifs", []),
                        errors=meta.get("errors", []),
                        notes=meta.get("notes", []),
                        edge_cases=meta.get("edge_cases", []),
                        workflow=meta.get("workflow", [])
                    )
                )
                
                ctx.documents[doc_urn] = doc
