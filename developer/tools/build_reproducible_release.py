#!/usr/bin/env python3
from __future__ import annotations
import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import _ALLOWED_WRITE_ROOTS, safe_write_path

# Release archives are documented to be written under releases/ (see
# RELEASE_WORKFLOW.md), so that root is allowed in addition to the defaults.
_RELEASE_WRITE_ROOTS = _ALLOWED_WRITE_ROOTS + [Path("releases")]


_DEFAULT_EXCLUDES = [
    ".git",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "*.DS_Store",
    "node_modules",
]


def _load_gitignore_patterns(root: Path) -> list[str]:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return []
    patterns = []
    for line in gitignore.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line.rstrip("/"))
    return patterns


def _is_excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    parts = path.relative_to(root).parts
    # Always skip .git directory
    if ".git" in parts:
        return True
    rel_str = str(path.relative_to(root))
    name = path.name
    for pattern in patterns:
        # Match against the filename alone
        if fnmatch.fnmatch(name, pattern):
            return True
        # Match against the relative path
        if fnmatch.fnmatch(rel_str, pattern):
            return True
        # Match against any path component
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False


def build_release(root_path: str, output_path: str, extra_excludes: list[str] | None = None) -> dict:
    root = Path(root_path).resolve()
    gitignore_patterns = _load_gitignore_patterns(root)
    all_patterns = _DEFAULT_EXCLUDES + gitignore_patterns + (extra_excludes or [])

    included: list[str] = []
    excluded: list[str] = []

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            if _is_excluded(p, root, all_patterns):
                excluded.append(str(p.relative_to(root)))
                continue
            arcname = str(p.relative_to(root))
            zf.write(p, arcname)
            included.append(arcname)

    return {
        "output": output_path,
        "included_count": len(included),
        "excluded_count": len(excluded),
        "included_files": included,
        "excluded_files": excluded,
        "gitignore_patterns_applied": gitignore_patterns,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build sorted deterministic release zip")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--output", required=True, help="Output zip file path")
    parser.add_argument("--exclude", action="append", default=[], metavar="PATTERN",
                        help="Additional glob patterns to exclude (repeatable)")
    args = parser.parse_args()

    # FILE-01: the CLI-supplied output path must stay inside the allowed roots
    try:
        validated_output = safe_write_path(args.output, allowed_roots=_RELEASE_WRITE_ROOTS)
    except ValueError:
        print(f"Error: output path outside allowed write roots: {args.output}")
        sys.exit(1)
    result = build_release(args.root, str(validated_output), args.exclude)
    print(f"Built {args.output}: {result['included_count']} files included, "
          f"{result['excluded_count']} excluded")


if __name__ == "__main__":
    main()
