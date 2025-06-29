import re
import difflib
import string
import hashlib
from typing import List, Tuple, Dict, Set
from collections import defaultdict
import unicodedata

class CodeSimilarityAnalyzer:
    """
    A focused code similarity analyzer for detecting similar code within the same programming language.
    Optimized for accuracy in plagiarism detection and identifying code modifications.
    """
    
    def __init__(self):
        # Language-agnostic structural patterns for same-language comparison
        self.structural_keywords = {
            'if', 'else', 'elif', 'for', 'while', 'do', 'switch', 'case', 
            'function', 'def', 'class', 'return', 'break', 'continue',
            'try', 'catch', 'finally', 'throw', 'import', 'from'
        }
        
        self.operators = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                         '&&', '||', '!', '&', '|', '^', '++', '--'}
        
    def normalize_line(self, line: str) -> str:
        """Normalize a line of code for comparison."""
        # Remove common comment patterns
        line = re.sub(r'//.*$|#.*$|/\*.*?\*/|<!--.*?-->', '', line, flags=re.DOTALL)
        
        # Normalize whitespace
        line = re.sub(r'\s+', ' ', line.strip())
        
        # Convert to lowercase for comparison
        line = line.lower()
        
        return line
        
        return line
    
    def extract_structural_features(self, line: str) -> Set[str]:
        """Extract key structural features from a line of code for same-language comparison."""
        features = set()
        normalized = self.normalize_line(line)
        
        # Extract keywords that indicate code structure
        words = re.findall(r'\b\w+\b', normalized)
        for word in words:
            if word in self.structural_keywords:
                features.add(f"keyword:{word}")
        
        # Extract operators
        for op in self.operators:
            if op in normalized:
                features.add(f"operator:{op}")
        
        # Extract specific patterns for same-language detection
        patterns = {
            r'\b\w+\s*\(.*?\)': 'function_call',
            r'\b\w+\s*=': 'assignment',
            r'\[.*?\]': 'indexing',
            r'\{.*?\}': 'block_or_object',
            r'"[^"]*"': 'string_literal',
            r"'[^']*'": 'string_literal',
            r'\b\d+(\.\d+)?\b': 'numeric_literal',
        }
        
        for pattern, feature in patterns.items():
            if re.search(pattern, normalized):
                features.add(feature)
        
        return features
    
    def tokenize_line(self, line: str) -> List[str]:
        """Tokenize a line into meaningful code tokens."""
        normalized = self.normalize_line(line)
        
        # Extract meaningful tokens (identifiers, operators, literals)
        tokens = re.findall(r'\w+|[^\w\s]', normalized)
        
        # Filter meaningful tokens
        filtered_tokens = []
        for token in tokens:
            # Keep multi-character tokens, important operators, and numbers
            if len(token) > 1 or token in self.operators or token.isdigit():
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def calculate_line_similarity(self, line_a: str, line_b: str) -> float:
        """Calculate similarity between two lines of the same programming language."""
        if not line_a.strip() or not line_b.strip():
            return 0.0
        
        # Exact match after normalization
        norm_a = self.normalize_line(line_a)
        norm_b = self.normalize_line(line_b)
        
        if norm_a == norm_b:
            return 1.0
        
        # Skip very short lines (likely generic syntax)
        if len(norm_a) <= 2 or len(norm_b) <= 2:
            return 1.0 if norm_a == norm_b else 0.0
        
        # Heavily penalize generic single-character or common syntax lines
        generic_patterns = {'{', '}', '(', ')', '[', ']', ';', ':', ','}
        if norm_a.strip() in generic_patterns or norm_b.strip() in generic_patterns:
            return 1.0 if norm_a == norm_b else 0.0
        
        # Get tokens and features
        tokens_a = self.tokenize_line(line_a)
        tokens_b = self.tokenize_line(line_b)
        features_a = self.extract_structural_features(line_a)
        features_b = self.extract_structural_features(line_b)
        
        if not tokens_a or not tokens_b:
            return 0.0
        
        # Calculate different similarity metrics
        
        # 1. Token-based Jaccard similarity
        set_a = set(tokens_a)
        set_b = set(tokens_b)
        jaccard = len(set_a & set_b) / len(set_a | set_b) if set_a | set_b else 0.0
        
        # 2. Sequence similarity (order matters for code)
        sequence_similarity = difflib.SequenceMatcher(None, tokens_a, tokens_b).ratio()
        
        # 3. Structural pattern similarity
        structural_similarity = (
            len(features_a & features_b) / len(features_a | features_b) 
            if features_a | features_b else 0.0
        )
        
        # 4. Literal string similarity (for variable name changes detection)
        string_similarity = difflib.SequenceMatcher(None, norm_a, norm_b).ratio()
        
        # 5. Enhanced structural similarity for plagiarism detection
        # Count shared patterns even if variable names differ
        enhanced_structural = 0.0
        if features_a and features_b:
            # Higher weight if lines have similar structural patterns
            pattern_overlap = len(features_a & features_b) / max(len(features_a), len(features_b))
            if pattern_overlap > 0.5:  # Strong structural similarity
                enhanced_structural = pattern_overlap
        
        # Require minimum meaningful overlap for any similarity
        if jaccard < 0.1 and sequence_similarity < 0.2 and string_similarity < 0.3:
            return 0.0
        
        # Adaptive weighted combination based on the type of similarity detected
        if string_similarity > 0.7:  # High string similarity (likely variable name changes)
            # Emphasize string and structural similarity for plagiarism detection
            similarity = (
                0.40 * string_similarity +       # High weight for similar structure
                0.25 * sequence_similarity +     # Code structure and order
                0.20 * enhanced_structural +     # Enhanced structural patterns
                0.15 * jaccard                   # Token overlap
            )
        else:  # Different implementations or unrelated code
            # More balanced approach
            similarity = (
                0.35 * sequence_similarity +     # Code structure and order
                0.30 * string_similarity +       # Overall similarity
                0.20 * jaccard +                 # Token overlap
                0.15 * structural_similarity     # Basic structural patterns
            )
        
        return max(0.0, similarity)
    
    def preprocess_file(self, filepath: str) -> List[str]:
        """Read and preprocess a file, extracting meaningful code lines."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []
        
        # Filter for meaningful code lines
        meaningful_lines = []
        for line in lines:
            normalized = self.normalize_line(line)
            # Keep lines that have substantial content
            if normalized and len(normalized) > 3 and not self._is_trivial_line(normalized):
                meaningful_lines.append(line.rstrip())
        
        return meaningful_lines
    
    def preprocess_code_fragment(self, code: str) -> List[str]:
        """Process a code fragment string into meaningful lines."""
        if not code:
            return []
        
        # Split into lines
        lines = code.split('\n')
        
        # Filter for meaningful code lines
        meaningful_lines = []
        for line in lines:
            normalized = self.normalize_line(line)
            # Keep lines that have substantial content
            if normalized and len(normalized) > 3 and not self._is_trivial_line(normalized):
                meaningful_lines.append(line.rstrip())
        
        return meaningful_lines

    def _is_trivial_line(self, normalized_line: str) -> bool:
        """Check if a line is too trivial to be meaningful for comparison."""
        trivial_patterns = {
            # Common single characters or simple syntax
            '{', '}', '(', ')', '[', ']', ';', ':', ',',
            # Common single words that appear everywhere
            'else', 'end', 'pass', 'break', 'continue'
        }
        
        # Remove common trivial lines
        line = normalized_line.strip()
        if line in trivial_patterns:
            return True
        
        # Lines with only punctuation or very short
        if len(line) <= 2 or line.isspace():
            return True
            
        # Lines that are just imports/includes without specific content
        if re.match(r'^(import|include|using|from)\s*$', line):
            return True
            
        return False
    
    def find_similar_lines(self, lines_a: List[str], lines_b: List[str], 
                          threshold: float = 0.7) -> List[Tuple[int, int, float]]:
        """Find similar lines between two sets of lines using optimal matching."""
        # Calculate similarity matrix
        similarity_matrix = []
        for i, line_a in enumerate(lines_a):
            row = []
            for j, line_b in enumerate(lines_b):
                similarity = self.calculate_line_similarity(line_a, line_b)
                row.append(similarity if similarity >= threshold else 0.0)
            similarity_matrix.append(row)
        
        # Find optimal one-to-one matching using greedy approach
        similar_matches = []
        used_b_indices = set()
        
        # Create list of all potential matches above threshold
        potential_matches = []
        for i in range(len(lines_a)):
            for j in range(len(lines_b)):
                if similarity_matrix[i][j] >= threshold:
                    potential_matches.append((i, j, similarity_matrix[i][j]))
        
        # Sort by similarity score (descending) to prioritize best matches
        potential_matches.sort(key=lambda x: x[2], reverse=True)
        
        # Greedily select non-conflicting matches
        used_a_indices = set()
        for i, j, score in potential_matches:
            if i not in used_a_indices and j not in used_b_indices:
                similar_matches.append((i, j, score))
                used_a_indices.add(i)
                used_b_indices.add(j)
        
        return similar_matches
    
    def analyze_code_similarity(self, input_a: str, input_b: str, 
                               similarity_threshold: float = 0.7, 
                               is_file: bool = True) -> Dict:
        """
        Analyze similarity between two code inputs (files or code fragments).
        
        Args:
            input_a: Path to first file or first code fragment
            input_b: Path to second file or second code fragment
            similarity_threshold: Minimum similarity score to consider lines similar
            is_file: If True, inputs are file paths; if False, inputs are code fragments
            
        Returns:
            Dictionary with analysis results
        """
        if is_file:
            print(f"Analyzing similarity between files {input_a} and {input_b}")
            source_a, source_b = input_a, input_b
            # Read and preprocess files
            lines_a = self.preprocess_file(input_a)
            lines_b = self.preprocess_file(input_b)
        else:
            print(f"Analyzing similarity between code fragments")
            source_a, source_b = "Code Fragment A", "Code Fragment B"
            # Process code fragments directly
            lines_a = self.preprocess_code_fragment(input_a)
            lines_b = self.preprocess_code_fragment(input_b)
        
        print(f"Similarity threshold: {similarity_threshold}")
        
        if not lines_a or not lines_b:
            return {
                'error': 'One or both inputs could not be read or contain no meaningful code',
                'lines_a_count': len(lines_a) if lines_a else 0,
                'lines_b_count': len(lines_b) if lines_b else 0,
                'similarity_percentage': 0.0,  # Include this for consistency
                'similar_matches': [],
                'input_a': source_a,
                'input_b': source_b,
                'similarity_threshold': similarity_threshold,
                'is_file': is_file
            }
        
        # Find similar lines
        similar_matches = self.find_similar_lines(lines_a, lines_b, similarity_threshold)
        
        # Calculate statistics with improved similarity percentage
        total_lines_a = len(lines_a)
        total_lines_b = len(lines_b)
        similar_lines_count = len(similar_matches)
        
        # Calculate weighted similarity percentage based on match quality
        if similar_matches:
            # For plagiarism detection, consider both quantity and quality of matches
            # Weight matches by their similarity scores
            total_score = sum(score for _, _, score in similar_matches)
            
            # Calculate coverage for both files  
            coverage_a = (similar_lines_count / total_lines_a) * 100 if total_lines_a > 0 else 0
            coverage_b = (similar_lines_count / total_lines_b) * 100 if total_lines_b > 0 else 0
            
            # Calculate average match quality
            avg_quality = total_score / similar_lines_count if similar_lines_count > 0 else 0
            
            # Check characteristics to distinguish plagiarism from structural modifications
            high_coverage = min(coverage_a, coverage_b) > 75  # Both files well covered
            high_quality = avg_quality > 0.7
            similar_size = abs(total_lines_a - total_lines_b) / max(total_lines_a, total_lines_b) < 0.25
            
            # More nuanced similarity calculation
            if high_coverage and high_quality and similar_size:
                # Likely variable name changes (plagiarism) - boost similarity
                base_similarity = max(coverage_a, coverage_b)
                similarity_percentage = min(100.0, base_similarity * avg_quality * 1.1)
            elif avg_quality > 0.6:
                # Moderate quality matches - balanced approach
                avg_coverage = (coverage_a + coverage_b) / 2
                similarity_percentage = avg_coverage * avg_quality * 1.05
            else:
                # Lower quality or structural changes - more conservative
                avg_coverage = (coverage_a + coverage_b) / 2
                similarity_percentage = avg_coverage * avg_quality
        else:
            similarity_percentage = 0.0
        
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
            'input_a': source_a,
            'input_b': source_b,
            'is_file': is_file,
            'lines_a_count': total_lines_a,
            'lines_b_count': total_lines_b,
            'similar_lines_count': similar_lines_count,
            'similarity_percentage': round(similarity_percentage, 2),
            'average_similarity_score': round(avg_similarity, 3),
            'similarity_threshold': similarity_threshold,
            'similar_matches': similar_matches,  # Include all matches
            'similarity_distribution': dict(similarity_distribution),
            'interpretation': self._interpret_similarity(similarity_percentage, avg_similarity)
        }
        
        return results
    
    def _interpret_similarity(self, percentage: float, avg_score: float) -> str:
        """Provide interpretation of similarity results."""
        if percentage >= 90:
            return "Very High Similarity - Likely identical or minimal changes"
        elif percentage >= 70:
            return "High Similarity - Possible plagiarism or close modification"
        elif percentage >= 40:
            return "Moderate Similarity - Some common patterns or logic"
        elif percentage >= 20:
            return "Low Similarity - Limited common elements"
        else:
            return "Very Low Similarity - Largely different code"
    
    def print_detailed_report(self, results: Dict):
        """Print a focused similarity analysis report."""
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        print("=" * 80)
        print("CODE SIMILARITY ANALYSIS")
        print("=" * 80)
        input_type = "Files" if results.get('is_file', True) else "Code Fragments"
        print(f"Input Type: {input_type}")
        print(f"Input A: {results['input_a']}")
        print(f"Input B: {results['input_b']}")
        print(f"Threshold: {results['similarity_threshold']}")
        print("-" * 80)
        print(f"Meaningful Lines A: {results['lines_a_count']}")
        print(f"Meaningful Lines B: {results['lines_b_count']}")
        print(f"Matching Lines: {results['similar_lines_count']}")
        print(f"Similarity: {results['similarity_percentage']}%")
        print(f"Average Match Quality: {results['average_similarity_score']:.3f}")
        print(f"Interpretation: {results['interpretation']}")
        print("-" * 80)
        
        
        if results['similar_matches'] and len(results['similar_matches']) > 0:
            print(f"\nTop {min(10, len(results['similar_matches']))} Similar Line Matches:")
            for i, (line_a_idx, line_b_idx, score) in enumerate(results['similar_matches'][:10]):
                print(f"  {i+1}. Line {line_a_idx + 1} -> Line {line_b_idx + 1}: {score:.3f}")
        
        print("=" * 80)


def main():
    """Example usage of the CodeSimilarityAnalyzer."""
    analyzer = CodeSimilarityAnalyzer()
    
    print("Code Similarity Analyzer")
    print("1. Compare two files")
    print("2. Compare two code fragments")
    
    choice = input("\nChoose an option (1 or 2): ").strip()
    
    if choice == "2":
        # Code fragment mode
        print("\nEnter first code fragment (press Enter twice to finish):")
        code_a_lines = []
        while True:
            line = input()
            if line == "" and code_a_lines and code_a_lines[-1] == "":
                break
            code_a_lines.append(line)
        code_a = '\n'.join(code_a_lines[:-1] if code_a_lines and code_a_lines[-1] == "" else code_a_lines)
        
        print("\nEnter second code fragment (press Enter twice to finish):")
        code_b_lines = []
        while True:
            line = input()
            if line == "" and code_b_lines and code_b_lines[-1] == "":
                break
            code_b_lines.append(line)
        code_b = '\n'.join(code_b_lines[:-1] if code_b_lines and code_b_lines[-1] == "" else code_b_lines)
        
        # Get similarity threshold from user
        threshold_input = input("\nEnter similarity threshold (0.0-1.0, default 0.7): ").strip()
        threshold = float(threshold_input) if threshold_input else 0.7
        
        # Perform analysis on code fragments
        results = analyzer.analyze_code_similarity(code_a, code_b, threshold, is_file=False)
        
    else:
        # File mode (default)
        file_a = input("\nEnter path to first file (A): ").strip()
        file_b = input("Enter path to second file (B): ").strip()
        
        # Get similarity threshold from user
        threshold_input = input("Enter similarity threshold (0.0-1.0, default 0.7): ").strip()
        threshold = float(threshold_input) if threshold_input else 0.7
        
        # Perform analysis on files
        results = analyzer.analyze_code_similarity(file_a, file_b, threshold, is_file=True)
    
    # Print detailed report
    analyzer.print_detailed_report(results)
    
    # Optional: Save results to a file
    save_report = input("\nSave detailed report to file? (y/n): ").strip().lower()
    if save_report == 'y':
        import json
        if results.get('is_file', True):
            output_file = f"similarity_report_{hashlib.md5((results['input_a'] + results['input_b']).encode()).hexdigest()[:8]}.json"
        else:
            output_file = f"similarity_report_fragments_{hashlib.md5((results['input_a'] + results['input_b']).encode()).hexdigest()[:8]}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Report saved to {output_file}")


if __name__ == "__main__":
    main()