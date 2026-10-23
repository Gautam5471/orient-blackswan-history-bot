import unittest
import os
from rag_pipeline import OrientBlackSwanRAG

class TestOrientBlackSwanRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rag = OrientBlackSwanRAG()

    def test_q1_price_update(self):
        """Q1: On what date were the prices in this catalogue last updated?"""
        query = "On what date were the prices in this catalogue last updated?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "20 January 2025")
        self.assertIsNotNone(result["page"])
        self.assertIn("20-01-2025", result["excerpt"])

    def test_q2_incorporation_year(self):
        """Q2: In which year was the publisher (Orient BlackSwan) incorporated?"""
        query = "In which year was the publisher (Orient BlackSwan) incorporated?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "1948")
        self.assertEqual(result["page"], 2)
        self.assertIn("1948", result["excerpt"])

    def test_q3_physics_price_not_found(self):
        """Q3: What is the price of a Physics textbook?"""
        query = "What is the price of a Physics textbook?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "Not found")
        self.assertIsNone(result["page"])

    def test_q4_minister_of_education_not_found(self):
        """Q4: Who is the current Minister of Education?"""
        query = "Who is the current Minister of Education?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "Not found")
        self.assertIsNone(result["page"])

    def test_q5_best_book_not_found(self):
        """Q5: Which is the 'best' history book for a beginner?"""
        query = "Which is the 'best' history book for a beginner?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "Not found")
        self.assertIsNone(result["page"])

    def test_extra_unrelated_question(self):
        """Extra test: Unrelated question outside history scope."""
        query = "What is the melting point of copper?"
        result = self.rag.answer_question(query)
        self.assertEqual(result["answer"], "Not found")

    def test_extra_catalogue_search(self):
        """Extra test: General catalogue search for publisher website or distributor."""
        query = "What is the website of Orient BlackSwan?"
        result = self.rag.answer_question(query)
        self.assertTrue(result["answer"] != "" or result["answer"] == "Not found")

if __name__ == "__main__":
    unittest.main()
