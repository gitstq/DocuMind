"""
Tests for Structured Extractor
"""

import unittest
import tempfile
from pathlib import Path

from documind.extractor import StructuredExtractor, ExtractionRule


class TestStructuredExtractor(unittest.TestCase):
    """Test cases for StructuredExtractor"""
    
    def setUp(self):
        self.extractor = StructuredExtractor()
    
    def test_extract_emails(self):
        """Test email extraction"""
        text = "Contact us at test@example.com or support@company.org"
        result = self.extractor.extract(text, ['email'])
        
        self.assertIn('email', result)
        self.assertEqual(len(result['email']), 2)
        self.assertIn('test@example.com', result['email'])
    
    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Visit https://example.com and http://test.org"
        result = self.extractor.extract(text, ['url'])
        
        self.assertIn('url', result)
        self.assertEqual(len(result['url']), 2)
    
    def test_extract_dates(self):
        """Test date extraction"""
        text = "Meeting on 2025-01-15 and deadline 12/31/2025"
        result = self.extractor.extract(text, ['date_iso', 'date_us'])
        
        self.assertIn('date_iso', result)
        self.assertIn('2025-01-15', result['date_iso'])
    
    def test_extract_all_patterns(self):
        """Test extracting all patterns"""
        text = "Email: test@example.com, URL: https://example.com"
        result = self.extractor.extract(text)
        
        self.assertIn('email', result)
        self.assertIn('url', result)
    
    def test_extract_entities(self):
        """Test entity extraction"""
        text = "John Smith works at Acme Corp in New York."
        result = self.extractor.extract_entities(text)
        
        self.assertIn('persons', result)
        self.assertIn('organizations', result)
    
    def test_extract_key_value_pairs(self):
        """Test key-value pair extraction"""
        text = "Name: John\nAge: 30\nCity: New York"
        result = self.extractor.extract_key_value_pairs(text)
        
        self.assertEqual(result.get('Name'), 'John')
        self.assertEqual(result.get('Age'), '30')
    
    def test_add_custom_rule(self):
        """Test adding custom extraction rule"""
        self.extractor.add_custom_rule(
            name="custom_id",
            pattern=r"ID:\s*(\d+)",
            multiple=True
        )
        
        text = "ID: 123 and ID: 456"
        result = self.extractor.extract(text)
        
        self.assertIn('custom_id', result)
    
    def test_export_to_json(self):
        """Test JSON export"""
        data = {"email": ["test@example.com"]}
        result = self.extractor.export_to_json(data)
        
        self.assertIn('test@example.com', result)
        self.assertIn('"email"', result)


if __name__ == "__main__":
    unittest.main()
