"""
Tests for Document Analyzer
"""

import unittest

from documind.analyzer import DocumentAnalyzer, DocumentStats


class TestDocumentAnalyzer(unittest.TestCase):
    """Test cases for DocumentAnalyzer"""
    
    def setUp(self):
        self.analyzer = DocumentAnalyzer()
        self.sample_text = """
        # Document Title
        
        This is the first paragraph. It contains multiple sentences.
        Here is another sentence with some important keywords.
        
        ## Section 1
        
        This section discusses Python programming and software development.
        Python is a great language for building applications.
        
        ## Section 2
        
        Another paragraph with different content about data analysis.
        Data analysis is crucial for modern businesses.
        """
    
    def test_get_statistics(self):
        """Test document statistics calculation"""
        stats = self.analyzer.get_statistics(self.sample_text)
        
        self.assertIsInstance(stats, DocumentStats)
        self.assertGreater(stats.word_count, 0)
        self.assertGreater(stats.sentence_count, 0)
        self.assertGreater(stats.paragraph_count, 0)
    
    def test_analyze_keywords(self):
        """Test keyword analysis"""
        analysis = self.analyzer.analyze_keywords(self.sample_text)
        
        self.assertGreater(len(analysis.top_keywords), 0)
        # Check that stop words are filtered
        self.assertNotIn('the', [kw[0] for kw in analysis.top_keywords])
    
    def test_summarize(self):
        """Test text summarization"""
        summary = self.analyzer.summarize(self.sample_text, num_sentences=2)
        
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        # Should contain sentences
        self.assertIn('.', summary)
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        positive_text = "This is great! I love this amazing product."
        result = self.analyzer.analyze_sentiment(positive_text)
        
        self.assertIn('sentiment', result)
        self.assertIn('score', result)
        self.assertIn(result['sentiment'], ['positive', 'negative', 'neutral'])
    
    def test_detect_topics(self):
        """Test topic detection"""
        topics = self.analyzer.detect_topics(self.sample_text, num_topics=3)
        
        self.assertIsInstance(topics, list)
        self.assertLessEqual(len(topics), 3)
        
        for topic in topics:
            self.assertIn('topic', topic)
            self.assertIn('keywords', topic)
    
    def test_compare_documents(self):
        """Test document comparison"""
        text1 = "Python is a programming language. It is popular."
        text2 = "Python is widely used. Java is also popular."
        
        result = self.analyzer.compare_documents(text1, text2)
        
        self.assertIn('jaccard_similarity', result)
        self.assertIn('common_words', result)
        self.assertGreaterEqual(result['jaccard_similarity'], 0)
        self.assertLessEqual(result['jaccard_similarity'], 1)
    
    def test_generate_report(self):
        """Test report generation"""
        report = self.analyzer.generate_report(self.sample_text, output_format='dict')
        
        self.assertIn('statistics', report)
        self.assertIn('keywords', report)
        self.assertIn('summary', report)
        self.assertIn('sentiment', report)
        self.assertIn('topics', report)


if __name__ == "__main__":
    unittest.main()
