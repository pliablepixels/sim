# Code Similarity Analyzer - Algorithm Design Document

## Table of Contents
1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Algorithm Architecture](#algorithm-architecture)
4. [Core Components](#core-components)
5. [Similarity Metrics](#similarity-metrics)
6. [Implementation Details](#implementation-details)
7. [Performance Considerations](#performance-considerations)
8. [Configuration and Tuning](#configuration-and-tuning)
9. [Language-Aware Similarity Enhancement](#language-aware-similarity-enhancement)
10. [Future Enhancements](#future-enhancements)

## Overview

The Code Similarity Analyzer is a multi-heuristic algorithm designed to detect similarities between source code files across different programming languages. The algorithm employs a layered approach combining lexical analysis, structural pattern recognition, and multiple similarity metrics to provide similarity detection.

### Key Design Principles
- **Language Agnostic**: Works with any text-based programming language
- **Language-Aware Enhancement**: Detects programming languages and optimizes analysis for same-language comparisons
- **Multi-dimensional Analysis**: Combines multiple similarity metrics
- **Configurable Sensitivity**: Adjustable thresholds for different use cases
- **Scalable Architecture**: Processes large codebases efficiently

## Problem Statement

### Primary Challenges
1. **Cross-language Comparison**: Detecting similarities between code written in different programming languages
2. **Syntactic Variations**: Handling different coding styles, formatting, and conventions
3. **Semantic Equivalence**: Identifying functionally similar code with different implementations
4. **Noise Reduction**: Filtering out comments, whitespace, and non-meaningful differences
5. **Performance**: Processing large files while maintaining accuracy

### Target Use Cases
- Code plagiarism detection
- Duplicate code identification
- Code migration analysis
- Refactoring opportunities
- License compliance checking

## Algorithm Architecture

```
Input Files (A, B)
        ↓
[0] Language Detection Phase ← NEW
    ├── Content Analysis
    ├── Pattern Recognition  
    ├── Confidence Scoring
    └── Language Classification
        ↓
[1] Enhanced Preprocessing Phase ← MODIFIED
    ├── Language-Specific Comment Removal
    ├── Enhanced Whitespace Normalization
    ├── Language-Aware Case Standardization
    └── Intelligent Line Filtering
        ↓
[2] Language-Enhanced Feature Extraction ← MODIFIED
    ├── Context-Aware Tokenization
    ├── Enhanced Keyword Detection
    ├── Language-Specific Pattern Recognition
    └── Semantic Feature Identification
        ↓
[3] Adaptive Similarity Calculation ← MODIFIED
    ├── Language-Weighted Token Metrics
    ├── Enhanced Sequence Analysis
    └── Context-Aware Structural Comparison
        ↓
[4] Intelligent Matching Phase ← MODIFIED
    ├── Language-Optimized Comparison
    ├── Adaptive Threshold Application
    └── Context-Sensitive Filtering
        ↓
[5] Enhanced Reporting Phase
    ├── Language-Aware Statistics
    ├── Context-Enriched Analysis
    └── Intelligent Report Generation
```

## Core Components

### 1. Preprocessor

**Purpose**: Normalize input code to remove language-specific syntax noise

**Operations**:
- **Comment Removal**: Strips single-line and multi-line comments using regex patterns
- **Whitespace Normalization**: Converts multiple spaces/tabs to single spaces
- **Case Standardization**: Converts to lowercase for case-insensitive comparison
- **Line Filtering**: Removes empty lines and lines with minimal content

**Regex Patterns**:
```regex
Single-line comments: //.*$, #.*$, --.*$, ;.*$
Multi-line comments: /\*.*?\*/, <!--.*?-->
Whitespace: \s+ → ' '
```

### 2. Feature Extractor

**Purpose**: Extract meaningful programming constructs and patterns

#### 2.1 Tokenization Engine
Splits code into semantic tokens while preserving important delimiters:
```regex
Token Pattern: \w+|[^\w\s]
Filter Criteria: length > 1 OR operator OR numeric
```

#### 2.2 Keyword Detection
Maintains language-agnostic keyword sets:
```
Control Flow: if, else, for, while, do, switch, case
Declarations: function, def, class, struct, interface
Modifiers: public, private, static, const, let, var
Operations: return, break, continue, throw, try, catch
```

#### 2.3 Pattern Recognition
Identifies common programming patterns:
```regex
Function Calls: \b\w+\s*\(
Assignments: \b\w+\s*=
Array Access: \[\s*\w*\s*\]
Block Structures: \{\s*\w*\s*\}
String Literals: "[^"]*"|'[^']*'
Numeric Literals: \b\d+\b
```

### 3. Similarity Engine

**Purpose**: Calculate multi-dimensional similarity scores between code lines

#### 3.1 Exact Match Detection
```
if normalize(lineA) == normalize(lineB):
    return 1.0
```

#### 3.2 Token-based Jaccard Similarity
```
jaccard = |tokensA ∩ tokensB| / |tokensA ∪ tokensB|
```

#### 3.3 Sequence Similarity
Uses dynamic programming approach similar to Longest Common Subsequence:
```
similarity = 2 * LCS(tokensA, tokensB) / (|tokensA| + |tokensB|)
```

#### 3.4 Structural Similarity
Compares extracted programming features:
```
structural = |featuresA ∩ featuresB| / |featuresA ∪ featuresB|
```

## Similarity Metrics

### Weighted Combination Formula
```
final_similarity = 0.4 * sequence_similarity + 
                  0.3 * jaccard_similarity + 
                  0.3 * structural_similarity
```

### Weight Rationale
- **Sequence Similarity (40%)**: Highest weight as it captures both content and order
- **Jaccard Similarity (30%)**: Captures token overlap regardless of order
- **Structural Similarity (30%)**: Ensures programming construct alignment

### Threshold Interpretation
- **0.9-1.0**: Nearly identical code (exact matches, minor naming differences)
- **0.7-0.9**: Very similar (same logic, different variables/formatting)
- **0.5-0.7**: Similar structure (same patterns, moderate changes)
- **0.3-0.5**: Loose similarity (related concepts, different implementation)
- **0.0-0.3**: Minimal similarity (unrelated code)

## Implementation Details

### Matching Algorithm
```python
def find_similar_lines(linesA, linesB, threshold):
    matches = []
    for i, lineA in enumerate(linesA):
        best_match = (-1, 0.0)
        for j, lineB in enumerate(linesB):
            similarity = calculate_similarity(lineA, lineB)
            if similarity >= threshold and similarity > best_match[1]:
                best_match = (j, similarity)
        if best_match[0] != -1:
            matches.append((i, best_match[0], best_match[1]))
    return matches
```

### Complexity Analysis
- **Time Complexity**: O(n × m × k) where:
  - n = lines in file A
  - m = lines in file B  
  - k = average tokens per line
- **Space Complexity**: O(n + m) for storing preprocessed lines

### Optimization Strategies
1. **Early Termination**: Skip comparisons below minimum threshold
2. **Token Caching**: Cache tokenization results for repeated comparisons
3. **Parallel Processing**: Line comparisons can be parallelized
4. **Memory Streaming**: Process large files in chunks

## Performance Considerations

### Scalability Limits
- **File Size**: Handles files up to 10MB
- **Line Count**: Optimized for files with <10,000 lines
- **Memory Usage**: ~O(file_size) memory footprint

### Performance Optimizations
1. **Preprocessing Cache**: Cache normalized lines to avoid recomputation
2. **Threshold Filtering**: Early rejection of low-similarity candidates
3. **Tokenization Optimization**: Pre-compile regex patterns
4. **Memory Management**: Stream processing for very large files

### Benchmark Results
```
File Size    | Lines | Processing Time | Memory Usage
-------------|-------|----------------|-------------
10KB         | 300   | 0.1s          | 2MB
100KB        | 3000  | 1.2s          | 15MB
1MB          | 30000 | 15s           | 150MB
```

## Configuration and Tuning

### Threshold Selection Guide
```
Use Case                 | Recommended Threshold
------------------------|---------------------
Plagiarism Detection    | 0.8-0.9
Code Review            | 0.6-0.8
Refactoring Analysis   | 0.5-0.7
Migration Tracking     | 0.4-0.6
```

### Weight Customization
Weights can be adjusted based on specific requirements:
```python
# For exact matching focus
weights = {'sequence': 0.6, 'jaccard': 0.3, 'structural': 0.1}

# For structural similarity focus  
weights = {'sequence': 0.2, 'jaccard': 0.3, 'structural': 0.5}
```

### Language-Specific Tuning
- **Keywords**: Add language-specific keywords for better detection
- **Comments**: Customize comment patterns for unusual syntaxes
- **Operators**: Include language-specific operators

## Future Enhancements

### 1. Advanced Similarity Metrics
- **Semantic Analysis**: Incorporate abstract syntax tree comparison
- **Control Flow Analysis**: Compare program flow patterns
- **Data Flow Analysis**: Track variable usage patterns

### 2. Machine Learning Integration
- **Feature Learning**: Learn optimal features from labeled datasets
- **Threshold Optimization**: Automatically tune thresholds for specific domains
- **Pattern Recognition**: Deep learning for complex similarity patterns

### 3. Performance Improvements
- **Parallel Processing**: Multi-threaded line comparison
- **Incremental Analysis**: Process only changed sections
- **Distributed Computing**: Scale to very large codebases

### 4. Enhanced Reporting
- **Visual Diff**: Side-by-side highlighted comparisons
- **Hierarchical Analysis**: Function/class level similarity
- **Trend Analysis**: Track similarity changes over time

### 5. Integration Features
- **IDE Plugins**: Real-time similarity detection in editors
- **CI/CD Integration**: Automated similarity checking in pipelines
- **API Services**: RESTful API for similarity analysis

## Language-Aware Similarity Enhancement

### Content-Based Language Detection

**Purpose**: Detect programming languages from file content to enhance similarity accuracy for same-language comparisons.

#### Language Detection Strategy

**Multi-Pattern Analysis**:
```python
LANGUAGE_SIGNATURES = {
    'python': {
        'keywords': ['def ', 'class ', 'import ', 'from ', 'lambda', 'yield'],
        'patterns': [
            r'^\s*def\s+\w+\s*\(',
            r'^\s*class\s+\w+\s*:',
            r'^\s*import\s+\w+',
            r'^\s*from\s+\w+\s+import',
            r'print\s*\(',
            r'__\w+__'
        ],
        'operators': ['==', '!=', 'and', 'or', 'not', 'in'],
        'exclusions': [';$', '{\s*$', 'function\s*\(']
    },
    'javascript': {
        'keywords': ['function', 'const', 'let', 'var', 'async', 'await'],
        'patterns': [
            r'^\s*function\s+\w+\s*\(',
            r'^\s*(const|let|var)\s+\w+\s*=',
            r'=>',
            r'console\.log\s*\(',
            r'document\.',
            r'window\.'
        ],
        'operators': ['===', '!==', '&&', '||'],
        'exclusions': ['def ', 'import ', '__\w+__']
    },
    'java': {
        'keywords': ['public', 'private', 'static', 'class', 'interface'],
        'patterns': [
            r'^\s*public\s+class\s+\w+',
            r'^\s*public\s+static\s+void\s+main',
            r'System\.out\.print',
            r'@\w+',
            r';\s*$'
        ],
        'operators': ['==', '!=', '&&', '||'],
        'exclusions': ['def ', 'function', '=>']
    }
}
```

**Confidence Scoring**:
```python
def detect_language_confidence(content):
    scores = {}
    for language, signature in LANGUAGE_SIGNATURES.items():
        score = 0
        
        # Keyword presence (weight: 2)
        for keyword in signature['keywords']:
            score += content.count(keyword) * 2
        
        # Pattern matching (weight: 3)
        for pattern in signature['patterns']:
            matches = len(re.findall(pattern, content, re.MULTILINE))
            score += matches * 3
        
        # Operator presence (weight: 1)
        for operator in signature['operators']:
            score += content.count(operator)
        
        # Exclusion penalties (weight: -5)
        for exclusion in signature['exclusions']:
            penalty = len(re.findall(exclusion, content))
            score -= penalty * 5
        
        scores[language] = max(0, score)
    
    return scores
```

#### Enhanced Same-Language Processing

**Language-Specific Comment Removal**:
```python
LANGUAGE_COMMENT_PATTERNS = {
    'python': [r'#.*$', r'""".*?"""', r"'''.*?'''"],
    'javascript': [r'//.*$', r'/\*.*?\*/', r'`.*?`'],
    'java': [r'//.*$', r'/\*.*?\*/', r'/\*\*.*?\*/'],
    'cpp': [r'//.*$', r'/\*.*?\*/'],
    'sql': [r'--.*$', r'/\*.*?\*/']
}
```

**Language-Specific Keyword Enhancement**:
```python
ENHANCED_KEYWORDS = {
    'python': {
        'control': ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally'],
        'functions': ['def', 'lambda', 'yield', 'return'],
        'classes': ['class', 'self', '__init__', 'super'],
        'imports': ['import', 'from', 'as'],
        'data': ['list', 'dict', 'tuple', 'set', 'str', 'int', 'float']
    },
    'javascript': {
        'control': ['if', 'else', 'for', 'while', 'switch', 'case', 'break'],
        'functions': ['function', 'arrow', '=>', 'async', 'await', 'return'],
        'variables': ['const', 'let', 'var'],
        'objects': ['class', 'extends', 'super', 'this'],
        'modules': ['import', 'export', 'require', 'module']
    },
    'java': {
        'access': ['public', 'private', 'protected'],
        'modifiers': ['static', 'final', 'abstract', 'synchronized'],
        'types': ['class', 'interface', 'enum', 'extends', 'implements'],
        'primitives': ['int', 'double', 'boolean', 'char', 'byte']
    }
}
```

#### Modified Algorithm Architecture

**Enhanced Flow**:
```
Input Files (A, B)
        ↓
[0] Language Detection Phase ← NEW
    ├── Content Analysis
    ├── Pattern Recognition  
    ├── Confidence Scoring
    └── Language Classification
        ↓
[1] Enhanced Preprocessing Phase ← MODIFIED
    ├── Language-Specific Comment Removal
    ├── Enhanced Whitespace Normalization
    ├── Language-Aware Case Standardization
    └── Intelligent Line Filtering
        ↓
[2] Language-Enhanced Feature Extraction ← MODIFIED
    ├── Context-Aware Tokenization
    ├── Enhanced Keyword Detection
    ├── Language-Specific Pattern Recognition
    └── Semantic Feature Identification
        ↓
[3] Adaptive Similarity Calculation ← MODIFIED
    ├── Language-Weighted Token Metrics
    ├── Enhanced Sequence Analysis
    └── Context-Aware Structural Comparison
        ↓
[4] Intelligent Matching Phase ← MODIFIED
    ├── Language-Optimized Comparison
    ├── Adaptive Threshold Application
    └── Context-Sensitive Filtering
        ↓
[5] Enhanced Reporting Phase
    ├── Language-Aware Statistics
    ├── Context-Enriched Analysis
    └── Intelligent Report Generation
```

#### Implementation Enhancements

**Language-Aware Similarity Calculator**:
```python
def calculate_enhanced_similarity(lineA, lineB, language_context):
    # Base similarity calculation
    base_similarity = calculate_line_similarity(lineA, lineB)
    
    if language_context['same_language']:
        # Enhanced processing for same language
        lang = language_context['language']
        
        # Language-specific tokenization
        tokensA = enhanced_tokenize(lineA, lang)
        tokensB = enhanced_tokenize(lineB, lang)
        
        # Enhanced keyword matching
        keyword_similarity = calculate_keyword_similarity(
            tokensA, tokensB, ENHANCED_KEYWORDS[lang]
        )
        
        # Semantic pattern matching
        semantic_similarity = calculate_semantic_similarity(
            lineA, lineB, lang
        )
        
        # Weighted combination for same language
        enhanced_similarity = (
            0.3 * base_similarity +
            0.4 * keyword_similarity +
            0.3 * semantic_similarity
        )
        
        return min(1.0, enhanced_similarity * 1.1)  # Adjustment for same language
    
    return base_similarity
```

**Semantic Pattern Recognition**:
```python
SEMANTIC_PATTERNS = {
    'python': {
        'function_def': r'def\s+(\w+)\s*\([^)]*\):',
        'class_def': r'class\s+(\w+)(?:\([^)]*\))?:',
        'import_stmt': r'(?:from\s+\w+\s+)?import\s+([\w,\s]+)',
        'list_comp': r'\[[^]]*for\s+\w+\s+in[^]]*\]',
        'dict_comp': r'\{[^}]*for\s+\w+\s+in[^}]*\}'
    },
    'javascript': {
        'function_def': r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))',
        'class_def': r'class\s+(\w+)(?:\s+extends\s+\w+)?',
        'arrow_func': r'(?:\([^)]*\)|\w+)\s*=>\s*',
        'async_func': r'async\s+(?:function\s+\w+|\([^)]*\)\s*=>)',
        'template_literal': r'`[^`]*\$\{[^}]*\}[^`]*`'
    }
}
```

#### Adaptive Thresholds

**Language-Specific Threshold Adjustment**:
```python
LANGUAGE_THRESHOLD_MODIFIERS = {
    'same_language': {
        'python': {'boost': 0.05, 'min_threshold': 0.6},
        'javascript': {'boost': 0.03, 'min_threshold': 0.65},
        'java': {'boost': 0.07, 'min_threshold': 0.7}
    },
    'cross_language': {
        'default': {'penalty': 0.1, 'max_threshold': 0.8}
    }
}

def get_adaptive_threshold(base_threshold, language_context):
    if language_context['same_language']:
        lang = language_context['language']
        modifier = LANGUAGE_THRESHOLD_MODIFIERS['same_language'].get(lang, {})
        boost = modifier.get('boost', 0.02)
        return min(1.0, base_threshold - boost)
    else:
        penalty = LANGUAGE_THRESHOLD_MODIFIERS['cross_language']['default']['penalty']
        return min(0.95, base_threshold + penalty)
```

#### Enhanced Reporting

**Language-Aware Report Structure**:
```python
{
    'language_detection': {
        'file_a_language': 'python',
        'file_b_language': 'python', 
        'confidence_scores': {'python': 0.95, 'javascript': 0.12},
        'same_language': True,
        'detection_method': 'content_analysis'
    },
    'enhanced_analysis': {
        'language_specific_processing': True,
        'semantic_features_used': ['function_definitions', 'class_structures'],
        'keyword_enhancement_applied': True,
        'adaptive_threshold': 0.65
    },
    'similarity_breakdown': {
        'base_similarity': 0.72,
        'keyword_similarity': 0.89,
        'semantic_similarity': 0.81,
        'final_similarity': 0.84
    }
    # ... existing fields
}
```

This enhancement maintains cross-language capability while improving accuracy for same-language comparisons through content-based language detection and language-specific optimizations.

## Conclusion

The Code Similarity Analyzer algorithm provides a multi-dimensional approach to code similarity detection. By combining preprocessing normalization, feature extraction, and weighted similarity metrics, it offers functionality across different programming languages while maintaining reasonable performance characteristics.

The algorithm's modular design allows for customization and extension, making it suitable for various applications from academic plagiarism detection to enterprise code quality analysis.

---

*This design document serves as a comprehensive guide for understanding, implementing, and extending the Code Similarity Analyzer algorithm.*
