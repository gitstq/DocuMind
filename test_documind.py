#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocuMind Unit Tests
"""

import unittest
import tempfile
import os
from pathlib import Path

from documind import (
    TextUtils, DocumentSummarizer, KeywordExtractor,
    KnowledgeGraph, MarkdownParser, TextParser, DocumentProcessor
)


class TestTextUtils(unittest.TestCase):
    """Test text utility functions"""

    def test_tokenize(self):
        text = "The quick brown fox jumps over the lazy dog"
        tokens = TextUtils.tokenize(text)
        self.assertIn('quick', tokens)
        self.assertIn('brown', tokens)
        self.assertIn('fox', tokens)
        self.assertNotIn('the', tokens)  # Stop word

    def test_normalize_whitespace(self):
        text = "  Multiple   spaces   here  "
        normalized = TextUtils.normalize_whitespace(text)
        self.assertEqual(normalized, "Multiple spaces here")

    def test_extract_sentences(self):
        text = "First sentence. Second sentence! Third sentence?"
        sentences = TextUtils.extract_sentences(text)
        self.assertEqual(len(sentences), 3)

    def test_calculate_tf_idf(self):
        docs = ["machine learning is amazing", "deep learning is powerful"]
        tf_idf = TextUtils.calculate_tf_idf(docs)
        self.assertIn('machine', tf_idf)
        self.assertIn('learning', tf_idf)


class TestDocumentSummarizer(unittest.TestCase):
    """Test document summarization"""

    def test_summarize_short_text(self):
        text = "This is a short text."
        summary = DocumentSummarizer.summarize(text)
        self.assertEqual(summary, text)

    def test_summarize_long_text(self):
        text = " ".join([f"Sentence number {i} has some content." for i in range(20)])
        summary = DocumentSummarizer.summarize(text, ratio=0.2)
        self.assertTrue(len(summary) < len(text))


class TestKeywordExtractor(unittest.TestCase):
    """Test keyword extraction"""

    def test_extract_keywords(self):
        text = "Python programming is great. Python is versatile. Programming with Python is fun."
        keywords = KeywordExtractor.extract(text, top_n=3)
        self.assertTrue(len(keywords) <= 3)
        self.assertTrue(all(isinstance(k, tuple) and len(k) == 2 for k in keywords))


class TestKnowledgeGraph(unittest.TestCase):
    """Test knowledge graph building"""

    def test_extract_entities(self):
        kg = KnowledgeGraph()
        text = "Apple Inc. is located in Cupertino. Contact us at test@example.com"
        entities = kg.extract_entities(text)
        self.assertTrue(len(entities) > 0)

    def test_build(self):
        kg = KnowledgeGraph()
        text = "Google and Microsoft are tech companies. Google competes with Microsoft."
        graph = kg.build(text)
        self.assertIn('entities', graph)
        self.assertIn('relations', graph)

    def test_to_mermaid(self):
        kg = KnowledgeGraph()
        kg.build("Apple and Google are companies.")
        mermaid = kg.to_mermaid()
        self.assertTrue(mermaid.startswith('graph TD'))


class TestMarkdownParser(unittest.TestCase):
    """Test markdown parsing"""

    def test_parse_heading(self):
        content = "# Title\n\n## Section\n\nParagraph text."
        result = MarkdownParser._parse_content(content)
        self.assertEqual(result['title'], 'Title')
        self.assertTrue(len(result['headings']) > 0)

    def test_parse_code_block(self):
        content = "```python\nprint('hello')\n```"
        result = MarkdownParser._parse_content(content)
        self.assertEqual(len(result['code_blocks']), 1)
        self.assertEqual(result['code_blocks'][0]['language'], 'python')

    def test_parse_links(self):
        content = "[Link text](https://example.com)"
        result = MarkdownParser._parse_content(content)
        self.assertEqual(len(result['links']), 1)
        self.assertEqual(result['links'][0]['text'], 'Link text')


class TestTextParser(unittest.TestCase):
    """Test text file parsing"""

    def test_parse(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Line 1\nLine 2\nLine 3")
            temp_path = f.name

        try:
            result = TextParser.parse(temp_path)
            self.assertEqual(result['title'], 'Line 1')
            self.assertEqual(len(result['paragraphs']), 3)
        finally:
            os.unlink(temp_path)


class TestDocumentProcessor(unittest.TestCase):
    """Test document processor"""

    def test_process_txt_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document. It has multiple sentences.")
            temp_path = f.name

        try:
            processor = DocumentProcessor()
            result = processor.process_file(temp_path)
            self.assertTrue(result['success'])
            self.assertEqual(result['format'], '.txt')
        finally:
            os.unlink(temp_path)

    def test_process_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            for i in range(3):
                with open(os.path.join(tmpdir, f"test{i}.txt"), 'w') as f:
                    f.write(f"Content {i}")

            processor = DocumentProcessor()
            results = processor.process_directory(tmpdir, recursive=False)
            self.assertEqual(len(results), 3)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_full_pipeline(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""
Machine Learning and Artificial Intelligence

Machine learning is a subset of artificial intelligence.
Deep learning is a technique used in machine learning.
AI systems can learn from data and improve over time.
            """)
            temp_path = f.name

        try:
            processor = DocumentProcessor()
            result = processor.process_file(temp_path, {
                'summarize': True,
                'keywords': True,
                'knowledge_graph': True
            })

            self.assertTrue(result['success'])
            self.assertTrue(result['summary'])
            self.assertTrue(result['keywords'])
            self.assertTrue(result['knowledge_graph'])
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
