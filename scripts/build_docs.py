from __future__ import annotations

import subprocess
import sys

SCRIPTS = [
    "scripts/generate_cli_docs.py",
    "scripts/generate_metadata.py",

    "scripts/generate_handbook.py",
    "scripts/generate_error_handbook.py",
    "scripts/generate_provider_docs.py",
    "scripts/generate_config_docs.py",

    "scripts/generate_workflows.py",

    "scripts/generate_relationships.py",
    "scripts/generate_personas.py",
    "scripts/generate_architecture_docs.py",
    "scripts/generate_use_cases.py",
    "scripts/generate_command_matrix.py",
    "scripts/generate_dataflow_docs.py",
    "scripts/generate_lifecycle_docs.py",
    "scripts/generate_workflow_graph.py",

    "scripts/generate_web_docs.py",

    "scripts/check_coverage.py",
    "scripts/check_metadata.py",
    "scripts/check_relationships.py",
    "scripts/check_metadata_drift.py",
    "scripts/generate_readme.py",
    "scripts/validate_docs.py",
    "scripts/verify_artifacts.py",
]

import argparse
from pathlib import Path

# Legacy V1 Scripts
SCRIPTS = [
    "scripts/generate_cli_docs.py",
    "scripts/generate_metadata.py",
    "scripts/generate_handbook.py",
    "scripts/generate_error_handbook.py",
    "scripts/generate_provider_docs.py",
    "scripts/generate_config_docs.py",
    "scripts/generate_workflows.py",
    "scripts/generate_relationships.py",
    "scripts/generate_personas.py",
    "scripts/generate_architecture_docs.py",
    "scripts/generate_use_cases.py",
    "scripts/generate_command_matrix.py",
    "scripts/generate_dataflow_docs.py",
    "scripts/generate_lifecycle_docs.py",
    "scripts/generate_workflow_graph.py",
    "scripts/generate_web_docs.py",
    "scripts/check_coverage.py",
    "scripts/check_metadata.py",
    "scripts/check_relationships.py",
    "scripts/check_metadata_drift.py",
    "scripts/generate_readme.py",
    "scripts/validate_docs.py",
    "scripts/verify_artifacts.py",
]

def run_legacy(ignore_errors=False):
    for script in SCRIPTS:
        print(f"\nRunning Legacy: {script}")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0 and not ignore_errors:
            raise SystemExit(result.returncode)

def run_v4():
    print("\nRunning V4 Compiler Pipeline...")
    try:
        from project_brain.docs.compiler.pipeline import CompilerPipeline
        from project_brain.docs.compiler.collectors import LegacyCollectorStage
        from project_brain.docs.compiler.ast_builder import LegacyASTBuilderStage
        from project_brain.docs.compiler.nav_builder import LegacyNavBuilderStage
        from project_brain.docs.compiler.search_builder import LegacySearchBuilderStage
        from project_brain.docs.compiler.linker import BaseLinker
        from project_brain.docs.compiler.asset_resolver import BaseAssetResolver
        from project_brain.docs.compiler.validator import BaseValidator
        from project_brain.docs.compiler.publisher import BasePublisher
        
        from project_brain.docs.compiler.registry_builder import RegistryBuilderStage
        from project_brain.docs.compiler.manifest_builder import ManifestBuilderStage
        
        # Build the pipeline
        pipeline = CompilerPipeline()
        
        # 1. Collectors
        pipeline.collectors.append(LegacyCollectorStage())
        
        # 2. AST Builders
        pipeline.ast_builders.append(LegacyASTBuilderStage())
        
        # 3. Linkers
        pipeline.linkers.append(BaseLinker())
        
        # 4. Assets
        pipeline.asset_resolvers.append(BaseAssetResolver())
        
        # 5. Nav & Search
        pipeline.nav_builders.append(LegacyNavBuilderStage())
        pipeline.search_builders.append(LegacySearchBuilderStage())
        
        # 5.5 Registry and Manifest
        from project_brain.docs.compiler.pipeline import NavigationBuilderStage
        # HACK: attach these to validators since there's no native stage slot for Registry/Manifest yet,
        # or actually create proper slots in pipeline.py.
        # But wait, I'll just add them as Validators since they execute right before publisher.
        class Wrapper(BaseValidator):
            def execute(self, ctx):
                RegistryBuilderStage().execute(ctx)
                ManifestBuilderStage().execute(ctx)
                
        # 6. Validators
        pipeline.validators.append(Wrapper())
        pipeline.validators.append(BaseValidator())
        from project_brain.docs.compiler.shadow_validator import SemanticShadowValidatorStage
        pipeline.validators.append(SemanticShadowValidatorStage())
        
        # 7. Publishers
        pipeline.publishers.append(BasePublisher("docs-generated/web/v4"))
        
        # Run
        pipeline.run()
        print("\nV4 Compiler Pipeline completed.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy", action="store_true")
    parser.add_argument("--v4", action="store_true")
    parser.add_argument("--shadow", action="store_true")
    args = parser.parse_args()

    if args.shadow:
        args.legacy = True
        args.v4 = True
        
    if not args.legacy and not args.v4:
        # Default to legacy if nothing specified for backwards compatibility
        args.legacy = True

    if args.legacy:
        run_legacy(ignore_errors=args.shadow)
        
    if args.v4:
        run_v4()
        
    print("\nDocumentation build completed.")

if __name__ == "__main__":
    main()
