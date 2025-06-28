import re
import difflib
import string
import hashlib
from typing import List, Tuple, Dict, Set
from collections import defaultdict
import unicodedata

class CodeSimilarityAnalyzer:
    """
    A comprehensive code similarity analyzer that can compare source code files
    across different programming languages using multiple heuristics.
    """
    
    def __init__(self):
        # Common programming language keywords and operators
        self.common_keywords = {
            'if', 'else', 'elif', 'for', 'while', 'do', 'switch', 'case', 'default',
            'function', 'def', 'class', 'struct', 'interface', 'extends', 'implements',
            'import', 'include', 'require', 'from', 'as', 'namespace', 'using',
            'public', 'private', 'protected', 'static', 'final', 'const', 'let', 'var',
            'return', 'yield', 'break', 'continue', 'pass', 'throw', 'try', 'catch',
            'finally', 'except', 'with', 'lambda', 'async', 'await', 'new', 'delete'
        }
        
        self.operators = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                         '&&', '||', '!', '&', '|', '^', '<<', '>>', '++', '--'}
        
        # Comment patterns for different languages
        self.comment_patterns = [
            r'//.*$',           # C-style single line
            r'#.*$',            # Python/Shell style
            r'/\*.*?\*/',       # C-style multiline
            r'<!--.*?-->',      # HTML/XML
            r'--.*$',           # SQL style
            r';.*$',            # Assembly/Lisp style
        ]
        
    def normalize_line(self, line: str) -> str:
        """Normalize a line of code by removing comments, extra whitespace, and standardizing format."""
        # Remove comments
        for pattern in self.comment_patterns:
            line = re.sub(pattern, '', line, flags=re.DOTALL)
        
        # Normalize whitespace
        line = re.sub(r'\s+', ' ', line.strip())
        
        # Convert to lowercase for comparison
        line = line.lower()
        
        return line
    
    def extract_structural_features(self, line: str) -> Set[str]:
        """Extract structural features from a line of code."""
        features = set()
        normalized = self.normalize_line(line)
        
        # Check for keywords
        words = re.findall(r'\b\w+\b', normalized)
        for word in words:
            if word in self.common_keywords:
                features.add(f"keyword:{word}")
        
        # Check for operators
        for op in self.operators:
            if op in normalized:
                features.add(f"operator:{op}")
        
        # Check for common patterns
        patterns = {
            r'\b\w+\s*\(': 'function_call',
            r'\b\w+\s*=': 'assignment',
            r'\[\s*\w*\s*\]': 'array_access',
            r'\{\s*\w*\s*\}': 'block_or_dict',
            r'"\s*.*?\s*"': 'string_literal',
            r"'\s*.*?\s*'": 'string_literal',
            r'\b\d+\b': 'numeric_literal',
        }
        
        for pattern, feature in patterns.items():
            if re.search(pattern, normalized):
                features.add(feature)
        
        return features
    
    def tokenize_line(self, line: str) -> List[str]:
        """Tokenize a line into meaningful tokens."""
        normalized = self.normalize_line(line)
        
        # Split on common delimiters but preserve them
        tokens = re.findall(r'\w+|[^\w\s]', normalized)
        
        # Filter out empty tokens and single characters that aren't operators
        filtered_tokens = []
        for token in tokens:
            if len(token) > 1 or token in self.operators or token.isdigit():
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def calculate_line_similarity(self, line_a: str, line_b: str) -> float:
        """Calculate similarity between two lines using multiple metrics."""
        if not line_a.strip() or not line_b.strip():
            return 0.0
        
        # Exact match after normalization
        norm_a = self.normalize_line(line_a)
        norm_b = self.normalize_line(line_b)
        
        if norm_a == norm_b:
            return 1.0
        
        # Token-based similarity
        tokens_a = self.tokenize_line(line_a)
        tokens_b = self.tokenize_line(line_b)
        
        if not tokens_a or not tokens_b:
            return 0.0
        
        # Calculate Jaccard similarity for tokens
        set_a = set(tokens_a)
        set_b = set(tokens_b)
        jaccard = len(set_a & set_b) / len(set_a | set_b) if set_a | set_b else 0.0
        
        # Calculate sequence similarity
        sequence_similarity = difflib.SequenceMatcher(None, tokens_a, tokens_b).ratio()
        
        # Structural similarity
        features_a = self.extract_structural_features(line_a)
        features_b = self.extract_structural_features(line_b)
        structural_similarity = (
            len(features_a & features_b) / len(features_a | features_b) 
            if features_a | features_b else 0.0
        )
        
        # Weighted combination
        similarity = (
            0.4 * sequence_similarity +
            0.3 * jaccard +
            0.3 * structural_similarity
        )
        
        return similarity
    
    def preprocess_file(self, filepath: str) -> List[str]:
        """Read and preprocess a file, returning meaningful lines."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []
        
        # Filter out empty lines and comment-only lines
        meaningful_lines = []
        for line in lines:
            normalized = self.normalize_line(line)
            if normalized and len(normalized) > 2:  # Ignore very short lines
                meaningful_lines.append(line.rstrip())
        
        return meaningful_lines
    
    def find_similar_lines(self, lines_a: List[str], lines_b: List[str], 
                          threshold: float = 0.7) -> List[Tuple[int, int, float]]:
        """Find similar lines between two sets of lines."""
        similar_matches = []
        
        for i, line_a in enumerate(lines_a):
            best_match = (-1, 0.0)
            
            for j, line_b in enumerate(lines_b):
                similarity = self.calculate_line_similarity(line_a, line_b)
                
                if similarity >= threshold and similarity > best_match[1]:
                    best_match = (j, similarity)
            
            if best_match[0] != -1:
                similar_matches.append((i, best_match[0], best_match[1]))
        
        return similar_matches
    
    def analyze_code_similarity(self, file_a: str, file_b: str, 
                               similarity_threshold: float = 0.7) -> Dict:
        """
        Analyze similarity between two code files.
        
        Args:
            file_a: Path to first file
            file_b: Path to second file
            similarity_threshold: Minimum similarity score to consider lines similar
            
        Returns:
            Dictionary with analysis results
        """
        print(f"Analyzing similarity between {file_a} and {file_b}")
        print(f"Similarity threshold: {similarity_threshold}")
        
        # Read and preprocess files
        lines_a = self.preprocess_file(file_a)
        lines_b = self.preprocess_file(file_b)
        
        if not lines_a or not lines_b:
            return {
                'error': 'One or both files could not be read or contain no meaningful code',
                'lines_a_count': len(lines_a),
                'lines_b_count': len(lines_b)
            }
        
        # Find similar lines
        similar_matches = self.find_similar_lines(lines_a, lines_b, similarity_threshold)
        
        # Calculate statistics
        total_lines_a = len(lines_a)
        total_lines_b = len(lines_b)
        similar_lines_count = len(similar_matches)
        similarity_percentage = (similar_lines_count / total_lines_a) * 100 if total_lines_a > 0 else 0
        
        # Group matches by similarity score
        similarity_distribution = defaultdict(int)
        for _, _, score in similar_matches:
            score_range = f"{int(score * 10) * 10}%-{int(score * 10) * 10 + 9}%"
            similarity_distribution[score_range] += 1
        
        # Calculate average similarity for matches
        avg_similarity = (
            sum(score for _, _, score in similar_matches) / len(similar_matches)
            if similar_matches else 0.0
        )
        
        results = {
            'file_a': file_a,
            'file_b': file_b,
            'lines_a_count': total_lines_a,
            'lines_b_count': total_lines_b,
            'similar_lines_count': similar_lines_count,
            'similarity_percentage': round(similarity_percentage, 2),
            'average_similarity_score': round(avg_similarity, 3),
            'similarity_threshold': similarity_threshold,
            'similar_matches': similar_matches[:10],  # First 10 matches for review
            'similarity_distribution': dict(similarity_distribution)
        }
        
        return results
    
    def print_detailed_report(self, results: Dict):
        """Print a detailed similarity analysis report."""
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        print("=" * 80)
        print("CODE SIMILARITY ANALYSIS REPORT")
        print("=" * 80)
        print(f"File A: {results['file_a']}")
        print(f"File B: {results['file_b']}")
        print(f"Similarity Threshold: {results['similarity_threshold']}")
        print("-" * 80)
        print(f"Lines in File A: {results['lines_a_count']}")
        print(f"Lines in File B: {results['lines_b_count']}")
        print(f"Similar Lines Found: {results['similar_lines_count']}")
        print(f"Similarity Percentage: {results['similarity_percentage']}%")
        print(f"Average Similarity Score: {results['average_similarity_score']}")
        print("-" * 80)
        
        if results['similarity_distribution']:
            print("Similarity Score Distribution:")
            for score_range, count in sorted(results['similarity_distribution'].items()):
                print(f"  {score_range}: {count} matches")
        
        if results['similar_matches']:
            print("\nTop Similar Line Matches (Line A -> Line B, Score):")
            for line_a_idx, line_b_idx, score in results['similar_matches']:
                print(f"  Line {line_a_idx + 1} -> Line {line_b_idx + 1}: {score:.3f}")
        
        print("=" * 80)


def main():
    """Example usage of the CodeSimilarityAnalyzer."""
    analyzer = CodeSimilarityAnalyzer()
    
    # Example: Compare two files
    # You can replace these with actual file paths
    file_a = input("Enter path to first file (A): ").strip()
    file_b = input("Enter path to second file (B): ").strip()
    
    # Get similarity threshold from user
    threshold_input = input("Enter similarity threshold (0.0-1.0, default 0.7): ").strip()
    threshold = float(threshold_input) if threshold_input else 0.7
    
    # Perform analysis
    results = analyzer.analyze_code_similarity(file_a, file_b, threshold)
    
    # Print detailed report
    analyzer.print_detailed_report(results)
    
    # Optional: Save results to a file
    save_report = input("\nSave detailed report to file? (y/n): ").strip().lower()
    if save_report == 'y':
        import json
        output_file = f"similarity_report_{hashlib.md5((file_a + file_b).encode()).hexdigest()[:8]}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Report saved to {output_file}")


if __name__ == "__main__":
    main()