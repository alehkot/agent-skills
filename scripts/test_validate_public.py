#!/usr/bin/env python3
"""Regression tests for the bundle checker; Python stdlib and Git only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_public as validator


class MarkdownLinksTests(unittest.TestCase):
    def test_quoted_titles_and_angle_destinations(self) -> None:
        text = (
            '[One](one.md "A title") [Two](two.md \'Another title\')\n'
            '[Three](<three words.md> "Title") [Four](four.md#section)'
        )
        self.assertEqual(
            validator.markdown_links(text),
            ["one.md", "two.md", "three words.md", "four.md#section"],
        )

    def test_titles_can_contain_backticks_and_parentheses(self) -> None:
        text = (
            '[One](one.md "Use `one`") [Two](two.md "Use `two`")\n'
            '[Three](three.md "A \\`") [Four](four.md "A \\`")\n'
            '[Five](five.md "A (title)") [Six](six.md (Title))'
        )
        self.assertEqual(
            validator.markdown_links(text),
            ["one.md", "two.md", "three.md", "four.md", "five.md", "six.md"],
        )

    def test_title_separator_accepts_tabs_and_multiple_spaces(self) -> None:
        for separator in (" ", "   ", "\t", " \t "):
            with self.subTest(separator=separator):
                self.assertEqual(
                    validator.markdown_links(f'[One](one.md{separator}"Title")'),
                    ["one.md"],
                )

    def test_escaped_opening_backtick_does_not_hide_live_link(self) -> None:
        self.assertEqual(
            validator.markdown_links(r'\` [Actual](actual.md) `'),
            ["actual.md"],
        )
        self.assertEqual(validator.markdown_links(r'`\` [Actual](actual.md)'), ["actual.md"])

    def test_same_line_triple_backticks_are_not_a_fence(self) -> None:
        text = '```[Example](missing.md)``` [Actual](actual.md)\n[Next](next.md)'
        self.assertEqual(validator.markdown_links(text), ["actual.md", "next.md"])

    def test_code_spans_do_not_hide_adjacent_live_links(self) -> None:
        text = '`[Example](missing.md)` [Actual](actual.md)'
        self.assertEqual(validator.markdown_links(text), ["actual.md"])

    def test_code_span_delimiters_must_have_equal_lengths(self) -> None:
        cases = {
            '``[Example](missing.md)`` [Actual](actual.md)': ["actual.md"],
            '``a ` [Example](missing.md)``': [],
            '`a `` [Example](missing.md)`': [],
            '``unclosed [Actual](actual.md)`': ["actual.md"],
            '`unclosed [Actual](actual.md)``': ["actual.md"],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(validator.markdown_links(text), expected)

    def test_backtick_and_tilde_fences_are_examples(self) -> None:
        for marker in ("```", "~~~~"):
            with self.subTest(marker=marker):
                text = (
                    f'{marker}markdown\n[Example](missing.md)\n{marker}\n'
                    '[Actual](actual.md)'
                )
                self.assertEqual(validator.markdown_links(text), ["actual.md"])

    def test_shorter_or_different_fence_does_not_end_example(self) -> None:
        text = (
            '````markdown\n```\n[Example](missing.md)\n~~~\n'
            '[Also example](missing.md)\n````\n[Actual](actual.md)'
        )
        self.assertEqual(validator.markdown_links(text), ["actual.md"])


class LinkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.files = {
            "README.md": "# Bundle\n## Local\n",
            "skills/example/SKILL.md": (
                '# Example\n[Guide](references/guide.md "Read the guide")\n'
                '[Space](<references/with space.md>)\n'
            ),
            "skills/example/references/guide.md": (
                '# Guide\n## Real heading\n## Real heading\n## Café\n'
                '```md\n## Not a heading\n```\n'
            ),
            "skills/example/references/with space.md": "# Space\n",
            "skills/other/SKILL.md": "# Other\n",
        }
        for name, content in self.files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        self.addCleanup(patch.stopall)
        patch.object(validator, "ROOT", self.root).start()
        patch.object(validator, "PUBLIC_FILES", frozenset(self.files)).start()
        self.skill = "skills/example/SKILL.md"

    def test_titled_untracked_dependency_is_rejected(self) -> None:
        (self.root / "skills/example/references/extra.md").write_text("# Extra\n")
        for destination in (
            'references/extra.md "Extra"',
            "references/extra.md 'Extra'",
            '<references/extra.md> "Extra"',
            "references/extra.md",
        ):
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(ValueError, "not in the bundle"):
                    validator.check_links(self.skill, f"[Extra]({destination})")

    def test_readme_titled_untracked_dependency_is_rejected(self) -> None:
        (self.root / "extra.md").write_text("# Extra\n")
        with self.assertRaisesRegex(ValueError, "not in the bundle"):
            validator.check_links("README.md", '[Extra](extra.md "Extra")')

    def test_readme_cross_file_fragment_is_checked(self) -> None:
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            validator.check_links(
                "README.md", "[Guide](skills/example/references/guide.md#missing)"
            )

    def test_readme_same_file_fragment_is_checked(self) -> None:
        validator.check_links("README.md", "[Here](#local)")
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            validator.check_links("README.md", "[Missing](#missing)")

    def test_supported_fragments_and_percent_decoding(self) -> None:
        for fragment in ("real-heading", "real-heading-1", "caf%C3%A9"):
            with self.subTest(fragment=fragment):
                validator.check_links(
                    "README.md",
                    f'[Guide](skills/example/references/guide.md#{fragment} "Guide")',
                )
        validator.check_links(self.skill, "[Space](references/with%20space.md)")
        validator.check_links(self.skill, '[Space](<references/with space.md> "Space")')

    def test_fenced_heading_is_not_a_valid_fragment(self) -> None:
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            validator.check_links(
                self.skill, "[Example](references/guide.md#not-a-heading)"
            )

    def test_live_broken_link_next_to_code_is_rejected(self) -> None:
        for code in (
            '`[Example](fiction.md)`',
            '``[Example](fiction.md)``',
            '```md\n[Example](fiction.md)\n```\n',
            '~~~md\n[Example](fiction.md)\n~~~\n',
        ):
            with self.subTest(code=code):
                validator.check_links("README.md", code)
                with self.assertRaisesRegex(ValueError, "not in the bundle"):
                    validator.check_links("README.md", code + " [Live](missing.md)")

    def test_standalone_skill_boundary_remains_enforced(self) -> None:
        for destination in (
            '../other/SKILL.md "Other"',
            '../%6Fther/SKILL.md "Other"',
            '../../README.md "Bundle"',
        ):
            with self.subTest(destination=destination):
                with self.assertRaises(ValueError):
                    validator.check_links(self.skill, f"[Outside]({destination})")

    def test_bundle_escape_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validator.check_links("README.md", '[Outside](../outside.md "Outside")')

    def test_allowlisted_but_missing_file_is_rejected(self) -> None:
        (self.root / "skills/example/references/guide.md").unlink()
        with self.assertRaises(ValueError):
            validator.check_links(self.skill, "[Guide](references/guide.md)")

    def test_external_destinations_are_not_local_dependencies(self) -> None:
        for destination in (
            "https://example.org/missing.md#missing",
            "//example.org/missing.md",
            "mailto:person@example.org",
        ):
            with self.subTest(destination=destination):
                validator.check_links("README.md", f'[External]({destination} "Title")')

    def test_reference_validation_uses_the_same_bundle_policy(self) -> None:
        validator.validate_reference_resources(self.root / "skills/example")
        extra = self.root / "skills/example/references/extra.md"
        extra.write_text("# Extra\n")
        with (self.root / self.skill).open("a") as stream:
            stream.write('\n[Extra](references/extra.md "Extra")\n')
        with self.assertRaisesRegex(ValueError, "not in the bundle"):
            validator.validate_reference_resources(self.root / "skills/example")

    def test_code_example_does_not_count_as_direct_reference(self) -> None:
        (self.root / self.skill).write_text(
            '# Example\n`[Guide](references/guide.md)`\n'
            '[Space](<references/with space.md>)\n'
        )
        with self.assertRaisesRegex(ValueError, "never linked directly"):
            validator.validate_reference_resources(self.root / "skills/example")

    def test_reference_fragment_is_checked(self) -> None:
        guide = self.root / "skills/example/references/guide.md"
        with guide.open("a", encoding="utf-8") as stream:
            stream.write('\n[Missing](#missing "Section")\n')
        with self.assertRaisesRegex(ValueError, "incorrect anchor"):
            validator.validate_reference_resources(self.root / "skills/example")

    def test_long_reference_still_requires_complete_contents(self) -> None:
        guide = self.root / "skills/example/references/guide.md"
        text = '# Guide\n\n## Details\n' + 'Explanation.\n' * 100
        guide.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "need a Contents section"):
            validator.validate_reference_resources(self.root / "skills/example")
        guide.write_text(
            '# Guide\n\n## Contents\n\n[Details](#details "Read details")\n\n'
            '## Details\n' + 'Explanation.\n' * 100,
            encoding="utf-8",
        )
        validator.validate_reference_resources(self.root / "skills/example")



class InterfaceMetadataTests(unittest.TestCase):
    """Exercise metadata through check_skill, including its file-reading path."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/handoff"
        (self.skill / "agents").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: handoff\ndescription: Prepare a continuation prompt.\n---\n",
            encoding="utf-8",
        )
        self.metadata = self.skill / "agents/openai.yaml"
        self.fields = {
            "display_name": "Handoff",
            "short_description": "Continue with fresh context",
            "default_prompt": "Use $handoff to continue.",
        }
        patcher = patch.object(validator, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def document(self, **overrides: str) -> str:
        fields = self.fields | overrides
        return "interface:\n" + "".join(
            f"  {key}: {json.dumps(value, ensure_ascii=False)}\n"
            for key, value in fields.items()
        )

    def check(self, text: str) -> None:
        self.metadata.write_text(text, encoding="utf-8")
        validator.check_skill("handoff")

    def test_canonical_interface_passes(self) -> None:
        self.check(self.document())

    def test_all_published_interfaces_pass(self) -> None:
        source = Path(__file__).resolve().parents[1]
        for name in validator.REFERENCES:
            with self.subTest(skill=name), patch.object(validator, "ROOT", source):
                validator.check_skill(name)

    def test_missing_wrong_or_duplicate_root_fails(self) -> None:
        text = self.document()
        for mutant in (
            text.removeprefix("interface:\n"),
            text.replace("interface:", "other:"),
            "interface: {}\n" + text.removeprefix("interface:\n"),
            text + "interface:\n",
            " interface:\n" + text.removeprefix("interface:\n"),
            "---\n" + text,
            text + "...\n",
        ):
            with self.subTest(text=mutant), self.assertRaises(ValueError):
                self.check(mutant)

    def test_duplicate_fields_fail_even_when_values_agree(self) -> None:
        for key, value in self.fields.items():
            for duplicate in (value, "Unrelated text"):
                with self.subTest(key=key, value=duplicate), self.assertRaises(ValueError):
                    self.check(self.document() + f"  {key}: {json.dumps(duplicate)}\n")

    def test_missing_fields_fail(self) -> None:
        for key in self.fields:
            text = "\n".join(
                line for line in self.document().splitlines()
                if not line.startswith(f"  {key}:")
            )
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(text)

    def test_unknown_fields_and_nested_blocks_fail(self) -> None:
        for extra in (
            '  unexpected: "Value"\n',
            'policy:\n  default_prompt: "Use $handoff"\n',
            '  nested:\n    default_prompt: "Use $handoff"\n',
        ):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.check(self.document() + extra)

    def test_wrong_field_token_does_not_satisfy_default_prompt(self) -> None:
        for key in ("display_name", "short_description"):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "default prompt"):
                self.check(self.document(**{key: "$handoff", "default_prompt": "Continue."}))

    def test_comment_token_does_not_satisfy_default_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "default prompt"):
            self.check(self.document(default_prompt="Continue.") + "# Use $handoff\n")

    def test_longer_skill_name_or_embedded_token_fails(self) -> None:
        for token in ("$handoff-other", "$handoff2", "$handoff_other", "x$handoff", "$$handoff"):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, "default prompt"):
                self.check(self.document(default_prompt=f"Use {token}."))

    def test_exact_skill_token_with_punctuation_passes(self) -> None:
        for token in ("$handoff", "($handoff)", "`$handoff`", '"$handoff"', "$handoff."):
            with self.subTest(token=token):
                self.check(self.document(default_prompt=token))

    def test_escaped_quotes_backslashes_and_unicode_pass(self) -> None:
        self.check(self.document(display_name='Handoff "notes" \\ café 🔎'))
        # The check uses the decoded value, not its source spelling.
        self.check(self.document().replace("$handoff", r"\u0024handoff"))

    def test_invalid_escapes_quotes_and_trailing_data_fail(self) -> None:
        for value in (r'"Bad\q"', '"Unclosed', '"One" "Two"', '"Bad "quotes""', 'true', 'null', '["text"]'):
            text = self.document().replace('"Handoff"', value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(text)

    def test_empty_whitespace_controls_and_lone_surrogates_fail(self) -> None:
        for key in self.fields:
            for value in ("", "   ", "\t", "Text\nLine", "Text\x00", "Text\x7f", "Text\ud800"):
                fields = self.fields | {key: value}
                text = "interface:\n" + "".join(
                    f"  {k}: {json.dumps(v)}\n" for k, v in fields.items()
                )
                with self.subTest(key=key, value=repr(value)), self.assertRaises(ValueError):
                    self.check(text)

    def test_raw_controls_cannot_hide_in_comments_or_line_breaks(self) -> None:
        for text in (
            self.document() + "# ignored\x00comment\n",
            self.document(display_name="Not YAML-printable \ufffe"),
            self.document() + "# ignored\uffffcomment\n",
            self.document() + "# ignored\u2028fragment\n",
            self.document() + "# ignored\u2029fragment\n",
            self.document().replace("interface:\n", "interface:\x0c"),
        ):
            with self.subTest(text=repr(text)), self.assertRaises(ValueError):
                self.check(text)

    def test_field_order_comments_and_blank_lines_pass(self) -> None:
        self.check(
            "# metadata\n\ninterface:\n\n  # prompt first\n"
            + "".join(
                f"  {key}: {json.dumps(value)}\n"
                for key, value in reversed(list(self.fields.items()))
            )
            + "\n# end\n"
        )

    def test_non_yaml_whitespace_is_not_ignored_as_blank_or_comment(self) -> None:
        for prefix in ("\u00a0# comment\n", "\u00a0\n", "\u3000# comment\n"):
            with self.subTest(prefix=repr(prefix)), self.assertRaises(ValueError):
                self.check(prefix + self.document())

    def test_unsupported_indentation_or_single_quotes_fail(self) -> None:
        for text in (
            self.document().replace("  display_name:", "    display_name:"),
            self.document().replace("  display_name:", "\tdisplay_name:"),
            self.document().replace('"Handoff"', "'Handoff'"),
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.check(text)


class BundleIntegrationTests(unittest.TestCase):
    """Exercise the command on real tracked files in an isolated checkout."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = Path(__file__).resolve().parents[1]
        for name in validator.PUBLIC_FILES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        # Copy the tested implementation, including when testing an older baseline.
        shutil.copyfile(validator.__file__, self.root / "scripts/validate_public.py")
        self.git("init", "-q")
        self.git("add", ".")

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True, capture_output=True, text=True, timeout=10,
        )

    def validate(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/validate_public.py")],
            cwd=self.root, capture_output=True, text=True, timeout=10,
        )

    def append(self, name: str, text: str) -> None:
        with (self.root / name).open("a", encoding="utf-8") as stream:
            stream.write("\n" + text + "\n")

    def test_clean_checkout_passes(self) -> None:
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated 5 skills", result.stdout)

    def test_standalone_skill_copies_retain_license(self) -> None:
        expected = (self.root / "LICENSE").read_bytes()
        with tempfile.TemporaryDirectory() as destination:
            for name in validator.REFERENCES:
                with self.subTest(skill=name):
                    installed = Path(destination) / name
                    shutil.copytree(self.root / "skills" / name, installed)
                    self.assertTrue((installed / "SKILL.md").is_file())
                    self.assertEqual((installed / "LICENSE").read_bytes(), expected)
            self.assertFalse((Path(destination) / "LICENSE").exists())

    def test_changed_or_empty_skill_license_fails(self) -> None:
        expected = (self.root / "LICENSE").read_bytes()
        for name in validator.REFERENCES:
            path = self.root / "skills" / name / "LICENSE"
            for content in (b"MIT License\n", b""):
                with self.subTest(skill=name, content=content):
                    path.write_bytes(content)
                    result = self.validate()
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn(f"skills/{name}/LICENSE", result.stderr)
                    self.assertIn("must match repository LICENSE", result.stderr)
            path.write_bytes(expected)

    def test_missing_skill_license_fails(self) -> None:
        expected = (self.root / "LICENSE").read_bytes()
        for name in validator.REFERENCES:
            with self.subTest(skill=name):
                path = self.root / "skills" / name / "LICENSE"
                path.unlink()
                result = self.validate()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(f"skills/{name}/LICENSE", result.stderr)
                path.write_bytes(expected)

    def test_skill_license_must_be_tracked(self) -> None:
        for name in validator.REFERENCES:
            with self.subTest(skill=name):
                path = f"skills/{name}/LICENSE"
                self.git("rm", "--cached", path)
                result = self.validate()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("Tracked inventory differs", result.stderr)
                self.assertIn(path, result.stderr)
                self.git("add", path)

    def test_root_license_update_requires_resynchronizing_copies(self) -> None:
        path = self.root / "LICENSE"
        updated = path.read_bytes() + b"\n"
        path.write_bytes(updated)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("must match repository LICENSE", result.stderr)
        for name in validator.REFERENCES:
            (self.root / "skills" / name / "LICENSE").write_bytes(updated)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_verification_recipe_must_be_in_tracked_bundle(self) -> None:
        self.git("rm", "--cached", "skills/review-loop/references/verification-recipe.md")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Tracked inventory differs", result.stderr)
        self.assertIn("skills/review-loop/references/verification-recipe.md", result.stderr)

    def test_verification_recipe_requires_direct_entrypoint_link(self) -> None:
        path = self.root / "skills/review-loop/SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "[verification-recipe.md](references/verification-recipe.md)",
                "verification-recipe.md",
            ),
            encoding="utf-8",
        )
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("never linked directly", result.stderr)

    def test_titled_untracked_runtime_reference_fails(self) -> None:
        extra = self.root / "skills/handoff/references/extra.md"
        extra.write_text("# Extra\n", encoding="utf-8")
        self.append("skills/handoff/SKILL.md", '[Extra](references/extra.md "Extra")')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("not in the bundle", result.stderr)

    def test_examples_pass_but_live_broken_link_fails(self) -> None:
        self.append(
            "README.md",
            '`[Example](not-a-real-file.md)`\n\n'
            '```markdown\n[Example](not-a-real-file.md)\n```',
        )
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.append("README.md", '[Live](not-a-real-file.md "Missing")')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("not in the bundle", result.stderr)

    def test_readme_broken_fragment_fails(self) -> None:
        self.append("README.md", "[Handoff](skills/handoff/SKILL.md#does-not-exist)")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("incorrect anchor", result.stderr)

    def test_title_backticks_cannot_hide_missing_dependency(self) -> None:
        self.append(
            "README.md", r'[License](LICENSE "A \`") [Missing](missing.md "A \`")'
        )
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("not in the bundle", result.stderr)

    def test_same_line_triple_code_cannot_hide_missing_dependency(self) -> None:
        self.append("README.md", '```literal``` [Missing](missing.md)')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("not in the bundle", result.stderr)

    def test_escaped_backtick_cannot_hide_missing_dependency(self) -> None:
        self.append("README.md", r'\` [Missing](missing.md) `')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("not in the bundle", result.stderr)

    def test_tab_separated_valid_title_passes(self) -> None:
        self.append("README.md", '[License](LICENSE\t"License")')
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)


    def test_misleading_interface_metadata_fails_at_cli(self) -> None:
        path = self.root / "skills/handoff/agents/openai.yaml"
        original = path.read_text(encoding="utf-8")
        for mutant in (
            original.replace("interface:", "other:"),
            original + '  default_prompt: "Continue without a skill."\n',
            original.replace('"Handoff"', '"$handoff"').replace("Use $handoff to", "Continue to"),
            original.replace("$handoff", "$handoff-other"),
            original.replace('"Handoff"', r'"Invalid\q"'),
            original.replace('"Handoff"', '"   "'),
        ):
            with self.subTest(metadata=mutant):
                path.write_text(mutant, encoding="utf-8")
                result = self.validate()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("validation failed:", result.stderr)

    def test_escaped_interface_string_passes_at_cli(self) -> None:
        path = self.root / "skills/handoff/agents/openai.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace('"Handoff"', r'"Handoff \"notes\""'),
            encoding="utf-8",
        )
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unexpected_tracked_file_still_fails(self) -> None:
        (self.root / "extra.md").write_text("# Extra\n", encoding="utf-8")
        self.git("add", "-f", "extra.md")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Tracked inventory differs", result.stderr)


if __name__ == "__main__":
    unittest.main()
