import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from analyze_sales import load_orders
from rag_engine import chunk_text, retrieve

class InternshipLabTests(unittest.TestCase):
    def test_sales_dataset_is_generated_and_valid(self):
        df = load_orders()
        self.assertEqual(len(df), 480)
        self.assertTrue((df["revenue_inr"] >= 0).all())

    def test_chunk_overlap_keeps_context(self):
        chunks = chunk_text("one two three four five six seven", size=5, overlap=2)
        self.assertEqual(chunks[1], "four five six seven")

    def test_retrieval_ranks_relevant_source_first(self):
        docs = [
            {"title": "SQL basics", "text": "SQL queries use select group by and joins."},
            {"title": "Fitness", "text": "A training plan includes exercise and recovery."}
        ]
        hits = retrieve("SQL group by queries", docs)
        self.assertTrue(hits)
        self.assertEqual(hits[0]["title"], "SQL basics")

if __name__ == "__main__":
    unittest.main()
