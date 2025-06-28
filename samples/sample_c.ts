// Sample TypeScript file C - copy of A with minor modifications

export function calculateMyArea(radius: number): number {
    // Calculate the area of a circle
    return Math.PI * radius * radius;
}

export function greetUserHello(name: string): string {
    // Greet a user with their name
    const message = `Aloha there, ${name}!`; // Modified greeting
    console.log(message);
    return message;
}

export class Circle {
    private radius: number;

    constructor(radius: number) {
        this.radius = radius;
    }

    area(): number {
        return Math.PI * this.radius ** 2;
    }

    circumference(): number {
        return 2 * Math.PI * this.radius;
    }

    diameter(): number { // Added new method
        return 2 * this.radius;
    }
}

// Main execution
const circleC = new Circle(10); // Changed radius
console.log(`Area: ${circleC.area()}`);
greetUserHello("Alice"); // Changed name
