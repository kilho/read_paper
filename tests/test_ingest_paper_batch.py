import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from harness import ingest_paper_batch as batch


TAU = "arxiv-2406.12045"
TERMINAL = "arxiv-2601.11868"


class BatchTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        papers = self.root / "wiki" / "papers"
        shutil.copytree(batch.wiki.PAPERS, papers)
        self.index = papers.parent / "index.md"
        shutil.copyfile(batch.wiki.PAPERS.parent / "index.md", self.index)
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(batch.wiki, "PAPERS", papers))
        stack.enter_context(patch.object(batch.wiki, "ROOT", self.root))
        stack.enter_context(patch.object(batch.shutil, "which", return_value="/bin/copilot"))
        self.launch = stack.enter_context(patch.object(batch.subprocess, "run"))
        self.stdout = stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.stderr = stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def complete(self, *outputs):
        self.launch.side_effect = [subprocess.CompletedProcess([], 0, output) for output in outputs]

    def test_isolates_papers_then_synthesizes_verified_ids(self):
        self.complete(f"INGEST_RESULT {TAU}\n", f"INGEST_RESULT {TERMINAL}\n", "SYNTHESIS_COMPLETE\n")
        self.assertEqual(batch.main([
            "https://arxiv.org/abs/2406.12045v1", TAU, "Terminal-Bench title",
            "--compare-with", TERMINAL, "--ingest-constraints", "Use short examples",
            "--synthesis-constraints", "Compare verifiers", "--allow-tool", "write(wiki/**)",
        ]), 0)
        calls = [call.args[0] for call in self.launch.call_args_list]
        session_ids = [uuid.UUID(call[call.index("--session-id") + 1]) for call in calls]
        self.assertEqual(len(set(session_ids)), 3)
        prompts = [call[call.index("--prompt") + 1] for call in calls]
        self.assertTrue(all("write(wiki/**)" in call and "--allow-all" not in call for call in calls))
        self.assertIn("/ingest-paper", prompts[0])
        data = [json.loads(prompt.rsplit("\nJSON input:\n", 1)[1]) for prompt in prompts]
        self.assertEqual(data, [
            {"paper": "https://arxiv.org/abs/2406.12045v1", "constraints": "Use short examples"},
            {"paper": "Terminal-Bench title", "constraints": "Use short examples"},
            {"papers": [TAU, TERMINAL], "compare_with": [], "constraints": "Compare verifiers"},
        ])

    def test_unindexed_page_blocks_synthesis_but_remaining_papers_run(self):
        lines = self.index.read_text(encoding="utf-8").splitlines()
        self.index.write_text("\n".join(line for line in lines if TAU not in line), encoding="utf-8")
        self.complete(f"INGEST_RESULT {TAU}\n", f"INGEST_RESULT {TERMINAL}\n")
        self.assertEqual(batch.main([TAU, TERMINAL]), 1)
        self.assertEqual(self.launch.call_count, 2)
        self.assertIn(TERMINAL, self.stdout.getvalue())
        self.assertIn("not linked in wiki/index.md", self.stderr.getvalue())
        self.assertIn("synthesis skipped", self.stderr.getvalue())

    def test_synthesis_needs_its_own_completion_report(self):
        self.complete(f"INGEST_RESULT {TAU}\n", "Could not verify the comparison.\n")
        self.assertEqual(batch.main([TAU, "--compare-with", TERMINAL]), 1)
        self.assertEqual(self.launch.call_count, 2)
        self.assertIn(f'"compare_with": ["{TERMINAL}"]', self.launch.call_args.args[0][-1])
        self.assertIn("synthesis did not report verified completion", self.stderr.getvalue())
