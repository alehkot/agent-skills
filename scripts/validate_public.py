#!/usr/bin/env python3
"""Check the tracked, distributable Agent Skills bundle using only the stdlib."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = {
    "agent-evals": (
        "agent-boundaries.md", "coverage.md", "experiments.md",
        "oracles-and-controls.md", "rubric.md",
    ),
    "challenge-me": ("decision-log.md",),
    "handoff": ("prompt-template.md",),
    "make-it-click": ("learning-patterns.md",),
    "review-loop": ("review-protocol.md",),
}
PUBLIC_FILES = frozenset({
    ".gitignore", ".github/workflows/validate.yml", "LICENSE", "README.md",
    "scripts/validate_public.py",
} | {
    f"skills/{name}/{path}"
    for name, references in REFERENCES.items()
    for path in ("SKILL.md", "agents/openai.yaml",
                 *(f"references/{reference}" for reference in references))
})


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def check_inventory() -> None:
    if Path(git("rev-parse", "--show-toplevel").strip()).resolve() != ROOT:
        raise ValueError("Run from a checkout whose root contains this script.")
    entries = {}
    for entry in git("ls-files", "--stage", "-z").split("\0"):
        if not entry:
            continue
        metadata, name = entry.split("\t", 1)
        mode, _object_id, stage = metadata.split()
        if stage != "0" or mode not in {"100644", "100755"}:
            raise ValueError(f"{name}: expected an ordinary tracked file")
        entries[name] = mode
    actual = set(entries)
    if actual != PUBLIC_FILES:
        raise ValueError(
            f"Tracked inventory differs: missing={sorted(PUBLIC_FILES - actual)}; "
            f"unexpected={sorted(actual - PUBLIC_FILES)}"
        )
    for name in PUBLIC_FILES:
        path = ROOT / name
        if not path.is_file() or any(
            parent.is_symlink() for parent in (path, *path.parents) if parent != ROOT
        ):
            raise ValueError(f"{name}: expected an ordinary file without symlinks")


def check_skill(name: str) -> None:
    path = ROOT / "skills" / name / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
    header = match.group(1)
    keys = re.findall(r"^([a-z][a-z_-]*):", header, re.MULTILINE)
    if sorted(keys) != ["description", "name"]:
        raise ValueError(f"{name}: expected only name and description metadata")
    if not re.search(rf"^name: {re.escape(name)}$", header, re.MULTILINE):
        raise ValueError(f"{name}: metadata name must match its directory")
    description = re.search(r"^description: (.+(?:\n[ \t]+.*)*)", header, re.MULTILINE)
    if not description or not description.group(1).replace(">-", "").strip():
        raise ValueError(f"{name}: empty description")
    metadata = (path.parent / "agents/openai.yaml").read_text(encoding="utf-8")
    for key in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf'^  {key}: "[^"\n]+"$', metadata, re.MULTILINE):
            raise ValueError(f"{name}: missing interface field {key}")
    if f"${name}" not in metadata:
        raise ValueError(f"{name}: default prompt must identify its skill")


def check_links(name: str, text: str) -> None:
    for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
        target = target.strip("<>")
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        path = (ROOT / name).parent / unquote(parts.path)
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            raise ValueError(f"{name}: link leaves the bundle: {target}") from None
        if relative not in PUBLIC_FILES:
            raise ValueError(f"{name}: link is not in the bundle: {target}")
        components = PurePosixPath(name).parts
        if components[0] == "skills":
            skill_root = (ROOT / "skills" / components[1]).resolve()
            if not resolved.is_relative_to(skill_root):
                raise ValueError(f"{name}: skill link leaves its directory: {target}")


def main() -> int:
    check_inventory()
    for name in sorted(PUBLIC_FILES):
        text = (ROOT / name).read_text(encoding="utf-8")
        if "\0" in text:
            raise ValueError(f"{name}: unexpected binary content")
        if name.endswith(".md"):
            check_links(name, text)
    for name in REFERENCES:
        check_skill(name)
    print(f"Validated {len(REFERENCES)} skills and {len(PUBLIC_FILES)} tracked files.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
