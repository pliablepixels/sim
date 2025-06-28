const { CodeSimilarityAnalyzer } = require('./typescript/dist/CodeSimilarityAnalyzer');

const analyzer = new CodeSimilarityAnalyzer();

// Simple test
const fileA = './samples/sample_a.ts';
const fileB = './samples/sample_c.ts';

console.log('Testing TypeScript Analyzer...');
try {
  const results = analyzer.analyzeCodeSimilarity(fileA, fileB, 0.5);
  console.log(`Similarity: ${results.similarityPercentage}%`);
  console.log(`Matches: ${results.similarLinesCount}`);
  console.log('TypeScript analyzer working! ✅');
} catch (error) {
  console.log('Error:', error.message);
}
