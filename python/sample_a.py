# Sample Python file A
import math

def calculate_area(radius):
    """Calculate the area of a circle."""
    return math.pi * radius * radius

def greet_user(name):
    """Greet a user with their name."""
    message = f"Hello, {name}!"
    print(message)
    return message

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def circumference(self):
        return 2 * math.pi * self.radius

if __name__ == "__main__":
    c = Circle(5)
    print(f"Area: {c.area()}")
    greet_user("Alice")
