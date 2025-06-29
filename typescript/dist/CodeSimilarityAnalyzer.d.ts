interface SimilarMatch {
    lineAIndex: number;
    lineBIndex: number;
    score: number;
}
interface AnalysisResults {
    fileA: string;
    fileB: string;
    linesACount: number;
    linesBCount: number;
    similarLinesCount: number;
    similarityPercentage: number;
    averageSimilarityScore: number;
    similarityThreshold: number;
    similarMatches: SimilarMatch[];
    similarityDistribution: Record<string, number>;
    interpretation: string;
    error?: string;
}
/**
 * A focused code similarity analyzer for detecting similar code within the same programming language.
 * Optimized for accuracy in plagiarism detection and identifying code modifications.
 *
 * This TypeScript implementation mirrors the Python version exactly.
 */
export declare class CodeSimilarityAnalyzer {
    private readonly structuralKeywords;
    private readonly operators;
    /**
     * Normalize a line of code for comparison (mirrors Python version exactly)
     */
    private normalizeLine;
    /**
     * Extract key structural features from a line of code for same-language comparison
     */
    private extractStructuralFeatures;
    /**
     * Tokenize a line into meaningful code tokens
     */
    private tokenizeLine;
    /**
     * Calculate sequence similarity similar to Python's difflib.SequenceMatcher
     */
    private calculateSequenceSimilarity;
    /**
     * Calculate string similarity using approach similar to Python's difflib
     */
    private calculateStringSimilarity;
    /**
     * Calculate similarity between two lines of the same programming language (exact Python mirror)
     */
    private calculateLineSimilarity;
    /**
     * Check if a line is too trivial to be meaningful for comparison
     */
    private isTrivialLine;
    /**
     * Read and preprocess a file, extracting meaningful code lines
     */
    private preprocessFile;
    /**
     * Find similar lines between two sets of lines using optimal matching (exact Python mirror)
     */
    private findSimilarLines;
    /**
     * Provide interpretation of similarity results
     */
    private interpretSimilarity;
    /**
     * Analyze similarity between two code files (exact Python mirror)
     */
    analyzeCodeSimilarity(fileA: string, fileB: string, similarityThreshold?: number): AnalysisResults;
    /**
     * Print a focused similarity analysis report
     */
    printDetailedReport(results: AnalysisResults): void;
}
export {};
//# sourceMappingURL=CodeSimilarityAnalyzer.d.ts.map