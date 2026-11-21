import contextlib
import io
import json
import re
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
        tau, = papers.glob(f"*/{TAU}.md")
        baseline = "arxiv-9999.99999"
        tau.with_name(f"{baseline}.md").write_text(
            tau.read_text(encoding="utf-8").replace("2406.12045", "9999.99999")
            .replace("τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains", "Baseline fixture"),
            encoding="utf-8",
        )
        terminal, = papers.glob(f"*/{TERMINAL}.md")
        terminal.write_text(re.sub(
            r"(?ms)^relationships:\n.*?(?=^---$)", "relationships: []\n", terminal.read_text(encoding="utf-8"),
        ), encoding="utf-8")
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(batch.wiki, "PAPERS", papers))
        stack.enter_context(patch.object(batch.wiki, "ROOT", self.root))
        stack.enter_context(patch.object(batch.shutil, "which", return_value="/bin/copilot"))
        self.launch = stack.enter_context(patch.object(batch.subprocess, "run"))
        self.stdout = stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.stderr = stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def complete(self, *outputs):
        outputs = iter(outputs)

        def finish(*args, **kwargs):
            output = next(outputs)
            if output.startswith("INGEST_RESULT "):
                paper_id = output.split()[1]
                if paper_id in self.unpublished:
                    path, contents = self.unpublished.pop(paper_id)
                    path.write_bytes(contents)
            return subprocess.CompletedProcess([], 0, output)

        self.unpublished = {}
        self.launch.side_effect = finish

    def unpublish(self, paper_id):
        path, = batch.wiki.PAPERS.glob(f"*/{paper_id}.md")
        self.unpublished[paper_id] = (path, path.read_bytes())
        path.unlink()

    def test_isolates_papers_then_synthesizes_verified_ids(self):
        self.complete(f"INGEST_RESULT {TAU}\n", f"INGEST_RESULT {TERMINAL}\n", "SYNTHESIS_COMPLETE\n")
        self.unpublish(TAU)
        self.unpublish(TERMINAL)
        self.assertEqual(batch.main([
            "https://arxiv.org/abs/2406.12045v1", TAU, "Terminal-Bench title",
            "--ingest-constraints", "Use short examples",
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
        self.unpublish(TAU)
        self.assertEqual(batch.main([TAU, "alternate terminal source"]), 1)
        self.assertEqual(self.launch.call_count, 2)
        self.assertIn(TERMINAL, self.stdout.getvalue())
        self.assertIn("not linked in wiki/index.md", self.stderr.getvalue())
        self.assertIn("synthesis skipped", self.stderr.getvalue())

    def test_synthesis_needs_its_own_completion_report(self):
        self.complete(f"INGEST_RESULT {TAU}\n", "Could not verify the comparison.\n")
        self.unpublish(TAU)
        self.assertEqual(batch.main([TERMINAL, TAU, "--compare-with", TERMINAL]), 1)
        self.assertEqual(self.launch.call_count, 2)
        self.assertIn(f'"compare_with": ["{TERMINAL}"]', self.launch.call_args.args[0][-1])
        self.assertIn("synthesis did not report verified completion", self.stderr.getvalue())

    def test_existing_url_path_and_title_do_not_start_sessions(self):
        path, = batch.wiki.PAPERS.glob(f"*/{TERMINAL}.md")
        meta, _ = batch.wiki.read_page(path)
        with patch.object(batch.shutil, "which", return_value=None):
            self.assertEqual(batch.main([
                "https://arxiv.org/abs/2406.12045v1",
                f"wiki/papers/{meta['year']}/{TERMINAL}.md",
                meta["title"].upper(),
            ]), 0)
        self.launch.assert_not_called()
        self.assertIn(f"Skipped existing wiki paper: {TAU}", self.stdout.getvalue())
        self.assertIn(f"Skipped existing wiki paper: {TERMINAL}", self.stdout.getvalue())
        self.assertIn("synthesis skipped", self.stdout.getvalue())

    def test_existing_paper_is_not_implicitly_added_to_synthesis(self):
        self.complete(f"INGEST_RESULT {TAU}\n", "SYNTHESIS_COMPLETE\n")
        self.unpublish(TAU)
        self.assertEqual(batch.main([TERMINAL, TAU]), 0)
        self.assertEqual(self.launch.call_count, 2)
        prompt = self.launch.call_args.args[0][-1]
        data = json.loads(prompt.rsplit("\nJSON input:\n", 1)[1])
        self.assertEqual(data, {"papers": [TAU], "compare_with": [], "constraints": ""})
