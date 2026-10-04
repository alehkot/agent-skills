#!/usr/bin/env python3
"""Check the tracked, distributable Agent Skills bundle using only the stdlib."""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit



def unfenced_lines(text: str) -> list[tuple[int, str]]:
    """Return numbered Markdown lines outside backtick and tilde fences."""
    result = []
    fence: tuple[str, int] | None = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1] and not tail.strip():
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def markdown_headings(text: str) -> list[tuple[int, int, str, str]]:
    """Return ATX headings with GitHub-style, duplicate-aware fragment IDs."""
    result = []
    used: set[str] = set()
    for number, line in unfenced_lines(text):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        marks, title = match.groups()
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        plain = re.sub(r"<[^>]+>", "", plain).lower()
        base = "".join(
            char
            for char in plain
            if char in "-_ " or unicodedata.category(char)[0] in {"L", "N"}
        ).replace(" ", "-")
        anchor = base
        suffix = 0
        while anchor in used:
            suffix += 1
            anchor = f"{base}-{suffix}"
        used.add(anchor)
        result.append((number, len(marks), title, anchor))
    return result


def markdown_links(text: str) -> list[str]:
    """Read inline link destinations outside fenced examples and inline code."""
    result = []
    for _, line in unfenced_lines(text):
        # Code spans are examples, not resource links.
        line = re.sub(r"(`+)(.*?)\1", lambda m: " " * len(m[0]), line)
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", line):
            target = match[1].strip()
            if target.startswith("<"):
                target = target[1:].split(">", 1)[0]
            else:
                target = target.split(' "', 1)[0].split(" '", 1)[0]
            result.append(target)
    return result


def validate_contents(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if len(text.splitlines()) <= 100:
        return
    headings = markdown_headings(text)
    contents = next((h for h in headings if h[2].casefold() == "contents"), None)
    if contents is None:
        raise ValueError(
            f"{path}: references over 100 lines need a Contents section with linked headings"
        )
    end = next(
        (h[0] for h in headings if h[0] > contents[0]), len(text.splitlines()) + 1
    )
    section = "\n".join(text.splitlines()[contents[0] : end - 1])
    linked = {
        unquote(target[1:])
        for target in markdown_links(section)
        if target.startswith("#")
    }
    expected = {h[3] for h in headings if h[1] > 1 and h != contents}
    missing = expected - linked
    invalid = linked - {h[3] for h in headings}
    if missing or invalid:
        raise ValueError(
            f"{path}: Contents anchors missing={sorted(missing)}, invalid={sorted(invalid)}"
        )


def validate_reference_resources(skill_dir: Path) -> None:
    """Require direct entrypoint links, local targets, valid anchors and long-file indexes."""
    root = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    references = skill_dir / "references"
    paths = sorted(references.rglob("*.md")) if references.is_dir() else []
    for path in paths:
        if path.parent != references:
            raise ValueError(f"{path}: references must stay one level deep")
    linked: set[Path] = set()
    for path in [skill_md, *paths]:
        for target in markdown_links(path.read_text(encoding="utf-8")):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            resolved = (
                (path.parent / unquote(parts.path)).resolve()
                if parts.path
                else path.resolve()
            )
            if not resolved.is_relative_to(root):
                raise ValueError(
                    f"{path}: link {target!r} escapes the standalone skill"
                )
            if not resolved.is_file():
                raise ValueError(f"{path}: broken local link {target!r}")
            if parts.fragment and resolved.suffix == ".md":
                anchors = {
                    h[3]
                    for h in markdown_headings(resolved.read_text(encoding="utf-8"))
                }
                if unquote(parts.fragment) not in anchors:
                    raise ValueError(f"{path}: incorrect anchor in {target!r}")
            if path == skill_md:
                linked.add(resolved)
    for path in paths:
        if path.resolve() not in linked:
            raise ValueError(
                f"{path}: reference file is never linked directly from SKILL.md"
            )
        validate_contents(path)

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
        validate_reference_resources(ROOT / "skills" / name)
    print(f"Validated {len(REFERENCES)} skills and {len(PUBLIC_FILES)} tracked files.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
