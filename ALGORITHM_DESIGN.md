# Code Similarity Analyzer - How It Works

## Table of Contents
1. [What This Tool Does](#what-this-tool-does)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [How the Algorithm Works](#how-the-algorithm-works)
4. [Step-by-Step Process](#step-by-step-process)
5. [How We Measure Similarity](#how-we-measure-similarity)
6. [Technical Implementation](#technical-implementation)
7. [Performance and Limitations](#performance-and-limitations)
8. [Configuration Options](#configuration-options)
9. [Language Detection Feature](#language-detection-feature)
10. [Possible Improvements](#possible-improvements)

## What This Tool Does

The Code Similarity Analyzer compares two code files and tells you how similar they are. It gives you a percentage score - for example, "75% similar" means the files share about three-quarters of their content or structure.

### Basic Design Goals
- **Works with any programming language**: Python, JavaScript, Java, C++, etc.
- **Detects the programming language**: Gives better results when comparing files in the same language
- **Uses multiple comparison methods**: Doesn't rely on just one way of measuring similarity
- **Can be adjusted**: You can make it more or less strict depending on what you need
- **Handles large files**: Can process reasonably sized code files without problems

## The Problem We're Solving

### What Makes Code Comparison Difficult?
1. **Different languages**: Python and Java might solve the same problem but look very different
2. **Different styles**: Some people use different spacing, variable names, or formatting
3. **Same logic, different code**: Two functions might do the same thing but be written differently
4. **Meaningless differences**: Comments, extra spaces, and formatting shouldn't affect similarity
5. **Speed**: Need to compare files quickly, even when they're large

### When You Might Use This
- Checking if someone copied code (plagiarism detection)
- Finding duplicate code in a project
- Seeing how much code changed during migration or refactoring
- Compliance checking for licensing

## How the Algorithm Works

The algorithm works like a reader comparing two books. It goes through both code files step by step, looking for similarities in different ways. Here's the basic flow:

```
Two Code Files
        ↓
Step 1: Figure Out What Programming Language Each File Uses
        ↓
Step 2: Clean Up Both Files (preserve comments and documentation for analysis)
        ↓
Step 3: Break Down Each Line Into Meaningful Parts (code and documentation tokens)
        ↓
Step 4: Compare Lines Using Four Different Methods (including documentation matching)
        ↓
Step 5: Find the Best Matches Between Files (considering content types)
        ↓
Step 6: Calculate Overall Similarity Percentage (code + documentation)
```

## Step-by-Step Process

### Step 1: Language Detection (New Feature)

**What it does**: Looks at the code content to guess what programming language it's written in.

**How it works**: The algorithm looks for clues like:
- Keywords specific to each language (`def` for Python, `function` for JavaScript)
- Common patterns (like `public static void main` in Java)
- Operators and syntax that are unique to certain languages

**Why this matters**: When both files are in the same language, we can be more precise in our comparison.

### Step 2: File Cleanup and Documentation Preservation

**What it does**: Cleans up formatting while preserving documentation and comments for similarity analysis.

**Specific actions**:
- **Preserve comments and documentation**: Extract and analyze comments separately while keeping them in context
- **Fix spacing**: Multiple spaces become single spaces
- **Standardize case**: Everything becomes lowercase for fair comparison (except within comments)
- **Remove empty lines**: Blank lines don't add meaning
- **Categorize content**: Separate code lines, comment lines, and documentation blocks

**Example**:
```
Before: 
    // Calculate area of a circle
    def   Calculate_Area(radius):    # function to get area
        """Returns the area of a circle given its radius"""
        return    3.14 * radius * radius

After (Code):
def calculate_area(radius):
return 3.14 * radius * radius

After (Documentation):
Line 1: "calculate area of a circle" (inline comment)
Line 2: "function to get area" (inline comment) 
Line 3: "returns the area of a circle given its radius" (docstring)
```

### Step 3: Breaking Down Each Line (Code and Documentation)

**What it does**: Splits each line into meaningful pieces (called "tokens") and categorizes content types.

**Content Categories**:
- **Code lines**: Actual programming logic
- **Comment lines**: Single-line comments (`//`, `#`)
- **Documentation blocks**: Multi-line comments, docstrings
- **Mixed lines**: Code with inline comments

**Types of pieces we look for**:
- **Words**: variable names, function names (`calculate`, `area`, `radius`)
- **Keywords**: language-specific words (`def`, `return`, `if`, `while`)
- **Operators**: symbols that do things (`+`, `-`, `=`, `==`)
- **Patterns**: common code structures like function calls or assignments
- **Documentation patterns**: Comment styles, docstring formats

**Example**:
```
Line: "def calculate_area(radius):  # Calculate circle area"
Code tokens: ["def", "calculate_area", "(", "radius", ")", ":"]
Comment tokens: ["calculate", "circle", "area"]
Keywords found: ["def"]
Patterns found: ["function_definition"]
Documentation pattern: ["inline_comment"]
```

### Step 4: Four Ways of Comparing Lines

We use four different methods to compare each line from File A with each line from File B, including documentation analysis:

#### Method 1: Token Matching (Jaccard Similarity)
**Simple explanation**: How many word-pieces do the two lines share?

**How it works**:
1. List all unique tokens in Line A
2. List all unique tokens in Line B  
3. Count how many tokens appear in both lines
4. Count total unique tokens across both lines
5. Similarity = (shared tokens) ÷ (total unique tokens)

**Example**:
```
Line A tokens: ["def", "calculate", "area", "radius"]
Line B tokens: ["def", "compute", "area", "value"]

Shared tokens: ["def", "area"] = 2 tokens
Total unique tokens: ["def", "calculate", "area", "radius", "compute", "value"] = 6 tokens
Similarity: 2 ÷ 6 = 0.33 (33%)
```

#### Method 2: Sequence Matching
**Simple explanation**: How similar are the lines when we consider the order of tokens?

**How it works**:
1. Compare tokens in order, like comparing two sentences word by word
2. Find the longest sequence of tokens that appear in the same order in both lines
3. Calculate similarity based on how much of each line is covered by matching sequences

**Example**:
```
Line A: ["if", "x", "==", "5", "print", "hello"]
Line B: ["if", "y", "==", "5", "print", "world"]

Matching sequences: ["if"], ["==", "5"], ["print"]
Coverage: 4 out of 6 tokens match in sequence
Similarity: 4 ÷ 6 = 0.67 (67%)
```

#### Method 3: Structure Matching
**Simple explanation**: Do the lines have similar programming structures?

**How it works**:
1. Look for programming patterns in each line (function calls, assignments, etc.)
2. Compare what types of programming constructs each line contains
3. Calculate similarity based on shared programming patterns

**Example**:
```
Line A: "result = calculate_area(radius)"
Line B: "answer = compute_size(width)"

Both lines have:
- Variable assignment pattern
- Function call pattern
- Same overall structure

Similarity: High (maybe 80%) because structure is very similar
```

#### Method 4: Documentation Matching (NEW)
**Simple explanation**: How similar are the comments and documentation?

**How it works**:
1. Extract comments, docstrings, and documentation from both lines
2. Compare the meaning and content of the documentation
3. Look for similar explanations, parameter descriptions, and purpose statements
4. Calculate similarity based on shared documentation concepts

**Example**:
```
Line A: "def calculate_area(radius):  # Computes circle area"
Line B: "def compute_area(r):        # Calculates area of circle"

Documentation A: ["computes", "circle", "area"]
Documentation B: ["calculates", "area", "of", "circle"]

Shared concepts: ["area", "circle"] and synonyms ["computes"/"calculates"]
Documentation similarity: High (maybe 85%) - same purpose explained
```

**Example**:
```
Line A: ["if", "x", "==", "5", "print", "hello"]
Line B: ["if", "y", "==", "5", "print", "world"]

Matching sequences: ["if"], ["==", "5"], ["print"]
Coverage: 4 out of 6 tokens match in sequence
Similarity: 4 ÷ 6 = 0.67 (67%)
```

#### Method 3: Structure Matching
**Simple explanation**: Do the lines have similar programming structures?

**How it works**:
1. Look for programming patterns in each line (function calls, assignments, etc.)
2. Compare what types of programming constructs each line contains
3. Calculate similarity based on shared programming patterns

**Example**:
```
Line A: "result = calculate_area(radius)"
Line B: "answer = compute_size(width)"

Both lines have:
- Variable assignment pattern
- Function call pattern
- Same overall structure

Similarity: High (maybe 80%) because structure is very similar
```

### Step 5: Finding the Best Matches

**What it does**: For each line in File A, find the most similar line in File B, considering both code and documentation.

**How it works**:
1. Take Line 1 from File A
2. Compare it to every line in File B using our four methods
3. Combine the four similarity scores into one final score
4. Give extra weight to lines that have similar content types (code-to-code, comment-to-comment)
5. Pick the line from File B with the highest score (if it's above our threshold)
6. Repeat for all lines in File A

**Content Type Matching**:
- **Code-to-code**: Standard comparison using all four methods
- **Comment-to-comment**: Emphasizes documentation matching
- **Mixed-to-mixed**: Compares both code and comment portions
- **Cross-type matching**: Reduced weight when comparing code to comments

**Important rule**: Each line can only be matched once. If Line 1 from File A matches Line 5 from File B, then Line 5 can't be matched to any other line.

### Step 6: Calculate Overall Similarity

**What it does**: Gives you a final percentage showing how similar the two files are.

**How it works**:
```
Similarity Percentage = (Number of matched lines) ÷ (Total lines in File A) × 100

Example:
- File A has 20 meaningful lines
- We found good matches for 15 of those lines
- Similarity = 15 ÷ 20 × 100 = 75%
```

## How We Measure Similarity

### Combining the Four Methods

Each line comparison gives us four separate similarity scores. We combine them using a weighted average:

```
Final Score = (30% × Sequence Score) + (25% × Token Score) + (25% × Structure Score) + (20% × Documentation Score)
```

**Why these weights?**
- **Sequence (30%)**: Still gets high weight because code order usually matters
- **Token (25%)**: Important for catching renamed variables or similar logic
- **Structure (25%)**: Helps identify code that does the same thing differently  
- **Documentation (20%)**: Significant weight for comments and documentation similarity

**Content Type Adjustments**:
- **Pure comment lines**: Documentation gets 50% weight, others split the remaining 50%
- **Code with inline comments**: Standard weights as above
- **Pure code lines**: Documentation weight redistributed to other methods

**Example calculation**:
```
Line A: "if x == 5: print('hello')  # Check condition and print"
Line B: "if y == 5: print('world')  # Verify condition and output"

Sequence Score: 0.7 (most tokens in same order)
Token Score: 0.6 (some shared words)
Structure Score: 0.9 (identical programming structure)
Documentation Score: 0.8 (very similar comment meaning)

Final Score = (0.3 × 0.7) + (0.25 × 0.6) + (0.25 × 0.9) + (0.2 × 0.8)
            = 0.21 + 0.15 + 0.225 + 0.16
            = 0.745 (74.5% similar)
```

### Understanding Similarity Levels

**90-100% Similar**: Almost identical code and documentation
- Only small differences like variable names, with very similar or identical comments
- Example: `area = pi * r * r  # Calculate area` vs `surface = 3.14 * radius * radius  # Compute area`

**70-89% Similar**: Very similar code with moderate changes, similar documentation intent
- Same logic with different variable names, comments explain same concepts
- Example: Same algorithm with different variable names but equivalent documentation

**50-69% Similar**: Similar structure and approach, documentation covers similar topics
- Same general approach but noticeable differences, related documentation themes
- Example: Two different sorting methods with comments explaining similar algorithmic concepts

**30-49% Similar**: Some similarities in code or documentation but mostly different
- Maybe solving same problem differently, or similar documentation style but different content
- Example: Different algorithms with comments that mention similar programming concepts

**0-29% Similar**: Little to no similarity in code or documentation
- Completely different code solving different problems with unrelated documentation
- Example: A sorting function with optimization comments vs a web scraping function with HTTP documentation

### Threshold Settings

A "threshold" is the minimum similarity score we accept for a match. Think of it like setting how picky the algorithm should be:

- **High threshold (0.8-0.9)**: Very picky, only finds very similar lines (including documentation)
- **Medium threshold (0.5-0.7)**: Balanced, finds reasonably similar lines with related documentation
- **Low threshold (0.3-0.5)**: Less picky, finds even loosely similar lines or documentation concepts

### Documentation Analysis Features

The enhanced algorithm now provides detailed documentation analysis:

**What it analyzes**:
- **Comment similarity**: How similar are inline comments and single-line comments
- **Documentation style**: Whether files use consistent documentation patterns
- **API documentation**: Similarity in function/method documentation
- **Code explanation**: Whether comments explain similar concepts

**Documentation matching examples**:
```
High similarity (90%+):
Line A: "# Calculate the area of a circle"
Line B: "# Compute the area of a circle"

Medium similarity (60-80%):
Line A: "# Returns circle area"  
Line B: "# Gets the surface area"

Low similarity (20-40%):
Line A: "# Main calculation function"
Line B: "# Helper method for processing"
```

**Benefits of documentation analysis**:
- **Better plagiarism detection**: Catches cases where code is copied with similar comments
- **Code review insights**: Identifies whether documentation standards are followed consistently
- **Refactoring analysis**: Shows if code changes preserved documentation intent
- **Learning pattern detection**: Reveals if developers explain concepts similarly

## Technical Implementation

### The Matching Process (Simplified)

Here's how the algorithm actually compares the files:

```python
# Simplified version of the matching algorithm
def find_similar_lines(file_a_lines, file_b_lines, threshold):
    matches = []
    used_lines_in_b = set()  # Keep track of which lines we've already matched
    
    for line_number_a, line_a in enumerate(file_a_lines):
        best_match = None
        best_score = 0
        
        for line_number_b, line_b in enumerate(file_b_lines):
            if line_number_b in used_lines_in_b:
                continue  # Skip lines we've already matched
            
            similarity_score = compare_lines(line_a, line_b)
            
            if similarity_score >= threshold and similarity_score > best_score:
                best_match = line_number_b
                best_score = similarity_score
        
        if best_match is not None:
            matches.append((line_number_a, best_match, best_score))
            used_lines_in_b.add(best_match)
    
    return matches
```

### How Fast Is It?

**Time complexity**: The algorithm needs to compare every line in File A with every line in File B. So if File A has 100 lines and File B has 200 lines, it makes 100 × 200 = 20,000 comparisons.

**Memory usage**: The algorithm keeps both files in memory, plus some extra space for processing. For most code files, this isn't a problem.

**Typical performance**:
- Small files (under 1,000 lines): Under 1 second
- Medium files (1,000-5,000 lines): 1-10 seconds  
- Large files (5,000-10,000 lines): 10-60 seconds

### Making It Faster

The algorithm includes several optimizations:

1. **Early stopping**: If a line comparison is clearly going to be low, stop calculating early
2. **Caching**: Remember results from previous calculations to avoid redoing work
3. **Skip obvious non-matches**: Don't compare lines that are obviously different (like very different lengths)

## Performance and Limitations

### What Works Well
- **Files up to 10,000 lines**: Handles most real-world code files fine
- **Most programming languages**: Works with Python, JavaScript, Java, C++, etc.
- **Different coding styles**: Handles different formatting and naming conventions
- **Moderate changes**: Good at finding code that's been modified but kept similar structure

### Current Limitations
- **Very large files**: Files over 10,000 lines might be slow
- **Completely restructured code**: If someone completely rewrites code to do the same thing, might not detect similarity
- **Cross-language detection**: Better at comparing files in the same language than different languages
- **Memory usage**: Keeps entire files in memory, so very large files could be problematic

### When Results Might Be Misleading

**False positives** (high similarity when code is actually different):
- Files with lots of boilerplate code (imports, basic setup) and standard comments
- Very simple code where many solutions look similar
- Code with lots of repeated patterns or similar documentation styles
- Standard documentation templates that appear across different functions

**False negatives** (low similarity when code is actually similar):
- Code that's been heavily refactored or restructured with completely rewritten documentation
- Same algorithm implemented very differently with different comment styles
- Code where variable names, structure, and documentation have been completely changed

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
# For exact matching focus (emphasize sequence and structure)
weights = {'sequence': 0.5, 'token': 0.2, 'structural': 0.2, 'documentation': 0.1}

# For documentation similarity focus (useful for API documentation comparison)
weights = {'sequence': 0.2, 'token': 0.2, 'structural': 0.2, 'documentation': 0.4}

# For structural similarity focus  
weights = {'sequence': 0.2, 'token': 0.2, 'structural': 0.4, 'documentation': 0.2}
```

### Language-Specific Tuning
- **Keywords**: Add language-specific keywords for better detection
- **Comments**: Customize comment patterns for unusual syntaxes
- **Operators**: Include language-specific operators

## Future Enhancements

### 1. Additional Similarity Metrics
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

**Language-Specific Comment Preservation and Analysis**:
```python
LANGUAGE_COMMENT_PATTERNS = {
    'python': {
        'single_line': r'#(.*)$',
        'docstring': r'"""(.*?)"""',
        'docstring_alt': r"'''(.*?)'''",
        'inline': r'#\s*(.+)$'
    },
    'javascript': {
        'single_line': r'//(.*)$', 
        'block': r'/\*(.*?)\*/',
        'jsdoc': r'/\*\*(.*?)\*/',
        'inline': r'//\s*(.+)$'
    },
    'java': {
        'single_line': r'//(.*)$',
        'block': r'/\*(.*?)\*/', 
        'javadoc': r'/\*\*(.*?)\*/',
        'inline': r'//\s*(.+)$'
    },
    'cpp': {
        'single_line': r'//(.*)$',
        'block': r'/\*(.*?)\*/',
        'inline': r'//\s*(.+)$'
    },
    'sql': {
        'single_line': r'--(.*)$',
        'block': r'/\*(.*?)\*/',
        'inline': r'--\s*(.+)$'
    }
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
    ├── Language-Specific Comment Extraction and Preservation
    ├── Enhanced Whitespace Normalization
    ├── Language-Aware Case Standardization
    ├── Line Filtering
    └── Documentation Categorization
        ↓
[2] Language-Enhanced Feature Extraction ← MODIFIED
    ├── Context-Aware Tokenization
    ├── Enhanced Keyword Detection
    ├── Language-Specific Pattern Recognition
    ├── Semantic Feature Identification
    └── Documentation Pattern Extraction
        ↓
[3] Adaptive Similarity Calculation ← MODIFIED
    ├── Language-Weighted Token Metrics
    ├── Enhanced Sequence Analysis
    ├── Context-Aware Structural Comparison
    └── Documentation Content Analysis
        ↓
[4] Matching Phase ← MODIFIED
    ├── Language-Optimized Comparison
    ├── Content-Type-Aware Matching
    ├── Adaptive Threshold Application
    └── Context-Sensitive Filtering
        ↓
[5] Enhanced Reporting Phase
    ├── Language-Aware Statistics
    ├── Documentation Analysis Results
    ├── Context-Enriched Analysis
    └── Report Generation
```

#### Implementation Enhancements

**Language-Aware Similarity Calculator with Documentation**:
```python
def calculate_enhanced_similarity(lineA, lineB, language_context):
    # Base similarity calculation (code analysis)
    base_similarity = calculate_line_similarity(lineA, lineB)
    
    # Documentation similarity calculation
    doc_similarity = calculate_documentation_similarity(lineA, lineB, language_context)
    
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
        
        # Weighted combination for same language (including documentation)
        enhanced_similarity = (
            0.25 * base_similarity +
            0.3 * keyword_similarity +
            0.25 * semantic_similarity +
            0.2 * doc_similarity
        )
        
        return min(1.0, enhanced_similarity * 1.1)  # Adjustment for same language
    else:
        # Cross-language comparison with documentation
        cross_lang_similarity = (
            0.3 * base_similarity +
            0.25 * keyword_similarity +
            0.25 * semantic_similarity +
            0.2 * doc_similarity
        )
        return cross_lang_similarity

def calculate_documentation_similarity(lineA, lineB, language_context):
    """Calculate similarity between documentation/comments in two lines"""
    lang = language_context.get('language', 'generic')
    
    # Extract documentation from both lines
    docsA = extract_documentation(lineA, lang)
    docsB = extract_documentation(lineB, lang)
    
    if not docsA and not docsB:
        return 0.0  # No documentation to compare
    
    if not docsA or not docsB:
        return 0.0  # Only one has documentation
    
    # Compare documentation content using text similarity
    return calculate_text_similarity(docsA, docsB)
```

**Semantic Pattern Recognition with Documentation**:
```python
SEMANTIC_PATTERNS = {
    'python': {
        'function_def': r'def\s+(\w+)\s*\([^)]*\):',
        'class_def': r'class\s+(\w+)(?:\([^)]*\))?:',
        'import_stmt': r'(?:from\s+\w+\s+)?import\s+([\w,\s]+)',
        'list_comp': r'\[[^]]*for\s+\w+\s+in[^]]*\]',
        'dict_comp': r'\{[^}]*for\s+\w+\s+in[^}]*\}',
        'docstring': r'"""([^"]*?)"""',
        'comment': r'#\s*(.+)$'
    },
    'javascript': {
        'function_def': r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))',
        'class_def': r'class\s+(\w+)(?:\s+extends\s+\w+)?',
        'arrow_func': r'(?:\([^)]*\)|\w+)\s*=>\s*',
        'async_func': r'async\s+(?:function\s+\w+|\([^)]*\)\s*=>)',
        'template_literal': r'`[^`]*\$\{[^}]*\}[^`]*`',
        'jsdoc': r'/\*\*(.*?)\*/',
        'comment': r'//\s*(.+)$'
    },
    'java': {
        'method_def': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)',
        'class_def': r'(?:public|private)?\s*class\s+(\w+)',
        'interface_def': r'(?:public)?\s*interface\s+(\w+)',
        'javadoc': r'/\*\*(.*?)\*/',
        'comment': r'//\s*(.+)$'
    }
}

def extract_documentation_patterns(line, language):
    """Extract documentation and comment patterns from a line"""
    patterns = SEMANTIC_PATTERNS.get(language, {})
    documentation = []
    
    # Extract different types of documentation
    for pattern_name, pattern in patterns.items():
        if pattern_name in ['docstring', 'comment', 'jsdoc', 'javadoc']:
            matches = re.findall(pattern, line, re.DOTALL)
            documentation.extend(matches)
    
    return documentation
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

**Language-Aware Report Structure with Documentation Analysis**:
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
        'documentation_analysis_enabled': True,
        'adaptive_threshold': 0.65
    },
    'similarity_breakdown': {
        'base_similarity': 0.72,
        'keyword_similarity': 0.89,
        'semantic_similarity': 0.81,
        'documentation_similarity': 0.76,
        'final_similarity': 0.84
    },
    'documentation_analysis': {
        'total_documented_lines_a': 12,
        'total_documented_lines_b': 15,
        'matching_documentation': 8,
        'documentation_similarity_avg': 0.67,
        'comment_style_consistency': 0.89
    },
    'content_breakdown': {
        'code_only_matches': 25,
        'comment_only_matches': 8,
        'mixed_content_matches': 12,
        'documentation_block_matches': 3
    }
    # ... existing fields
}
```

This enhancement maintains cross-language capability while improving accuracy for same-language comparisons through content-based language detection and language-specific optimizations.

## Conclusion

The Code Similarity Analyzer algorithm provides a multi-dimensional approach to code similarity detection. By combining preprocessing normalization, feature extraction, and weighted similarity metrics, it offers functionality across different programming languages while maintaining reasonable performance characteristics.

The algorithm's modular design allows for customization and extension, making it suitable for various applications from academic plagiarism detection to enterprise code quality analysis.

---

*This document explains how the Code Similarity Analyzer algorithm works and how to implement it.*
