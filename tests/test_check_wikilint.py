import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from harness import check_wikilint


PAGE = check_wikilint.PAPERS / "2024" / "arxiv-2406.12045.md"


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
            self.assertEqual(check_wikilint.main(["--candidate", str(self.draft)]), 0)
        self.assertEqual(PAGE.read_text(encoding="utf-8"), self.text)

    def test_rejects_mismatched_source_version_and_unknown_locator(self):
        self.draft.write_text(self.text.replace("version: v1", "version: v2").replace("[S4]", "[S9]"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source URL must match.*unknown source IDs: S9"):
            check_wikilint.validate_page(self.draft)

    def test_accepts_non_arxiv_sources_without_version(self):
        for kind in ("conference", "blog", "news"):
            with self.subTest(kind=kind):
                entry_id = f"{kind}-example-agent-evaluation"
                text = self.text.replace("id: arxiv-2406.12045", f"id: {entry_id}")
                text = text.replace("  version: v1\n", "").replace(
                    "https://arxiv.org/pdf/2406.12045v1", "https://example.org/agent-evaluation"
                )
                self.draft.write_text(text, encoding="utf-8")
                self.assertEqual(check_wikilint.validate_page(self.draft)["id"], entry_id)

    def test_accepts_news_without_specialized_terms_or_a_procedure(self):
        text = self.text.replace("id: arxiv-2406.12045", "id: news-example")
        text = re.sub(r"^authors:.*$", "authors: []", text, flags=re.M)
        text = text.replace("  version: v1\n", "").replace(
            "https://arxiv.org/pdf/2406.12045v1", "https://example.org/news"
        )
        text = re.sub(r"(?ms)^## Terminology\n.*?(?=^## )", "## Terminology\n\nNo specialized terminology.\n\n", text)
        text = re.sub(r"(?ms)^## Worked Example\n.*?(?=^## )", "## Worked Example\n\nNo method or procedure to demonstrate.\n\n", text)
        self.draft.write_text(text, encoding="utf-8")
        check_wikilint.validate_page(self.draft)
        self.draft.write_text(text.replace("https://example.org/news", "https:///news"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "HTTP\\(S\\) URL with a host"):
            check_wikilint.validate_page(self.draft)

    def test_rejects_missing_required_section_and_example_label(self):
        self.draft.write_text(self.text.replace("## Why", "## Motivation").replace("**Illustrative example:**", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "expected these H2 sections.*recognized example label"):
            check_wikilint.validate_page(self.draft)

    def test_accepts_core_with_either_both_or_neither_detail_section(self):
        for omitted in ((), ("Evidence",), ("Technical Depth",), ("Evidence", "Technical Depth")):
            with self.subTest(omitted=omitted):
                text = self.text
                for name in omitted:
                    text = re.sub(rf"(?ms)^## {name}\n.*?(?=^## )", "", text)
                self.draft.write_text(text, encoding="utf-8")
                check_wikilint.validate_page(self.draft)

    def test_requires_core_citations_even_with_cited_detail_sections(self):
        start = self.text.index("## Overview\n")
        end = self.text.index("## Evidence\n")
        text = self.text[:start] + re.sub(r"\[S[0-9]+\]", "", self.text[start:end]) + self.text[end:]
        text = re.sub(r"(?ms)^## Relationships\n.*?(?=^## )", "## Relationships\n\nNone.\n\n", text)
        self.draft.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "core explanation must cite"):
            check_wikilint.validate_page(self.draft)

    def test_rejects_misplaced_or_uncited_detail_sections(self):
        start = self.text.index("## Evidence\n")
        end = self.text.index("## Relationships\n", start)
        evidence = self.text[start:end]
        for text, error in (
            (self.text[:start] + self.text[end:] + "\n" + evidence, "expected these H2 sections"),
            (self.text[:start] + re.sub(r"\[S[0-9]+\]", "", evidence) + self.text[end:], "Evidence must cite"),
        ):
            with self.subTest(error=error):
                self.draft.write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, error):
                    check_wikilint.validate_page(self.draft)

    def test_requires_a_topics_list_but_accepts_empty_tags(self):
        self.assertEqual(check_wikilint.validate_page(PAGE)["topics"], [])
        for replacement in ("", "topics: agent-reliability\n"):
            with self.subTest(replacement=replacement):
                self.draft.write_text(self.text.replace("topics: []\n", replacement), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "topics"):
                    check_wikilint.validate_page(self.draft)

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
                    check_wikilint.validate_page(self.draft)

    def test_rejects_unresolved_relationship(self):
        self.draft.write_text(self.text.replace("relationships: []", """relationships:
  - paper: arxiv-2406.12046
    type: related_to
    reason: Test an unresolved target.
"""), encoding="utf-8")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), patch.object(check_wikilint, "PAPERS", self.root / "papers"):
            self.assertEqual(check_wikilint.main(["--candidate", str(self.draft)]), 1)
        self.assertIn("invalid relationship target: arxiv-2406.12046", stderr.getvalue())

    def test_requires_faq_but_allows_it_to_be_empty(self):
        before_faq = self.text.split("## FAQ\n", 1)[0]
        self.draft.write_text(before_faq + "## FAQ\n", encoding="utf-8")
        check_wikilint.validate_page(self.draft)
        self.draft.write_text(before_faq, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Source Locators, FAQ"):
            check_wikilint.validate_page(self.draft)

    def test_checks_citations_in_faq_after_source_locators(self):
        empty_faq = self.text.split("## FAQ\n", 1)[0] + "## FAQ\n"
        question = "\n### What does the scorer check?\n\nThe final database and required answers."
        self.draft.write_text(empty_faq + question + " [S2]\n", encoding="utf-8")
        check_wikilint.validate_page(self.draft)
        self.draft.write_text(empty_faq + question + " [S99]\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unknown source IDs: S99"):
            check_wikilint.validate_page(self.draft)


if __name__ == "__main__":
    unittest.main()
