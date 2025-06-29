/**
 * Comprehensive Test Suite for TypeScript Code Similarity Analyzer
 *
 * This test suite validates the accuracy and behavior of the Code Similarity Analyzer
 * with various TypeScript scenarios including:
 * - Identical code detection
 * - Plagiarism detection (modified variable names, structure changes)
 * - Different implementations of same functionality
 * - Unrelated code detection
 * - Edge cases and boundary conditions
 *
 * Usage:
 *   npm run build && npm run test
 *
 * The test suite provides detailed assertions and reporting to help developers
 * understand how the similarity analyzer behaves in different scenarios.
 */
export declare class TypeScriptSimilarityTester {
    private analyzer;
    private samplesDir;
    private testResults;
    constructor();
    private createTempFile;
    private analyzeSimilarity;
    private assert;
    testIdenticalCodeDetection(): void;
    testVariableNameChanges(): void;
    testStructuralModifications(): void;
    testDifferentImplementationsSameLogic(): void;
    testCompletelyUnrelatedCode(): void;
    testComplexSamplesSimilarity(): void;
    testThresholdSensitivity(): void;
    testEdgeCases(): void;
    runAllTests(): void;
    private generateTestReport;
    testPercentageAndCountReporting(): void;
}
export declare function runTypeScriptTests(): void;
//# sourceMappingURL=test_similarity_analyzer.d.ts.map