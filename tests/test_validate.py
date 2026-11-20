import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from harness import validate


PAGE = validate.PAPERS / "2024" / "arxiv-2406.12045.md"


class ValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.draft = self.root / "draft.md"
        self.text = PAGE.read_text(encoding="utf-8")

    def test_candidate_correction_does_not_change_canonical_page(self):
        self.draft.write_text(self.text.replace("skipped confirmation", "missing confirmation"), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validate.main(["--candidate", str(self.draft)]), 0)
        self.assertEqual(PAGE.read_text(encoding="utf-8"), self.text)

    def test_rejects_mismatched_source_version_and_unknown_locator(self):
        self.draft.write_text(self.text.replace("version: v1", "version: v2").replace("[S4]", "[S9]"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source URL must match.*unknown source IDs: S9"):
            validate.validate_page(self.draft)

    def test_rejects_missing_required_section_and_example_label(self):
        self.draft.write_text(self.text.replace("## Evidence", "## Results").replace("**Illustrative example:**", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "expected these H2 sections.*recognized example label"):
            validate.validate_page(self.draft)

    def test_requires_a_topics_list_but_accepts_empty_tags(self):
        self.assertEqual(validate.validate_page(PAGE)["topics"], [])
        for replacement in ("", "topics: agent-reliability\n"):
            with self.subTest(replacement=replacement):
                self.draft.write_text(self.text.replace("topics: []\n", replacement), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "topics"):
                    validate.validate_page(self.draft)

    def test_requires_a_terminology_table_with_complete_rows(self):
        start = self.text.index("## Terminology\n")
        end = self.text.index("## Why\n", start)
        header = "| Term | Meaning in this paper | Why it matters |\n| --- | --- | --- |\n"
        for content in (
            "",
            "## Terminology\n\nDefinitions in prose.\n\n",
            f"## Terminology\n\n{header}\n",
            f"## Terminology\n\n{header}| Task | A fixed scenario | |\n\n",
        ):
            with self.subTest(content=content):
                self.draft.write_text(self.text[:start] + content + self.text[end:], encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Terminology must be a Markdown table"):
                    validate.validate_page(self.draft)

    def test_rejects_unresolved_relationship(self):
        self.draft.write_text(self.text.replace("relationships: []", """relationships:
  - paper: arxiv-2406.12046
    type: related_to
    reason: Test an unresolved target.
"""), encoding="utf-8")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), patch.object(validate, "PAPERS", self.root / "papers"):
            self.assertEqual(validate.main(["--candidate", str(self.draft)]), 1)
        self.assertIn("invalid relationship target: arxiv-2406.12046", stderr.getvalue())

    def test_requires_faq_but_allows_it_to_be_empty(self):
        before_faq = self.text.split("## FAQ\n", 1)[0]
        self.draft.write_text(before_faq + "## FAQ\n", encoding="utf-8")
        validate.validate_page(self.draft)
        self.draft.write_text(before_faq, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Source Locators, FAQ"):
            validate.validate_page(self.draft)

    def test_checks_citations_in_faq_after_source_locators(self):
        empty_faq = self.text.split("## FAQ\n", 1)[0] + "## FAQ\n"
        question = "\n### What does the scorer check?\n\nThe final database and required answers."
        self.draft.write_text(empty_faq + question + " [S2]\n", encoding="utf-8")
        validate.validate_page(self.draft)
        self.draft.write_text(empty_faq + question + " [S99]\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unknown source IDs: S99"):
            validate.validate_page(self.draft)


if __name__ == "__main__":
    unittest.main()
