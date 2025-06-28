# Sample Python file C - copy of A with minor modifications
import math

def calculate_myarea(radius):
    """Calculate the area of a circle."""
    return math.pi * radius * radius

def greet_user_hello(name):
    """Greet a user with their name."""
    message = f"Aloha there, {name}!"  # Modified greeting
    print(message)
    return message

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def circumference(self):
        return 2 * math.pi * self.radius
    
    def diameter(self):  # Added new method
        return 2 * self.radius

if __name__ == "__main__":
    c = Circle(10)  # Changed radius
    print(f"Area: {c.area()}")
    greet_user_hello("Alice")  # Changed name
