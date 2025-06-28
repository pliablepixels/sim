// Sample JavaScript file B - similar structure but different language
const math = require('math');

function calculateArea(r) {
    // Calculate the area of a circle
    return Math.PI * r * r;
}

function greetUser(userName) {
    // Greet a user with their name
    const message = `Hello, ${userName}!`;
    console.log(message);
    return message;
}

class Circle {
    constructor(radius) {
        this.radius = radius;
    }
    
    area() {
        return Math.PI * this.radius ** 2;
    }
    
    circumference() {
        return 2 * Math.PI * this.radius;
    }
}

// Main execution
const c = new Circle(5);
console.log(`Area: ${c.area()}`);
greetUser("Alice");
