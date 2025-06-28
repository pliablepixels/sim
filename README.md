# Code Similarity Analyzer

A comprehensive code similarity analyzer that can compare source code files across different programming languages using multiple heuristics. Available in both **Python** and **TypeScript** implementations.

## Features

- **Multi-language Support**: Works with any programming language (Python, JavaScript, Java, C++, etc.)
- **Dual Implementation**: Choose between Python and TypeScript versions
- **Intelligent Normalization**: Removes comments, normalizes whitespace, and standardizes format
- **Multiple Similarity Metrics**: 
  - Token-based Jaccard similarity
  - Sequence similarity using difflib
  - Structural feature matching
- **Configurable Thresholds**: Adjust sensitivity to find exact matches or loose similarities
- **Detailed Reporting**: Get comprehensive analysis with line-by-line comparisons

## Project Structure

```
├── README.md            # Main documentation
├── ALGORITHM_DESIGN.md  # Detailed algorithm design document
├── python/              # Python implementation
│   ├── demo.py         # Demo script for Python version
│   ├── try.py          # Main analyzer class
│   ├── sample_a.py     # Sample Python file A
│   ├── sample_b.js     # Sample JavaScript file
│   └── sample_c.py     # Sample Python file C (modified copy of A)
└── typescript/         # TypeScript implementation
    ├── package.json    # NPM configuration
    ├── tsconfig.json   # TypeScript configuration
    ├── src/
    │   ├── CodeSimilarityAnalyzer.ts  # Main analyzer class
    │   ├── demo.ts                    # Demo script
    │   └── samples/
    │       ├── sample_a.ts           # Sample TypeScript file A
    │       └── sample_c.ts           # Sample TypeScript file C
    └── dist/           # Compiled JavaScript files
```

## Algorithm Overview

The `CodeSimilarityAnalyzer` uses a multi-layered approach:

1. **Preprocessing**: 
   - Removes comments using language-specific patterns
   - Normalizes whitespace and converts to lowercase
   - Filters out empty and meaningless lines

2. **Feature Extraction**:
   - Identifies programming keywords (`if`, `for`, `class`, etc.)
   - Detects operators (`+`, `=`, `==`, etc.)
   - Recognizes common patterns (function calls, assignments, etc.)

3. **Similarity Calculation**:
   - **Sequence Similarity** (40%): Uses difflib for token sequence matching
   - **Jaccard Similarity** (30%): Measures token set overlap
   - **Structural Similarity** (30%): Compares programming constructs

4. **Matching**: Finds best matches between lines using configurable thresholds

> 📖 **For detailed algorithm explanation, see [ALGORITHM_DESIGN.md](ALGORITHM_DESIGN.md)**

## Getting Started

### Python Implementation

#### Prerequisites
- Python 3.7+

#### Running the Demo
```bash
cd python
python demo.py
```

#### Basic Usage
```python
from try import CodeSimilarityAnalyzer

analyzer = CodeSimilarityAnalyzer()
results = analyzer.analyze_code_similarity('file_a.py', 'file_b.js', threshold=0.7)
analyzer.print_detailed_report(results)
```

### TypeScript Implementation

#### Prerequisites
- Node.js 16+
- npm

#### Setup
```bash
cd typescript
npm install
npm run build
```

#### Running the Demo
```bash
npm start
# or for development mode:
npm run dev
```

#### Basic Usage
```typescript
import { CodeSimilarityAnalyzer } from './src/CodeSimilarityAnalyzer';

const analyzer = new CodeSimilarityAnalyzer();
const results = analyzer.analyzeCodeSimilarity('file1.ts', 'file2.ts', 0.7);
analyzer.printDetailedReport(results);
```

## Available Scripts (TypeScript)

- `npm run build` - Compile TypeScript to JavaScript
- `npm start` - Run the compiled demo
- `npm run dev` - Run demo in development mode with ts-node
- `npm run demo` - Build and run demo
- `npm run clean` - Remove compiled files

## Sample Results

When comparing a Python file and its JavaScript equivalent:

```
============================================================
CODE SIMILARITY ANALYSIS REPORT
============================================================
File A: sample_a.py
File B: sample_b.js
Similarity Threshold: 0.7
--------------------------------------------------------
Lines in File A: 20
Lines in File B: 17
Similar Lines Found: 6
Similarity Percentage: 30.0%
Average Similarity Score: 0.896
--------------------------------------------------------
Top Similar Line Matches (Line A -> Line B, Score):
  Line 4 -> Line 3: 0.873
  Line 9 -> Line 7: 1.000
  Line 10 -> Line 8: 1.000
```

## Configuration Options

- **similarity_threshold** (0.0-1.0): Minimum similarity score to consider lines similar
  - 0.9+: Nearly identical code
  - 0.7-0.9: Very similar with minor modifications
  - 0.5-0.7: Similar structure with moderate changes
  - <0.5: Loose structural similarity

## Output Information

The analyzer provides:

- **Similarity Percentage**: % of lines in file A that have similar matches in file B
- **Average Similarity Score**: Mean similarity score of all matches
- **Similarity Distribution**: Breakdown of matches by similarity ranges
- **Line-by-Line Matches**: Detailed mapping of similar lines with scores
- **Detailed Comparisons**: Side-by-side view of matching lines

## Documentation

- **[ALGORITHM_DESIGN.md](ALGORITHM_DESIGN.md)** - Comprehensive algorithm design document
  - Detailed explanation of similarity metrics
  - Performance analysis and optimization strategies
  - Configuration guidelines and tuning recommendations
  - Future enhancement roadmap

## Use Cases

1. **Code Review**: Detect potential code duplication
2. **Plagiarism Detection**: Compare student submissions
3. **Code Migration**: Track changes when porting between languages
4. **Refactoring Analysis**: Identify similar code patterns for consolidation
5. **License Compliance**: Check for copied code from external sources

## Technical Details

- **Languages Supported**: Any text-based programming language
- **Comment Detection**: C-style (//,/**/), Python (#), HTML (<!---->), SQL (--)
- **Token Recognition**: Alphanumeric tokens, operators, and delimiters
- **Memory Efficient**: Processes files line-by-line, suitable for large files

## Files Included

- `try.py`: Main CodeSimilarityAnalyzer class
- `demo.py`: Interactive demonstration script
- `sample_a.py`: Sample Python file for testing
- `sample_b.js`: Sample JavaScript file (equivalent functionality)
- `sample_c.py`: Modified Python file for testing
- `README.md`: This documentation

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## License

MIT License - Feel free to use and modify for your projects.
