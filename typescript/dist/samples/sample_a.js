"use strict";
// Sample TypeScript file A
Object.defineProperty(exports, "__esModule", { value: true });
exports.Circle = void 0;
exports.calculateArea = calculateArea;
exports.greetUser = greetUser;
function calculateArea(radius) {
    // Calculate the area of a circle
    return Math.PI * radius * radius;
}
function greetUser(name) {
    // Greet a user with their name
    const message = `Hello, ${name}!`;
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
exports.Circle = Circle;
// Main execution
const c = new Circle(5);
console.log(`Area: ${c.area()}`);
greetUser("Alice");
//# sourceMappingURL=sample_a.js.map