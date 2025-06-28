// Sample TypeScript file A

export function calculateArea(radius: number): number {
    // Calculate the area of a circle
    return Math.PI * radius * radius;
}

export function greetUser(name: string): string {
    // Greet a user with their name
    const message = `Hello, ${name}!`;
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
}

// Main execution
const c = new Circle(5);
console.log(`Area: ${c.area()}`);
greetUser("Alice");
