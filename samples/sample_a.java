// Sample Java file A - similar to Python sample_a.py
import java.lang.Math;

public class sample_a {
    
    /**
     * Calculate the area of a circle
     * @param radius The radius of the circle
     * @return The area of the circle
     */
    public static double calculateArea(double radius) {
        // Calculate the area using the formula: π * r²
        return Math.PI * radius * radius;
    }
    
    /**
     * Greet a user with their name
     * @param userName The name of the user to greet
     * @return The greeting message
     */
    public static String greetUser(String userName) {
        // Create a personalized greeting message
        String message = "Hello, " + userName + "!";
        System.out.println(message);
        return message;
    }
    
    // Circle class for geometric calculations
    public static class Circle {
        private double radius;
        
        public Circle(double radius) {
            this.radius = radius;
        }
        
        public double getArea() {
            return Math.PI * Math.pow(this.radius, 2);
        }
        
        public double getCircumference() {
            return 2 * Math.PI * this.radius;
        }
        
        public double getRadius() {
            return this.radius;
        }
        
        public void setRadius(double radius) {
            this.radius = radius;
        }
    }
    
    // Main method for demonstration
    public static void main(String[] args) {
        // Test the functions
        double area = calculateArea(5.0);
        String greeting = greetUser("World");
        
        // Create a circle object
        Circle myCircle = new Circle(3.0);
        System.out.println("Circle area: " + myCircle.getArea());
        System.out.println("Circle circumference: " + myCircle.getCircumference());
    }
}
