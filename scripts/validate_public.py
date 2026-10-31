#!/usr/bin/env python3
"""Check the tracked, distributable Agent Skills bundle using only the stdlib."""

from __future__ import annotations

import json
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
                # Backticks cannot occur in a backtick fence's info string.
                # A same-line code span at column zero is not a fenced block.
                if marker[0] != "`" or "`" not in tail:
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
    """Read the bundle's single-line inline links, excluding code examples.

    Consume complete links before inspecting their titles for backticks. Masking
    code spans over a whole line first can hide real links between two titles.
    This is a deliberately small scanner, not a complete CommonMark parser.
    """
    link = re.compile(
        r'\[[^\]\n]*\]\([ \t]*'
        r'(?:<(?P<angle>[^<>\n]*)>|(?P<bare>[^\s()]*))'
        r'''(?:[ \t]+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\)))?'''
        r'[ \t]*\)'
    )
    result = []
    for _, line in unfenced_lines(text):
        position = 0
        while position < len(line):
            if line[position] == "\\":
                # An escaped opening delimiter is literal text, not code/link.
                position += 2
                continue
            if line[position] == "`":
                end = position + 1
                while end < len(line) and line[end] == "`":
                    end += 1
                closing = re.search(rf"(?<!`)`{{{end - position}}}(?!`)", line[end:])
                position = end + closing.end() if closing else end
                continue
            if line[position] == "[":
                match = link.match(line, position)
                if match:
                    result.append(
                        match["angle"] if match["angle"] is not None else match["bare"]
                    )
                    position = match.end()
                    continue
            position += 1
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
            resolved = validate_local_link(path, target, root)
            if path == skill_md and resolved is not None:
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
    "review-loop": ("blast-radius.md", "review-protocol.md", "verification-recipe.md"),
}
PUBLIC_FILES = frozenset({
    ".woodpecker.yaml", ".ci/check.sh",
    ".gitignore", ".github/workflows/validate.yml", "LICENSE", "README.md",
    "scripts/validate_public.py", "scripts/test_validate_public.py",
    "evals/handoff-recovery.md", "evals/challenge-me-limits.md",
    "evals/review-loop-blast-radius.md", "evals/agent-evals-model-replay.md",
} | {
    f"skills/{name}/{path}"
    for name, references in REFERENCES.items()
    for path in ("SKILL.md", "LICENSE", "agents/openai.yaml",
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


def parse_skill_frontmatter(name: str, text: str) -> str:
    """Decode this repository's small frontmatter subset, not general YAML.

    Folded descriptions are one paragraph of exactly two-space-indented lines.
    JSON-compatible quoted descriptions provide an unambiguous single-line form.
    Recognize the whole header so an ignored key or YAML tail cannot pass checks.
    """
    lines = text.split("\n")
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError(f"{name}: missing YAML frontmatter")
    header = lines[1:lines.index("---", 1)]
    if any(
        (unicodedata.category(char) in {"Cc", "Cs", "Zl", "Zp"})
        or char in "\ufffe\uffff"
        for line in header for char in line
    ):
        raise ValueError(f"{name}: unexpected non-printable character in frontmatter")
    values: dict[str, str] = {}
    index = 0
    while index < len(header):
        line = header[index]
        index += 1
        if not line.strip(" ") or line.startswith("#"):
            continue
        field = re.fullmatch(r"(name|description): (.+)", line)
        if field is None:
            raise ValueError(f"{name}: unsupported frontmatter line {index}")
        key, scalar = field.groups()
        if key in values:
            raise ValueError(f"{name}: duplicate frontmatter field {key}")
        if key == "name":
            if scalar != name:
                raise ValueError(f"{name}: metadata name must match its directory")
            value = scalar
        elif scalar == ">-":
            paragraph = []
            while index < len(header) and header[index].startswith("  "):
                content = header[index][2:]
                if not content or content[0].isspace():
                    raise ValueError(
                        f"{name}: folded description needs nonblank lines "
                        "with exactly two-space indentation"
                    )
                paragraph.append(content)
                index += 1
            value = " ".join(paragraph)
        else:
            if not scalar.startswith('"'):
                raise ValueError(
                    f"{name}: description must use >- or a JSON-quoted string"
                )
            try:
                value = json.loads(scalar)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{name}: invalid quoted description") from exc
        values[key] = value
    if set(values) != {"name", "description"}:
        raise ValueError(f"{name}: expected name and description metadata")
    description = values["description"]
    if not description.strip() or not 1 <= len(description) <= 1024:
        raise ValueError(f"{name}: description must be nonblank text of 1-1024 characters")
    if any(
        unicodedata.category(char) in {"Cc", "Cs", "Zl", "Zp"}
        or char in "\ufffe\uffff"
        for char in description
    ):
        raise ValueError(f"{name}: description must be single-line text without controls")
    return description


def check_skill(name: str) -> None:
    path = ROOT / "skills" / name / "SKILL.md"
    parse_skill_frontmatter(name, path.read_text(encoding="utf-8"))
    metadata = (path.parent / "agents/openai.yaml").read_text(encoding="utf-8")
    check_interface(name, metadata)


def check_license_copies() -> None:
    """Keep the existing notice in each independently distributable skill."""
    expected = (ROOT / "LICENSE").read_bytes()
    for name in REFERENCES:
        path = ROOT / "skills" / name / "LICENSE"
        if path.read_bytes() != expected:
            raise ValueError(f"{path.relative_to(ROOT)}: must match repository LICENSE")


def check_interface(name: str, text: str) -> None:
    """Check this bundle's three-field, JSON-quoted subset of openai.yaml.

    This is intentionally not a general YAML parser. Recognize the whole
    document before checking values so misplaced or duplicate fields cannot
    satisfy the contract accidentally. JSON string syntax is a YAML subset.
    """
    if any(
        (unicodedata.category(char) in {"Cc", "Cs"} and char not in "\t\r\n")
        or char in "\u2028\u2029\ufffe\uffff"
        for char in text
    ):
        raise ValueError(f"{name}: unexpected non-printable character in openai.yaml")
    lines = [
        (number, line)
        for number, line in enumerate(text.splitlines(), 1)
        if line.strip(" \t") and not line.lstrip(" \t").startswith("#")
    ]
    if not lines or lines[0][1] != "interface:":
        raise ValueError(f"{name}: expected an interface mapping in openai.yaml")
    required = {"display_name", "short_description", "default_prompt"}
    values: dict[str, str] = {}
    for number, line in lines[1:]:
        field = re.fullmatch(r'  ([a-z_]+): (".*")', line)
        if field is None or field[1] not in required:
            raise ValueError(
                f"{name}: openai.yaml:{number}: expected a supported interface field "
                "with a single-line JSON-quoted value"
            )
        key, scalar = field.groups()
        if key in values:
            raise ValueError(f"{name}: duplicate interface field {key}")
        try:
            value = json.loads(scalar)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{name}: invalid quoted interface field {key}") from exc
        if not value.strip() or any(
            unicodedata.category(char) in {"Cc", "Cs"} for char in value
        ):
            raise ValueError(f"{name}: interface field {key} must be nonblank text without controls")
        values[key] = value
    missing = required - values.keys()
    if missing:
        raise ValueError(f"{name}: missing interface fields {sorted(missing)}")
    if not re.search(rf"(?<![\w$-])\${re.escape(name)}(?![\w-])", values["default_prompt"]):
        raise ValueError(f"{name}: default prompt must identify its skill as ${name}")


def validate_local_link(path: Path, target: str, boundary: Path) -> Path | None:
    """Validate one destination against the bundle and its document boundary."""
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        return None
    resolved = (
        (path.parent / unquote(parts.path)).resolve()
        if parts.path
        else path.resolve()
    )
    if not resolved.is_relative_to(boundary.resolve()):
        raise ValueError(f"{path}: link leaves its allowed directory: {target!r}")
    relative = resolved.relative_to(ROOT.resolve()).as_posix()
    if relative not in PUBLIC_FILES:
        raise ValueError(f"{path}: link is not in the bundle: {target!r}")
    if not resolved.is_file():
        raise ValueError(f"{path}: broken local link {target!r}")
    if parts.fragment and resolved.suffix == ".md":
        anchors = {
            h[3] for h in markdown_headings(resolved.read_text(encoding="utf-8"))
        }
        if unquote(parts.fragment) not in anchors:
            raise ValueError(f"{path}: incorrect anchor in {target!r}")
    return resolved


def check_links(name: str, text: str) -> None:
    components = PurePosixPath(name).parts
    boundary = (
        ROOT / "skills" / components[1] if components[0] == "skills" else ROOT
    )
    for target in markdown_links(text):
        validate_local_link(ROOT / name, target, boundary)


def main() -> int:
    check_inventory()
    check_license_copies()
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
