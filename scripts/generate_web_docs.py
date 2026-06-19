from __future__ import annotations

import copy
from datetime import UTC, datetime
import json
import re
import shutil
from pathlib import Path

from lib.atomic_write import safe_write

# Paths
INPUT_COMMANDS = Path("docs-generated/metadata/commands.json")
INPUT_SIDEBAR = Path("docs-generated/metadata/sidebar.json")
INPUT_SEARCH = Path("docs-generated/metadata/search-index.json")
OUTPUT_WEB_DIR = Path("docs-generated/web")
VERSION_FILE = Path("src/project_brain/__init__.py")

# Assets
GIF_SOURCE_DIR = Path("demo/gifs")
GIF_OUTPUT_DIR = OUTPUT_WEB_DIR / "gifs"


def get_version() -> str:
    """Attempt to load version from source code or fallback to unknown."""
    if not VERSION_FILE.exists():
        return "unknown"
    content = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else "unknown"


def main():
    if not (INPUT_COMMANDS.exists() and INPUT_SIDEBAR.exists() and INPUT_SEARCH.exists()):
        print("[ERROR] Required metadata files missing. Run generate_metadata.py first.")
        raise SystemExit(1)

    OUTPUT_WEB_DIR.mkdir(parents=True, exist_ok=True)
    GIF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    commands_raw = json.loads(INPUT_COMMANDS.read_text(encoding="utf-8"))["commands"]
    sidebar_raw = json.loads(INPUT_SIDEBAR.read_text(encoding="utf-8"))
    search_index = json.loads(INPUT_SEARCH.read_text(encoding="utf-8"))

    # 4. Validate duplicate command titles in commands.json
    all_cmd_names = set()
    for cmd in commands_raw:
        name = cmd["command"]
        if name in all_cmd_names:
            print(f"[ERROR] Duplicate command name detected in commands.json: {name}")
            raise SystemExit(1)
        all_cmd_names.add(name)

    # Asset Handling: GIFs
    referenced_gifs = set()
    for cmd in commands_raw:
        gifs = cmd.get("metadata", {}).get("gifs", [])
        for gif in gifs:
            referenced_gifs.add(gif)

    for gif_name in referenced_gifs:
        src_path = GIF_SOURCE_DIR / gif_name
        dest_path = GIF_OUTPUT_DIR / gif_name

        if not src_path.exists():
            print(f"[ERROR] GIF asset referenced in metadata does not exist: {src_path}")
            raise SystemExit(1)
        
        # Copy asset
        try:
            shutil.copy2(src_path, dest_path)
        except Exception as e:
            print(f"[ERROR] Failed to copy GIF {gif_name}: {e}")
            raise SystemExit(1)

    # 3. Optimization: Command Map for O(1) lookups
    commands_map = {cmd["command"]: cmd for cmd in commands_raw}

    # 1. Validate sidebar.json structure
    if not isinstance(sidebar_raw, dict):
        print("[ERROR] sidebar.json must be a dictionary")
        raise SystemExit(1)

    flat_order = []
    seen_routes = set()

    for category, items in sidebar_raw.items():
        if not isinstance(items, list):
            print(f"[ERROR] Sidebar category '{category}' must be a list of items")
            raise SystemExit(1)

        for item in items:
            if not isinstance(item, dict):
                print(f"[ERROR] Sidebar entry in '{category}' must be a dictionary")
                raise SystemExit(1)
            
            if "title" not in item or "slug" not in item:
                print(f"[ERROR] Sidebar entry in '{category}' missing 'title' or 'slug'")
                raise SystemExit(1)

            title = item["title"]
            slug_raw = item["slug"]

            # 2. Validate command references: sidebar titles must exist in commands.json
            if title not in commands_map:
                print(f"[ERROR] Sidebar entry '{title}' references a command not found in commands.json")
                raise SystemExit(1)

            # Determine category and command slugs
            parts = slug_raw.split("/")
            if len(parts) == 2:
                cat_slug = parts[0]
                cmd_slug = parts[1]
            else:
                cat_slug = category.lower().replace(" ", "_")
                cmd_slug = slug_raw

            # 3. Validate duplicate routes (category, slug)
            route_key = (cat_slug, cmd_slug)
            if route_key in seen_routes:
                print(f"[ERROR] Duplicate route detected: {cat_slug}/{cmd_slug}")
                raise SystemExit(1)
            seen_routes.add(route_key)

            flat_order.append(
                {
                    "title": title,
                    "category": cat_slug,
                    "slug": cmd_slug,
                }
            )

    # 2. Build Web Content Map (Non-mutating via deepcopy)
    web_docs = {}
    for i, entry in enumerate(flat_order):
        original_cmd = commands_map[entry["title"]]
        cmd_data = copy.deepcopy(original_cmd)

        # Add Navigation Links (Prev/Next)
        cmd_data["navigation"] = {
            "prev": flat_order[i - 1] if i > 0 else None,
            "next": flat_order[i + 1] if i < len(flat_order) - 1 else None,
        }

        cat = entry["category"]
        slug = entry["slug"]

        if cat not in web_docs:
            web_docs[cat] = {}
        web_docs[cat][slug] = cmd_data

    # 5. Dynamic Version Generation
    version_data = {
        "version": get_version(),
        "generated_at": datetime.now(UTC).isoformat() + "Z",
        "command_count": len(commands_raw),
    }

    # Write Bundle (Preserving existing output schema)
    success = True
    if not safe_write(
        OUTPUT_WEB_DIR / "docs.json",
        json.dumps(web_docs, indent=2)
    ):
        success = False

    if not safe_write(
        OUTPUT_WEB_DIR / "sidebar.json",
        json.dumps(sidebar_raw, indent=2)
    ):
        success = False

    if not safe_write(
        OUTPUT_WEB_DIR / "search-index.json",
        json.dumps(search_index, indent=2)
    ):
        success = False

    if not safe_write(
        OUTPUT_WEB_DIR / "version.json",
        json.dumps(version_data, indent=2)
    ):
        success = False

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
