from .pipeline import ValidationCompilerStage, CompilationContext
import json
from pathlib import Path

class SemanticShadowValidatorStage(ValidationCompilerStage):
    def execute(self, ctx: CompilationContext):
        report = []
        report.append("# Semantic Shadow Validator Report\n")
        
        v1_docs = ctx.raw_data.get("docs", {})
        
        failed = False
        
        # Flatten V1 docs
        v1_flat = {}
        for category, commands in v1_docs.items():
            for cmd_id, raw_cmd in commands.items():
                v1_flat[raw_cmd["command"]] = raw_cmd
                
        # Flatten V4 docs
        v4_flat = {doc.title: doc for doc in ctx.documents.values() if doc.type == "command"}
        
        for cmd_name, raw_cmd in v1_flat.items():
            if cmd_name not in v4_flat:
                report.append(f"✗ {cmd_name}\n    Missing entirely in V4\n")
                failed = True
                continue
                
            doc = v4_flat[cmd_name]
            meta = raw_cmd.get("metadata", {})
            issues = []
            
            # Check core
            expected_help = raw_cmd.get("help", "")
            if not doc.blocks or not hasattr(doc.blocks[0], 'children') or not doc.blocks[0].children or doc.blocks[0].children[0].content != expected_help:
                issues.append("Help text mismatch")
                
            if getattr(doc.metadata, 'category', None) != meta.get("category"):
                issues.append("Category mismatch")
                
            # Parameters
            expected_params = raw_cmd.get("parameters", [])
            flag_tables = [b for b in doc.blocks if getattr(b, 'type', None) == 'flag_table']
            if expected_params and not flag_tables:
                issues.append("Missing parameters block")
            elif expected_params and flag_tables:
                ft = flag_tables[0]
                if len(ft.flags) != len(expected_params):
                    issues.append("Parameter count mismatch")
                else:
                    for i, ep in enumerate(expected_params):
                        if ft.flags[i].name != ep.get("name"):
                            issues.append(f"Parameter ordering mismatch at index {i}")
                            
            # Check metadata arrays
            for list_field in ["examples", "related", "outputs", "consumes", "produces", "prerequisites", "use_cases", "personas", "tags", "gifs", "errors", "notes", "edge_cases", "workflow"]:
                expected = meta.get(list_field, [])
                actual = getattr(doc.metadata, list_field, [])
                if expected != actual:
                    issues.append(f"Metadata field '{list_field}' mismatch. Expected {len(expected)}, got {len(actual)}")
            
            # Check introduced version
            if doc.versioning.introduced_in != meta.get("introduced", "0.1.0"):
                issues.append("Introduced version mismatch")
                
            # Check stability
            if doc.versioning.stability != meta.get("stability", "stable"):
                issues.append("Stability mismatch")
            
            if issues:
                report.append(f"✗ {cmd_name}")
                for issue in issues:
                    report.append(f"    {issue}")
                report.append("")
                failed = True
            else:
                report.append(f"✓ {cmd_name}")
                
        out_file = Path("docs-generated/web/v4/shadow-report.md")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text("\n".join(report), encoding="utf-8")
        
        if failed:
            raise Exception("SHADOW VALIDATION FAILED. See docs-generated/web/v4/shadow-report.md")
            
        print("SHADOW VALIDATION PASSED (100% Semantic Parity)")
