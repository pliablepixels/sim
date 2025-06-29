import { CodeSimilarityAnalyzer } from './CodeSimilarityAnalyzer';

/**
 * Test script for the updated CodeSimilarityAnalyzer with code fragments
 */
function testNewAPI() {
    const analyzer = new CodeSimilarityAnalyzer();
    
    // Test with code fragments
    const codeA = `function helloWorld(): void {
    console.log("Hello, World!");
    return;
}`;

    const codeB = `function greet(): void {
    console.log("Hello, World!");  
    return;
}`;

    console.log("Testing code fragment analysis...");
    const results = analyzer.analyzeCodeSimilarity(codeA, codeB, 0.7, false);
    analyzer.printDetailedReport(results);
    
    console.log("\n" + "=".repeat(60));
    console.log("Testing file analysis...");
    
    // Test with files for comparison - using known sample files
    const resultsFile = analyzer.analyzeCodeSimilarity('../samples/sample_a.py', '../samples/sample_c.py', 0.7, true);
    analyzer.printDetailedReport(resultsFile);
}

testNewAPI();
