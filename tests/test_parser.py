"""
Tests for Document Parser
"""

import unittest
import tempfile
import os
from pathlib import Path

from documind.parser import DocumentParser, DocumentType, ParsedDocument


class TestDocumentParser(unittest.TestCase):
    """Test cases for DocumentParser"""
    
    def setUp(self):
        self.parser = DocumentParser()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_detect_type_txt(self):
        """Test detecting text file type"""
        self.assertEqual(
            self.parser.detect_type("test.txt"),
            DocumentType.TXT
        )
    
    def test_detect_type_md(self):
        """Test detecting markdown file type"""
        self.assertEqual(
            self.parser.detect_type("test.md"),
            DocumentType.MD
        )
    
    def test_detect_type_unknown(self):
        """Test detecting unknown file type"""
        self.assertEqual(
            self.parser.detect_type("test.xyz"),
            DocumentType.UNKNOWN
        )
    
    def test_parse_txt(self):
        """Test parsing text file"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = "Hello World\nThis is a test."
        test_file.write_text(test_content)
        
        result = self.parser.parse(test_file)
        
        self.assertIsInstance(result, ParsedDocument)
        self.assertEqual(result.document_type, DocumentType.TXT)
        self.assertIn("Hello World", result.content)
    
    def test_parse_markdown(self):
        """Test parsing markdown file"""
        test_file = Path(self.temp_dir) / "test.md"
        test_content = "# Title\n\n## Section 1\nContent here."
        test_file.write_text(test_content)
        
        result = self.parser.parse(test_file)
        
        self.assertEqual(result.document_type, DocumentType.MD)
        self.assertEqual(len(result.sections), 2)
    
    def test_parse_json(self):
        """Test parsing JSON file"""
        test_file = Path(self.temp_dir) / "test.json"
        test_content = '{"key": "value", "number": 42}'
        test_file.write_text(test_content)
        
        result = self.parser.parse(test_file)
        
        self.assertEqual(result.document_type, DocumentType.JSON)
        self.assertTrue(result.metadata.get("is_valid_json"))
    
    def test_parse_text_direct(self):
        """Test parsing text directly"""
        text = "# Header\n\nParagraph content."
        result = self.parser.parse_text(text, DocumentType.TXT)
        
        self.assertIsInstance(result, ParsedDocument)
        self.assertEqual(result.document_type, DocumentType.TXT)
    
    def test_extract_sections(self):
        """Test section extraction"""
        content = "# Title\nContent 1\n## Section\nContent 2"
        sections = self.parser._extract_sections(content)
        
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, "Title")
        self.assertEqual(sections[1].title, "Section")
    
    def test_extract_links(self):
        """Test link extraction"""
        content = "Visit https://example.com for more info."
        links = self.parser._extract_links(content)
        
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["url"], "https://example.com")


if __name__ == "__main__":
    unittest.main()
