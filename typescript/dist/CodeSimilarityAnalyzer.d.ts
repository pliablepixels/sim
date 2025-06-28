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
    error?: string;
}
export declare class CodeSimilarityAnalyzer {
    private readonly commonKeywords;
    private readonly operators;
    private readonly commentPatterns;
    /**
     * Normalize a line of code by removing comments, extra whitespace, and standardizing format
     */
    private normalizeLine;
    /**
     * Extract structural features from a line of code
     */
    private extractStructuralFeatures;
    /**
     * Tokenize a line into meaningful tokens
     */
    private tokenizeLine;
    /**
     * Calculate similarity between two lines using multiple metrics
     */
    private calculateLineSimilarity;
    /**
     * Simple sequence similarity calculation (similar to difflib.SequenceMatcher)
     */
    private calculateSequenceSimilarity;
    /**
     * Read and preprocess a file, returning meaningful lines
     */
    private preprocessFile;
    /**
     * Find similar lines between two sets of lines
     */
    private findSimilarLines;
    /**
     * Analyze similarity between two code files
     */
    analyzeCodeSimilarity(fileA: string, fileB: string, similarityThreshold?: number): AnalysisResults;
    /**
     * Print a detailed similarity analysis report
     */
    printDetailedReport(results: AnalysisResults): void;
}
export {};
//# sourceMappingURL=CodeSimilarityAnalyzer.d.ts.map