import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from harness import search_related as related


def work(number, title, citations=None, refs=(), doi=None):
    return {"id": f"https://openalex.org/W{number}", "display_name": title, "doi": doi,
            "publication_year": 2025, "cited_by_count": citations,
            "referenced_works": [f"https://openalex.org/W{ref}" for ref in refs]}


class FixtureOpenAlex:
    def __init__(self):
        self.seed = work(1, "Seed", refs=(2, 4))
        self.other_seed = work(5, "Other seed", refs=(2,))
        self.baseline = work(2, "Baseline", 100, doi="https://doi.org/10.1234/baseline")
        self.alias = work(6, "Baseline preprint", 80, doi=self.baseline["doi"])
        self.incoming = work(3, "Later citation", 300)
        self.bibliography = work(4, "Bibliography only", 101)

    def resolve(self, value):
        for item in (self.seed, self.other_seed, self.baseline, self.incoming):
            if related.identifier(value) in related.aliases(item):
                return item
        raise ValueError("no matching OpenAlex work")

    def get(self, *, filter, **params):
        if filter == "cites:W1":
            return {"results": [self.incoming, self.alias, self.other_seed], "meta": {"count": 100}}
        if filter == "cites:W5":
            return {"results": [self.seed]}
        if filter == "openalex:W2|W4":
            return {"results": [self.baseline, self.bibliography]}
        raise AssertionError(filter)


class SearchRelatedTests(unittest.TestCase):
    def test_multiple_seeds_citation_directions_dedupe_and_evidence_order(self):
        evidence = [
            {"paper": "10.1234/baseline", "seed": "W1", "kind": "baseline",
             "source": "https://example.org/seed", "note": "Compared in section 3"},
            {"paper": "W2", "kind": "presentation", "source": "https://example.org/program", "note": "Oral"},
        ]
        seeds, ranked, warnings = related.discover(FixtureOpenAlex(), ["W1", "W5"], [], evidence, 40)
        self.assertEqual(list(seeds), ["https://openalex.org/W1", "https://openalex.org/W5"])
        self.assertEqual([item[1]["display_name"] for item in ranked], ["Baseline", "Later citation", "Bibliography only"])
        _, baseline, links, notes, _ = ranked[0]
        self.assertEqual(baseline["cited_by_count"], 100)
        self.assertIn(("cites-seed", "https://openalex.org/W1"), links)
        self.assertIn(("cited-by-seed", "https://openalex.org/W5"), links)
        self.assertEqual(len(notes), 2)
        self.assertTrue(any("of 100" in warning for warning in warnings))

    def test_cli_writes_new_ranked_report_and_keeps_unknown_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shortlist.md"
            evidence_path = Path(tmp) / "evidence.json"
            evidence_path.write_text(json.dumps([
                {"paper": "10.1234/unindexed", "seed": "W1", "kind": "citing-paper", "title": "Unindexed follow-up",
                 "source": "https://example.org/follow-up", "note": "Builds on the seed's benchmark"}
            ]), encoding="utf-8")
            argv = ["--output", str(path), "--evidence", str(evidence_path), "W1", "W5"]
            with patch.object(related, "OpenAlex", FixtureOpenAlex), patch.object(related, "wiki_pages", return_value=[]), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(related.main(argv), 0)
                saved = path.read_text(encoding="utf-8")
                self.assertEqual(related.main(argv), 1)
            self.assertEqual(path.read_text(encoding="utf-8"), saved)
            self.assertLess(saved.index("1. [Later citation]"), saved.index("Unindexed follow-up"))
            self.assertIn("unknown OpenAlex citations", saved)
            self.assertIn("[citing-paper](<https://example.org/follow-up>)", saved)

    def test_screened_shortlist_excludes_unscreened_citations_and_awards(self):
        evidence = [
            {"paper": "10.1234/baseline", "seed": "W1", "kind": "related-work",
             "source": "https://example.org/seed", "note": "Section 2 compares the same retrieval task."},
            {"paper": "W3", "kind": "award", "source": "https://example.org/awards", "note": "Best Paper"},
            {"paper": "W4", "seed": "W1", "kind": "bibliography",
             "source": "https://example.org/seed", "note": "Listed in the bibliography."},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shortlist.md"
            evidence_path = Path(tmp) / "evidence.json"
            evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
            with patch.object(related, "OpenAlex", FixtureOpenAlex), patch.object(related, "wiki_pages", return_value=[]), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(related.main(["--output", str(path), "--require-relevance", "--evidence",
                                               str(evidence_path), "W1"]), 0)
            saved = path.read_text(encoding="utf-8")
        self.assertIn("1. [Baseline]", saved)
        self.assertNotIn("Later citation", saved)
        self.assertNotIn("Bibliography only", saved)

    def test_known_arxiv_version_matches_provider_alias(self):
        provider = FixtureOpenAlex()
        provider.baseline["locations"] = [{"landing_page_url": "https://arxiv.org/abs/2501.12345"}]
        pages = [(related.PAPERS / "2025" / "arxiv-2501.12345.md",
                  {"id": "arxiv-2501.12345", "title": "Baseline",
                   "source": {"url": "https://arxiv.org/pdf/2501.12345v2"}})]
        _, ranked, _ = related.discover(provider, ["W1", "W5"], pages, [], 40)
        self.assertNotIn("Baseline", [item[1]["display_name"] for item in ranked])
        _, ranked, _ = related.discover(provider, ["W1", "W5"], pages, [], 40, include_known=True)
        self.assertTrue(next(item[4] for item in ranked if item[1]["display_name"] == "Baseline"))
