// Sample Java file B - similar structure but different implementation
import java.lang.Math;
import java.util.ArrayList;
import java.util.List;

public class sample_c {
    
    /**
     * Calculate circle area using a different approach
     * @param r The radius value
     * @return Area calculation result
     */
    public static double computeCircleArea(double r) {
        // Area calculation with different variable names
        double result = Math.PI * r * r;
        return result;
    }
    
    /**
     * Display welcome message to user
     * @param name User's name for greeting
     * @return Generated welcome text
     */
    public static String displayWelcome(String name) {
        // Generate welcome message
        String welcomeText = "Greetings, " + name + "!";
        System.out.println(welcomeText);
        return welcomeText;
    }
    
    // Geometric shape class with similar functionality
    public static class GeometricCircle {
        private double r;
        
        public GeometricCircle(double radius) {
            this.r = radius;
        }
        
        public double calculateArea() {
            return Math.PI * this.r * this.r;
        }
        
        public double calculatePerimeter() {
            return 2.0 * Math.PI * this.r;
        }
        
        public double getR() {
            return this.r;
        }
        
        public void updateRadius(double newRadius) {
            this.r = newRadius;
        }
    }
    
    // Additional utility methods
    public static double calculateDiameter(double radius) {
        return radius * 2;
    }
    
    public static List<Double> calculateMultipleAreas(double[] radii) {
        List<Double> areas = new ArrayList<>();
        for (double radius : radii) {
            areas.add(computeCircleArea(radius));
        }
        return areas;
    }
    
    // Main execution method
    public static void main(String[] args) {
        // Test the functionality
        double circleArea = computeCircleArea(4.0);
        String welcome = displayWelcome("Java Developer");
        
        // Test geometric circle
        GeometricCircle shape = new GeometricCircle(2.5);
        System.out.println("Shape area: " + shape.calculateArea());
        System.out.println("Shape perimeter: " + shape.calculatePerimeter());
        
        // Test multiple calculations
        double[] testRadii = {1.0, 2.0, 3.0};
        List<Double> results = calculateMultipleAreas(testRadii);
        System.out.println("Multiple areas: " + results);
    }
}
