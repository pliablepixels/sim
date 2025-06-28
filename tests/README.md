# Testing Guide for Code Similarity Analyzer

This document provides comprehensive information about testing the Code Similarity Analyzer in its primary use case: measuring how much of a user's final code originates from suggestions, even after user modifications.

## Primary Use Case: Code Attribution Analysis

The analyzer helps organizations and developers understand code influence by detecting similarity between:
- Original suggested code (baseline)
- User's final code after modifications

This enables:
- Development analytics and insights
- Code contribution attribution 
- Understanding coding patterns and adoption
- Quality metrics for assisted development

## Test Scenarios & Expected Behavior

The test suite validates the analyzer's accuracy across realistic suggestion scenarios:

- **Identical Code**: User accepted suggestion as-is → 90-100% similarity
- **Modified Code**: User renamed variables, added comments → 70-90% similarity
- **Refactored Code**: User restructured but kept core logic → 40-70% similarity  
- **Inspired Code**: User rewrote using different approach → 20-40% similarity
- **Original User Code**: No external influence detected → 0-20% similarity

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
## Sample Files for Code Attribution Testing

### Simple Samples (sample_a, sample_c)
- Basic functions and classes
- 15-25 lines of code  
- Simulates simple suggestions and user modifications
- Good for testing basic similarity detection

### Complex Samples (complex_a, complex_b, complex_c)
- E-commerce order processing systems
- 150+ lines of code
- Multiple classes, enums, interfaces
- Simulates real-world assisted development scenarios
- **complex_a**: Original suggested implementation
- **complex_b**: User's alternative approach (inspired)
- **complex_c**: User's modified version of complex_a (variable renames, comments)

## Running Python Tests

### Prerequisites
```bash
cd tests
python3 -m pip install --user unittest  # Usually included with Python
```

### Execute Test Suite
```bash
# Run comprehensive test suite for code attribution analysis
python3 test_similarity_analyzer.py

# Run with verbose output to see detailed influence metrics
python3 -m unittest test_similarity_analyzer.TestCodeSimilarityAnalyzer -v
```

### Expected Output - Code Attribution Analysis
```
Starting Code Similarity Analysis Test Suite...
============================================================
✅ Identical code (user accepted as-is): 95.0% similarity
✅ Modified code (variable renames + comments): 78.3% similarity  
✅ Refactored code (structural changes): 45.2% similarity
✅ Inspired code (different approach): 28.7% similarity
✅ Original user code (no external influence): 12.4% similarity
✅ Complex modification analysis: 82.1% similarity
✅ Complex inspired implementation: 34.6% similarity
✅ Edge cases for attribution completed

============================================================
CODE INFLUENCE ANALYSIS REPORT
============================================================

Suggestion vs User's Final Code:
  Comparing: complex_a.py (baseline) vs complex_c.py (user modified)
  High Confidence (90%+): 45.3% of code directly from suggestion
  Medium Confidence (70%+): 68.2% of code influenced  
  Low Confidence (50%+): 75.8% of code potentially derived
  
  Analysis: User significantly modified suggestions while retaining core structure
```

## Running TypeScript Tests

### Prerequisites
```bash
cd typescript
npm install --save-dev @types/node @types/fs
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

# Run code attribution test suite
node dist/tests/test_similarity_analyzer.js
```

## Understanding Code Attribution Results

### Code Influence Score Ranges

| Range | Influence Level | Interpretation |
|-------|-----------------|----------------|
| 90-100% | Direct Copy | User accepted suggestion unchanged |
| 70-90% | Heavy Influence | User made minor modifications (variables, comments) |
| 40-70% | Moderate Influence | User refactored but kept core logic |
| 20-40% | Light Influence | User was inspired but implemented differently |
| 0-20% | No Influence | Original user code or unrelated to suggestion |

### Key Code Attribution Metrics

1. **Code Influence Percentage**: Overall percentage of influenced code
2. **Confidence Levels**: High/Medium/Low confidence in attribution  
3. **Modification Patterns**: Types of changes made to suggestions
4. **Retention Analysis**: Which parts of code were preserved vs. modified

### Code Attribution Test Scenarios

#### 1. Direct Code Acceptance
**Purpose**: User accepted suggestion unchanged
**Expected**: 90-100% influence
```python
# Suggested:                  # User's final code:
def calculate_tax(amount):    def calculate_tax(amount):
    tax_rate = 0.08               tax_rate = 0.08
    return amount * tax_rate      return amount * tax_rate
```

#### 2. Code with Variable Renames  
**Purpose**: User modified suggestion with better naming
**Expected**: 70-90% influence
```python
# Suggested:                  # User's final code:
def calc_tax(amt):           def calculate_tax(amount):
    rate = 0.08                  tax_rate = 0.08
    return amt * rate            return amount * tax_rate
```

#### 3. Code Refactored
**Purpose**: User restructured suggestion while keeping logic
**Expected**: 40-70% influence
```python
# Suggested:                  # User's final code:
def process_order(items):    class OrderProcessor:
    total = 0                    def calculate_total(self, items):
    for item in items:               total = 0
        total += item.price          for item in items:
    return total                         total += item.price
                                     return total
```

#### 4. Inspired Implementation
**Purpose**: User wrote different approach inspired by suggestion
**Expected**: 20-40% influence
```python
# Suggested:                  # User's final code:
def quicksort(arr):          def merge_sort(arr):
    if len(arr) <= 1:            if len(arr) <= 1:
        return arr                   return arr
    pivot = arr[0]               mid = len(arr) // 2
    # ... quicksort logic      # ... merge sort logic
```

#### 5. Original User Code
**Purpose**: User wrote code without assistance
**Expected**: 0-20% influence
```python
# Baseline:                   # User's original code:
def web_scraper():           def data_processor():
    import requests              import pandas as pd
    # scraping logic           # data processing logic
```

## Interpreting Complex Attribution Results

### Complex A vs Complex C (Code Modified)
- **complex_c.py** represents user's modified version of suggested **complex_a.py**
- Variable names improved: `Order` → `PurchaseOrder`, `customer_id` → `buyer_id`
- Method names clarified: `create_order` → `generate_order`
- Comments and documentation added
- **Expected Result**: 70-85% influence (heavy contribution with user improvements)

### Complex A vs Complex B (Inspired Implementation)
- Both implement e-commerce order processing
- User saw suggestion (complex_a) but implemented own approach (complex_b)
- Similar domain concepts but distinct implementations  
- **Expected Result**: 25-45% influence (light inspiration, mostly original)

## Confidence Level Analysis

The analyzer provides multi-level confidence analysis for attribution:

```python
# Multi-threshold analysis for confidence
thresholds = [0.5, 0.7, 0.9]  # Low, Medium, High confidence
```

### Confidence Level Guidelines

| Threshold | Confidence Level | Attribution Interpretation |
|-----------|-----------------|----------------------------|
| 0.5-0.6 | Low Confidence | Possible influence, needs review |
| 0.7-0.8 | Medium Confidence | Likely derived with modifications |
| 0.9+ | High Confidence | Clear contribution, minimal changes |

## Use Cases for Code Attribution Analysis

### 1. Development Analytics
```bash
# Analyze team's AI adoption patterns
python3 analyze_ai_influence.py --team-repo /path/to/repo --ai-baseline /copilot/suggestions
```

### 2. Code Review Enhancement
```bash
# Identify AI-influenced code for focused review
python3 ai_attribution.py --pr-diff --highlight-ai-sections
```

### 3. Learning and Training
```bash
# Understand how developers modify AI suggestions
python3 modification_patterns.py --ai-baseline --user-final --output-report
```

### 4. Quality Metrics
```bash
# Measure AI suggestion adoption rates
python3 ai_metrics.py --suggestions-accepted --modifications-made --custom-implementations
```

## Troubleshooting AI Attribution Tests

### Common Issues

1. **False Positives in AI Detection**
   - Review threshold settings - may be too low
   - Check for common coding patterns vs. actual AI influence
   - Validate AI baseline accuracy

2. **False Negatives in AI Detection**
   - User may have significantly refactored AI code
   - Consider structural similarity vs. line-by-line matching
   - Review for algorithmic similarities despite different syntax

3. **Inconsistent Results**
   - Ensure AI baseline represents actual suggestions provided
   - Account for user's coding style vs. AI patterns
   - Consider temporal factors (AI suggestions change over time)

### Debugging AI Attribution

```python
# Detailed AI influence analysis
def debug_ai_attribution(self):
    results = self.analyze_ai_influence(ai_baseline, user_code, thresholds=[0.5, 0.7, 0.9])
    
    print(f"AI Influence Summary:")
    print(f"  High confidence: {results['high_confidence_percentage']:.1f}%")
    print(f"  Medium confidence: {results['medium_confidence_percentage']:.1f}%") 
    print(f"  Low confidence: {results['low_confidence_percentage']:.1f}%")
    print(f"  Modification patterns: {results['modification_types']}")
```

## Continuous AI Attribution Monitoring

### CI/CD Integration

```yaml
# GitHub Actions example for AI attribution tracking
- name: Analyze AI Code Influence
  run: |
    python3 ai_attribution_analysis.py \
      --baseline-dir ai_suggestions/ \
      --user-code-dir src/ \
      --output-report ai_influence_report.json
      
- name: Update AI Metrics Dashboard
  run: |
    python3 update_dashboard.py --report ai_influence_report.json
```

### Performance Benchmarks for AI Attribution

Expected analysis times:
- Simple AI attribution (< 50 lines): 1-3 seconds
- Complex AI attribution (150+ lines): 3-8 seconds
- Batch AI analysis (multiple files): 30-120 seconds

## Best Practices for AI Attribution

1. **Establish AI Baselines**: Maintain accurate records of AI suggestions
2. **Regular Analysis**: Run attribution analysis after significant code changes
3. **Context Awareness**: Consider development context when interpreting results
4. **Team Training**: Help developers understand AI influence patterns
5. **Quality Focus**: Use insights to improve AI-assisted development processes

## Contributing AI Attribution Tests

### Adding New AI Scenarios

```python
def test_ai_code_with_error_handling(self):
    """Test AI code where user added error handling"""
    ai_baseline = """
    def fetch_data(url):
        response = requests.get(url)
        return response.json()
    """
    
    user_final = """
    def fetch_data(url):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            return None
    """
    
    # Expected: 60-75% AI influence (core logic retained, error handling added)
    results = self.analyze_ai_influence(ai_baseline, user_final, 0.7)
    self.assertGreaterEqual(results['ai_influence_percentage'], 60)
    self.assertLessEqual(results['ai_influence_percentage'], 75)
```

### Documenting AI Patterns

When adding new test cases, document:
1. **AI suggestion context**: What the AI originally suggested
2. **User modification type**: How and why the user changed it
3. **Expected influence level**: What percentage indicates good detection
4. **Business context**: Why this scenario matters for AI attribution

## Support and Resources

For AI attribution analysis questions:
1. Review AI baseline accuracy and completeness
2. Validate user code represents actual final implementation
3. Consider development workflow and timing factors
4. Refer to algorithm documentation for scoring methodology
5. Contact development team for organization-specific AI usage patterns
