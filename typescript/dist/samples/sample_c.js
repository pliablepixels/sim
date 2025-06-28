"use strict";
// Sample TypeScript file C - copy of A with minor modifications
Object.defineProperty(exports, "__esModule", { value: true });
exports.Circle = void 0;
exports.calculateMyArea = calculateMyArea;
exports.greetUserHello = greetUserHello;
function calculateMyArea(radius) {
    // Calculate the area of a circle
    return Math.PI * radius * radius;
}
function greetUserHello(name) {
    // Greet a user with their name
    const message = `Aloha there, ${name}!`; // Modified greeting
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
    diameter() {
        return 2 * this.radius;
    }
}
exports.Circle = Circle;
// Main execution
const circleC = new Circle(10); // Changed radius
console.log(`Area: ${circleC.area()}`);
greetUserHello("Alice"); // Changed name
//# sourceMappingURL=sample_c.js.map