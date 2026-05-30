"""
Tests for Markdown Converter
"""

import unittest
import tempfile
from pathlib import Path

from documind.converter import MarkdownConverter


class TestMarkdownConverter(unittest.TestCase):
    """Test cases for MarkdownConverter"""
    
    def setUp(self):
        self.converter = MarkdownConverter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_convert_txt_to_markdown(self):
        """Test converting text to markdown"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Hello World\n\nThis is content.")
        
        result = self.converter.convert(test_file)
        
        self.assertIn("test", result.lower())
        self.assertIn("Hello World", result)
    
    def test_convert_with_toc(self):
        """Test conversion with table of contents"""
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("# Title\n\n## Section 1\nContent")
        
        result = self.converter.convert(test_file, include_toc=True)
        
        self.assertIn("Table of Contents", result)
    
    def test_convert_with_metadata(self):
        """Test conversion with metadata"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Content here.")
        
        result = self.converter.convert(test_file, include_metadata=True)
        
        self.assertIn("---", result)
    
    def test_table_to_markdown(self):
        """Test table conversion"""
        table = [
            ["Header 1", "Header 2"],
            ["Cell 1", "Cell 2"],
            ["Cell 3", "Cell 4"]
        ]
        
        result = self.converter._table_to_markdown(table)
        
        self.assertIn("| Header 1 | Header 2 |", result)
        self.assertIn("| --- | --- |", result)
    
    def test_convert_to_file(self):
        """Test converting and saving to file"""
        test_file = Path(self.temp_dir) / "test.txt"
        output_file = Path(self.temp_dir) / "output.md"
        test_file.write_text("Test content.")
        
        result_path = self.converter.convert_to_file(test_file, output_file)
        
        self.assertTrue(Path(result_path).exists())
        self.assertIn("Test content", Path(result_path).read_text())


if __name__ == "__main__":
    unittest.main()
