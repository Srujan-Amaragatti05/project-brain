import pytest
from project_brain.docs.v4 import (
    TextNode, ParagraphBlock, CommandDocument, CommandMetadata, VersioningInfo,
    Manifest, ManifestBuildMetadata, ManifestStatistics, ManifestIntegrity,
    ManifestCapabilities, ManifestEndpoints, NavNode, NavigationRegistry,
    Asset, AssetRegistry, DocumentRegistryEntry, DocumentRegistry,
    SearchEntry, HeadingEntry, SearchIndex
)

def test_inline_nodes():
    node = TextNode(content="Hello world")
    assert node.type == "text"
    assert node.content == "Hello world"

def test_blocks():
    para = ParagraphBlock(
        block_id="blk_123",
        children=[TextNode(content="Hello world")]
    )
    assert para.type == "paragraph"
    assert para.block_id == "blk_123"
    assert len(para.children) == 1

def test_documents():
    doc = CommandDocument(
        id="urn:brain:doc:123",
        slug="cli/init",
        aliases=["init"],
        title="Init",
        summary="Initialize",
        locale="en",
        versioning=VersioningInfo(
            introduced_in="1.0",
            stability="stable"
        ),
        blocks=[],
        metadata=CommandMetadata(
            command_name="init",
            category="cli",
            is_plugin=False
        )
    )
    assert doc.type == "command"
    assert doc.metadata.command_name == "init"

def test_manifest():
    manifest = Manifest(
        build_id="build_123",
        build_metadata=ManifestBuildMetadata(
            generated_at="2026",
            generator_version="1.0",
            cli_version="1.0",
            git_commit="abc",
            build_duration_ms=100
        ),
        statistics=ManifestStatistics(total_documents=1, total_assets=1),
        integrity=ManifestIntegrity(documents="a", navigation="b", assets="c", search="d"),
        capabilities=ManifestCapabilities(
            supported_document_types=["command"],
            supported_block_types=["paragraph"],
            supported_inline_types=["text"],
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
    assert manifest.schema_version == "4.0.0"
