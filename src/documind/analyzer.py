"""
Document Analyzer Module
文档分析模块

Provides intelligent document analysis and insights.
提供智能文档分析和洞察功能。
"""

import re
import math
from collections import Counter
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from .parser import ParsedDocument, DocumentParser


@dataclass
class DocumentStats:
    """Statistics about a document"""
    word_count: int = 0
    char_count: int = 0
    char_count_no_spaces: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    avg_word_length: float = 0.0
    avg_sentence_length: float = 0.0
    readability_score: float = 0.0
    unique_words: int = 0
    lexical_diversity: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "word_count": self.word_count,
            "char_count": self.char_count,
            "char_count_no_spaces": self.char_count_no_spaces,
            "sentence_count": self.sentence_count,
            "paragraph_count": self.paragraph_count,
            "avg_word_length": round(self.avg_word_length, 2),
            "avg_sentence_length": round(self.avg_sentence_length, 2),
            "readability_score": round(self.readability_score, 2),
            "unique_words": self.unique_words,
            "lexical_diversity": round(self.lexical_diversity, 4)
        }


@dataclass
class KeywordAnalysis:
    """Keyword analysis results"""
    top_keywords: List[Tuple[str, int]] = field(default_factory=list)
    keyword_density: Dict[str, float] = field(default_factory=dict)
    bigrams: List[Tuple[str, int]] = field(default_factory=list)
    trigrams: List[Tuple[str, int]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "top_keywords": self.top_keywords[:20],
            "keyword_density": dict(list(self.keyword_density.items())[:20]),
            "bigrams": self.bigrams[:10],
            "trigrams": self.trigrams[:10]
        }


class DocumentAnalyzer:
    """
    Document analysis engine
    
    Features:
    - Document statistics (word count, readability, etc.)
    - Keyword extraction and analysis
    - Content summarization
    - Sentiment analysis (basic)
    - Topic detection
    """
    
    # Common stop words
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
        'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'it', 'we', 'they', 'them', 'their', 'there', 'then', 'than'
    }
    
    def __init__(self):
        self.parser = DocumentParser()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive document analysis
        
        Args:
            text: Document text to analyze
            
        Returns:
            Dictionary containing all analysis results
        """
        return {
            "statistics": self.get_statistics(text).to_dict(),
            "keywords": self.analyze_keywords(text).to_dict(),
            "summary": self.summarize(text),
            "sentiment": self.analyze_sentiment(text),
            "topics": self.detect_topics(text)
        }
    
    def analyze_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a document file"""
        parsed = self.parser.parse(file_path)
        return self.analyze(parsed.content)
    
    def get_statistics(self, text: str) -> DocumentStats:
        """Calculate document statistics"""
        stats = DocumentStats()
        
        # Basic counts
        stats.char_count = len(text)
        stats.char_count_no_spaces = len(text.replace(' ', '').replace('\n', ''))
        
        # Words
        words = re.findall(r'\b\w+\b', text.lower())
        stats.word_count = len(words)
        
        # Unique words
        unique_words = set(words)
        stats.unique_words = len(unique_words)
        
        # Lexical diversity
        if words:
            stats.lexical_diversity = len(unique_words) / len(words)
        
        # Average word length
        if words:
            stats.avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        stats.sentence_count = len(sentences)
        
        # Average sentence length
        if sentences:
            stats.avg_sentence_length = stats.word_count / len(sentences)
        
        # Paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        stats.paragraph_count = len(paragraphs)
        
        # Readability score (Flesch Reading Ease)
        if sentences and words:
            avg_sentence_length = stats.avg_sentence_length
            avg_syllables_per_word = self._count_syllables(text) / stats.word_count
            stats.readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return stats
    
    def analyze_keywords(self, text: str, top_n: int = 20) -> KeywordAnalysis:
        """Extract and analyze keywords"""
        analysis = KeywordAnalysis()
        
        # Tokenize and clean
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [w for w in words if w not in self.STOP_WORDS]
        
        if not words:
            return analysis
        
        # Word frequency
        word_freq = Counter(words)
        analysis.top_keywords = word_freq.most_common(top_n)
        
        # Keyword density
        total_words = len(words)
        analysis.keyword_density = {
            word: round(count / total_words * 100, 2)
            for word, count in analysis.top_keywords
        }
        
        # Bigrams
        bigrams = zip(words, words[1:])
        bigram_freq = Counter([' '.join(bg) for bg in bigrams])
        analysis.bigrams = bigram_freq.most_common(10)
        
        # Trigrams
        trigrams = zip(words, words[1:], words[2:])
        trigram_freq = Counter([' '.join(tg) for tg in trigrams])
        analysis.trigrams = trigram_freq.most_common(10)
        
        return analysis
    
    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Generate a text summary using extractive summarization
        
        Args:
            text: Input text
            num_sentences: Number of sentences in summary
            
        Returns:
            Summary text
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= num_sentences:
            return ' '.join(sentences)
        
        # Score sentences based on word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in self.STOP_WORDS]
        word_freq = Counter(words)
        
        sentence_scores = []
        for sentence in sentences:
            sentence_words = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq.get(w, 0) for w in sentence_words)
            score = score / len(sentence_words) if sentence_words else 0
            sentence_scores.append((sentence, score))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:num_sentences]]
        
        # Restore original order
        top_sentences.sort(key=lambda s: text.find(s))
        
        return '. '.join(top_sentences) + '.'
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Basic sentiment analysis
        
        Returns sentiment scores and classification
        """
        # Simple keyword-based sentiment
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'like', 'happy', 'pleased', 'satisfied', 'best', 'awesome',
            'perfect', 'beautiful', 'nice', 'positive', 'success', 'win'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad',
            'angry', 'disappointed', 'worst', 'ugly', 'negative', 'fail',
            'wrong', 'problem', 'issue', 'error', 'bug', 'broken'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        total = positive_count + negative_count
        
        if total == 0:
            sentiment = "neutral"
            score = 0.0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.2:
                sentiment = "positive"
            elif score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "positive_words": positive_count,
            "negative_words": negative_count
        }
    
    def detect_topics(self, text: str, num_topics: int = 5) -> List[Dict[str, Any]]:
        """
        Detect main topics in the document
        
        Uses keyword clustering for topic detection
        """
        # Extract keywords
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        words = [w for w in words if w not in self.STOP_WORDS]
        
        word_freq = Counter(words)
        top_words = word_freq.most_common(num_topics * 3)
        
        topics = []
        for i in range(0, len(top_words), 3):
            topic_words = top_words[i:i+3]
            if topic_words:
                topic_name = topic_words[0][0]
                topics.append({
                    "topic": topic_name,
                    "keywords": [w[0] for w in topic_words],
                    "frequency": sum(w[1] for w in topic_words)
                })
        
        return topics[:num_topics]
    
    def compare_documents(self, text1: str, text2: str) -> Dict[str, Any]:
        """Compare two documents and return similarity metrics"""
        # Word overlap
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        intersection = words1 & words2
        union = words1 | words2
        
        jaccard_similarity = len(intersection) / len(union) if union else 0
        
        # Common keywords
        common_words = intersection - self.STOP_WORDS
        
        return {
            "jaccard_similarity": round(jaccard_similarity, 4),
            "common_words": list(common_words)[:20],
            "unique_to_doc1": list(words1 - words2)[:10],
            "unique_to_doc2": list(words2 - words1)[:10]
        }
    
    def _count_syllables(self, text: str) -> int:
        """Estimate syllable count in text"""
        words = re.findall(r'\b\w+\b', text.lower())
        count = 0
        
        for word in words:
            # Simple syllable counting heuristic
            vowels = 'aeiouy'
            syllables = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = is_vowel
            
            # Handle silent e
            if word.endswith('e') and syllables > 1:
                syllables -= 1
            
            count += max(1, syllables)
        
        return count
    
    def generate_report(self, text: str, output_format: str = "dict") -> Union[Dict, str]:
        """
        Generate a comprehensive analysis report
        
        Args:
            text: Document text
            output_format: 'dict', 'json', or 'markdown'
            
        Returns:
            Analysis report in specified format
        """
        analysis = self.analyze(text)
        
        if output_format == "dict":
            return analysis
        elif output_format == "json":
            import json
            return json.dumps(analysis, indent=2, ensure_ascii=False)
        elif output_format == "markdown":
            return self._format_markdown_report(analysis)
        else:
            raise ValueError(f"Unknown format: {output_format}")
    
    def _format_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """Format analysis as Markdown report"""
        lines = []
        
        lines.append("# Document Analysis Report")
        lines.append("")
        
        # Statistics
        stats = analysis["statistics"]
        lines.append("## Document Statistics")
        lines.append("")
        lines.append(f"- **Word Count**: {stats['word_count']}")
        lines.append(f"- **Character Count**: {stats['char_count']}")
        lines.append(f"- **Sentence Count**: {stats['sentence_count']}")
        lines.append(f"- **Paragraph Count**: {stats['paragraph_count']}")
        lines.append(f"- **Average Word Length**: {stats['avg_word_length']}")
        lines.append(f"- **Readability Score**: {stats['readability_score']}")
        lines.append(f"- **Lexical Diversity**: {stats['lexical_diversity']}")
        lines.append("")
        
        # Keywords
        keywords = analysis["keywords"]
        lines.append("## Top Keywords")
        lines.append("")
        for word, count in keywords["top_keywords"][:10]:
            lines.append(f"- {word}: {count}")
        lines.append("")
        
        # Sentiment
        sentiment = analysis["sentiment"]
        lines.append("## Sentiment Analysis")
        lines.append("")
        lines.append(f"- **Overall**: {sentiment['sentiment']}")
        lines.append(f"- **Score**: {sentiment['score']}")
        lines.append("")
        
        # Topics
        topics = analysis["topics"]
        lines.append("## Detected Topics")
        lines.append("")
        for topic in topics:
            lines.append(f"- **{topic['topic']}**: {', '.join(topic['keywords'])}")
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(analysis["summary"])
        
        return '\n'.join(lines)
