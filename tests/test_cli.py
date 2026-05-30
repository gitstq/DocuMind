"""
Tests for CLI
"""

import unittest
import tempfile
from pathlib import Path
import sys
from io import StringIO

from documind.cli import main, create_parser


class TestCLI(unittest.TestCase):
    """Test cases for CLI"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("Hello World\nThis is a test document.")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_parser(self):
        """Test argument parser creation"""
        parser = create_parser()
        self.assertIsNotNone(parser)
    
    def test_parse_command(self):
        """Test parse command"""
        args = ['parse', str(self.test_file)]
        result = main(args)
        self.assertEqual(result, 0)
    
    def test_convert_command(self):
        """Test convert command"""
        output_file = Path(self.temp_dir) / "output.md"
        args = ['convert', str(self.test_file), '-o', str(output_file)]
        result = main(args)
        
        self.assertEqual(result, 0)
        self.assertTrue(output_file.exists())
    
    def test_extract_command(self):
        """Test extract command"""
        args = ['extract', str(self.test_file)]
        result = main(args)
        self.assertEqual(result, 0)
    
    def test_analyze_command(self):
        """Test analyze command"""
        args = ['analyze', str(self.test_file)]
        result = main(args)
        self.assertEqual(result, 0)
    
    def test_version_flag(self):
        """Test version flag"""
        with self.assertRaises(SystemExit) as cm:
            main(['--version'])
        self.assertEqual(cm.exception.code, 0)
    
    def test_help_flag(self):
        """Test help flag"""
        with self.assertRaises(SystemExit) as cm:
            main(['--help'])
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
