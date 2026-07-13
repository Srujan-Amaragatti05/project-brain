import json
from pathlib import Path

def run_checks():
    out_dir = Path("docs-generated/web/v4")
    
    # Task 2
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    documents = json.loads((out_dir / "documents.json").read_text(encoding="utf-8"))["documents"]
    navigation = json.loads((out_dir / "navigation.json").read_text(encoding="utf-8"))
    assets = json.loads((out_dir / "assets.json").read_text(encoding="utf-8"))["assets"]
    search = json.loads((out_dir / "search-index.json").read_text(encoding="utf-8"))
    
    doc_ids = set()
    slugs = set()
    for d in documents:
        if d["id"] in doc_ids: raise Exception(f"Duplicate doc ID: {d['id']}")
        if d["slug"] in slugs: raise Exception(f"Duplicate slug: {d['slug']}")
        doc_ids.add(d["id"])
        slugs.add(d["slug"])
        
    for d in documents:
        # Check content files
        content_path = out_dir / "content" / f"{d['id'].split(':')[-1]}.json"
        if not content_path.exists():
            raise Exception(f"Missing content file: {content_path}")
            
    # Task 3
    for a_id, asset in assets.items():
        if not a_id.startswith("urn:brain:asset:"):
            raise Exception(f"Invalid asset ID: {a_id}")
        physical_path = Path("demo/gifs") / asset["storage_key"]
        if not physical_path.exists():
            raise Exception(f"Missing physical asset: {physical_path}")
            
    # Task 4
    def walk_nav(nodes):
        for n in nodes:
            if n.get("target_id") and n["target_id"] not in doc_ids:
                raise Exception(f"Dead link in nav: {n['target_id']}")
            if n.get("children"):
                walk_nav(n["children"])
    walk_nav(navigation["sidebar"])
    
    # Task 5
    for s_id, s_data in search.get("documents", {}).items():
        if s_id not in doc_ids:
            raise Exception(f"Search index points to dead doc: {s_id}")
            
    print("ALL VALIDATIONS PASSED")
    
if __name__ == "__main__":
    run_checks()
