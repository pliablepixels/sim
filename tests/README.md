# Testing Guide for Code Similarity Analyzer

This document provides comprehensive information about testing the Code Similarity Analyzer to ensure it behaves correctly across various scenarios.

## Overview

The test suite validates the analyzer's accuracy in detecting different types of code similarities:

- **Identical Code**: Should score 90-100% similarity
- **Plagiarized Code**: Variable/method name changes, should score 70-90% 
- **Structural Changes**: Class/function restructuring, should score 40-70%
- **Different Implementations**: Same logic, different approach, should score 20-40%
- **Unrelated Code**: Completely different functionality, should score 0-20%

## Test Files Structure

```
├── tests/
│   ├── test_similarity_analyzer.py      # Python test suite
│   ├── test_similarity_analyzer.ts      # TypeScript test suite
│   └── README.md                        # This documentation
├── samples/
│   ├── simple samples (existing)
│   ├── complex_a.py/.ts                 # Complex e-commerce system
│   ├── complex_b.py/.ts                 # Alternative implementation
│   └── complex_c.py                     # Plagiarized version of A
```

## Sample Complexity Levels

### Simple Samples (sample_a, sample_c)
- Basic functions and classes
- 15-25 lines of code
- Good for testing basic similarity detection

### Complex Samples (complex_a, complex_b, complex_c)
- E-commerce order processing systems
- 150+ lines of code
- Multiple classes, enums, interfaces
- Real-world scenario testing

## Running Python Tests

### Prerequisites
```bash
cd tests
python3 -m pip install --user unittest  # Usually included with Python
```

### Execute Test Suite
```bash
# Run comprehensive test suite
python3 test_similarity_analyzer.py

# Run with verbose output
python3 -m unittest test_similarity_analyzer.TestCodeSimilarityAnalyzer -v
```

### Expected Output
```
Starting Code Similarity Analyzer Test Suite...
============================================================
✅ Identical code test: 95.0% similarity
✅ Variable name changes test: 78.3% similarity  
✅ Structural modifications test: 45.2% similarity
✅ Different implementations test: 28.7% similarity
✅ Unrelated code test: 12.4% similarity
✅ Complex samples (plagiarism) test: 82.1% similarity
✅ Complex samples (different implementations) test: 34.6% similarity
✅ Edge cases test completed

============================================================
COMPREHENSIVE SIMILARITY ANALYSIS REPORT
============================================================

Original vs Plagiarized:
  Comparing: complex_a.py vs complex_c.py
  Threshold 0.5: 75.8% (89/117 lines matched)
  Threshold 0.7: 68.2% (67/117 lines matched)
  Threshold 0.9: 45.3% (23/117 lines matched)
```

## Running TypeScript Tests

### Prerequisites
```bash
cd typescript
npm install --save-dev @types/node @types/fs
```

### Build and Execute
```bash
# Build the analyzer
npm run build

# Run test suite (requires Node.js environment)
node dist/tests/test_similarity_analyzer.js
```

## Understanding Test Results

### Similarity Score Ranges

| Range | Interpretation | Use Case |
|-------|---------------|----------|
| 90-100% | Identical/Near-identical | Copy detection |
| 70-90% | High similarity | Plagiarism detection |
| 40-70% | Moderate similarity | Code review, refactoring |
| 20-40% | Some similarity | Related functionality |
| 0-20% | Low/No similarity | Different codebases |

### Key Metrics

1. **Similarity Percentage**: Overall percentage of similar lines
2. **Average Similarity Score**: Mean score of matched lines
3. **Match Count**: Number of lines that exceeded threshold
4. **Score Distribution**: Breakdown by similarity ranges

### Test Scenarios Explained

#### 1. Identical Code Detection
**Purpose**: Verify perfect matches are detected
**Expected**: >90% similarity
```python
# Both files contain exactly the same code
def hello(): print("world")
```

#### 2. Variable Name Changes (Plagiarism)
**Purpose**: Detect code with renamed variables/functions
**Expected**: 70-90% similarity
```python
# Original                    # Modified
def calc_area(radius):        def calc_area(r):
    pi = 3.14159                 pi_val = 3.14159
    return pi * radius ** 2      return pi_val * r ** 2
```

#### 3. Structural Modifications
**Purpose**: Detect reorganized/refactored code
**Expected**: 40-70% similarity
```python
# Original: Single class      # Modified: Separate classes
class Calculator:            class MathOps:
    def add(self, a, b):         def add(self, a, b):
        return a + b                 return a + b
    def multiply(self, a, b):    
        return a * b             class Calculator:
                                     def __init__(self):
                                         self.math = MathOps()
```

#### 4. Different Implementations
**Purpose**: Compare different algorithms for same task
**Expected**: 20-40% similarity
```python
# Iterative Fibonacci        # Recursive Fibonacci
def fib_iter(n):             def fib_rec(n):
    a, b = 0, 1                  if n <= 1:
    for i in range(n):               return n
        a, b = b, a + b          return fib_rec(n-1) + fib_rec(n-2)
    return a
```

#### 5. Unrelated Code
**Purpose**: Verify different domains show low similarity
**Expected**: 0-20% similarity
```python
# Web scraping               # Mathematical operations
import requests             import numpy as np
def scrape_url(url):        def matrix_multiply(a, b):
    response = requests.get(url)  return np.dot(a, b)
```

## Interpreting Complex Sample Results

### Complex A vs Complex C (Plagiarism Detection)
- **complex_c.py** is a deliberately plagiarized version of **complex_a.py**
- Variable names changed: `Order` → `PurchaseOrder`, `customer_id` → `buyer_id`
- Method names changed: `create_order` → `generate_order`
- Enum values changed: `PENDING` → `WAITING`
- **Expected Result**: 70-85% similarity

### Complex A vs Complex B (Different Implementations)
- Both implement e-commerce order processing
- Different class structures and approaches
- Similar domain concepts but distinct implementations
- **Expected Result**: 25-45% similarity

## Threshold Sensitivity Testing

The test suite evaluates how different thresholds affect detection:

```python
# Testing with multiple thresholds
thresholds = [0.3, 0.5, 0.7, 0.9]
# Expected: Higher thresholds → Fewer matches
```

### Threshold Selection Guidelines

| Threshold | Use Case | Description |
|-----------|----------|-------------|
| 0.3-0.4 | Broad detection | Catch loose similarities |
| 0.5-0.6 | Balanced detection | Good general purpose |
| 0.7-0.8 | Strict detection | Focus on clear similarities |
| 0.9+ | Exact matching | Near-identical code only |

## Troubleshooting Tests

### Common Issues

1. **Import Errors**
   ```bash
   # Python
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   
   # TypeScript
   npm install @types/node
   ```

2. **File Not Found**
   - Ensure you're running tests from the correct directory
   - Check that sample files exist in `samples/` directory

3. **Unexpected Results**
   - Review the specific test output
   - Check if sample files were modified
   - Verify analyzer implementation hasn't changed

### Debugging Individual Tests

```python
# Run specific test method
python3 -m unittest test_similarity_analyzer.TestCodeSimilarityAnalyzer.test_identical_code_detection

# Add debug output
def test_debug_similarity(self):
    results = self.analyze_similarity(code_a, code_b, 0.7)
    print(f"Debug: {results}")
    self.analyzer.print_detailed_report(results)
```

## Continuous Integration

### Adding to CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
- name: Run Similarity Tests
  run: |
    cd tests
    python3 test_similarity_analyzer.py
    
- name: Test TypeScript Similarity
  run: |
    cd typescript
    npm run build
    npm run test
```

### Performance Benchmarks

Expected test execution times:
- Python test suite: 5-15 seconds
- TypeScript test suite: 10-20 seconds
- Complex sample analysis: 2-5 seconds per comparison

## Contributing New Tests

### Adding Test Cases

1. **Create test method** following naming convention `test_<scenario>`
2. **Use appropriate assertions** with descriptive messages
3. **Test edge cases** and boundary conditions
4. **Document expected results** in method docstring

```python
def test_my_scenario(self):
    """Test description and expected behavior"""
    code_a = "..."
    code_b = "..."
    results = self.analyze_similarity(code_a, code_b, threshold)
    
    self.assertGreaterEqual(results['similarity_percentage'], expected_min)
    self.assertLessEqual(results['similarity_percentage'], expected_max)
    print(f"✅ My scenario test: {results['similarity_percentage']:.1f}% similarity")
```

### Adding Sample Files

1. **Follow naming convention**: `complex_<letter>.py/.ts`
2. **Document the scenario** in file header comments
3. **Ensure realistic complexity** (100+ lines)
4. **Add corresponding test methods**

## Best Practices

1. **Regular Testing**: Run tests after any analyzer modifications
2. **Baseline Establishment**: Document expected ranges for your use case
3. **Version Control**: Track test results over time
4. **Documentation**: Update this guide when adding new test scenarios
5. **Peer Review**: Have others validate test expectations

## Support

For questions about the test suite:
1. Review this documentation
2. Check test output and error messages
3. Examine sample files for expected patterns
4. Refer to the main Algorithm Design Document
