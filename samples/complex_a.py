# Complex Python Example A - E-commerce Order Processing System
import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed" 
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str
    stock_quantity: int
    
    def is_available(self, quantity: int = 1) -> bool:
        """Check if product has sufficient stock"""
        return self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock if available, return success status"""
        if self.is_available(quantity):
            self.stock_quantity -= quantity
            return True
        return False

@dataclass  
class OrderItem:
    product: Product
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

class OrderProcessor:
    def __init__(self):
        self.orders: Dict[str, 'Order'] = {}
        self.products: Dict[str, Product] = {}
        
    def add_product(self, product: Product) -> None:
        """Add a product to the inventory"""
        self.products[product.id] = product
        
    def create_order(self, customer_id: str, items: List[Dict]) -> Optional['Order']:
        """Create a new order with validation"""
        order_items = []
        total_amount = 0.0
        
        # Validate and process each item
        for item_data in items:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            
            product = self.products.get(product_id)
            if not product:
                print(f"Product {product_id} not found")
                return None
                
            if not product.is_available(quantity):
                print(f"Insufficient stock for {product.name}")
                return None
                
            order_item = OrderItem(
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
            order_items.append(order_item)
            total_amount += order_item.total_price
            
        # Create order if all validations pass
        order_id = f"ORD_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{customer_id}"
        order = Order(
            id=order_id,
            customer_id=customer_id,
            items=order_items,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            created_at=datetime.datetime.now()
        )
        
        # Reserve stock
        for item in order_items:
            item.product.reduce_stock(item.quantity)
            
        self.orders[order_id] = order
        return order
        
    def process_payment(self, order_id: str, payment_method: str) -> bool:
        """Process payment for an order"""
        order = self.orders.get(order_id)
        if not order or order.status != OrderStatus.PENDING:
            return False
            
        # Simulate payment processing
        if self._validate_payment(order.total_amount, payment_method):
            order.status = OrderStatus.CONFIRMED
            order.payment_method = payment_method
            return True
        return False
        
    def _validate_payment(self, amount: float, method: str) -> bool:
        """Validate payment details (simplified)"""
        return amount > 0 and method in ['credit_card', 'debit_card', 'paypal']
        
    def ship_order(self, order_id: str, tracking_number: str) -> bool:
        """Mark order as shipped"""
        order = self.orders.get(order_id)
        if not order or order.status != OrderStatus.CONFIRMED:
            return False
            
        order.status = OrderStatus.SHIPPED
        order.tracking_number = tracking_number
        order.shipped_at = datetime.datetime.now()
        return True

@dataclass
class Order:
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    created_at: datetime.datetime
    payment_method: Optional[str] = None
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime.datetime] = None
    
    def to_dict(self) -> Dict:
        """Convert order to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'total_amount': self.total_amount,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'items': [
                {
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'total_price': item.total_price
                }
                for item in self.items
            ]
        }

# Usage example and test data
if __name__ == "__main__":
    processor = OrderProcessor()
    
    # Add sample products
    products = [
        Product("LAPTOP001", "Gaming Laptop", 1299.99, "Electronics", 10),
        Product("MOUSE001", "Wireless Mouse", 49.99, "Electronics", 50),
        Product("BOOK001", "Python Programming Guide", 39.99, "Books", 25)
    ]
    
    for product in products:
        processor.add_product(product)
    
    # Create sample order
    order_items = [
        {'product_id': 'LAPTOP001', 'quantity': 1},
        {'product_id': 'MOUSE001', 'quantity': 2}
    ]
    
    order = processor.create_order("CUST001", order_items)
    if order:
        print(f"Order created: {order.id}")
        print(f"Total amount: ${order.total_amount}")
        
        # Process payment
        if processor.process_payment(order.id, "credit_card"):
            print("Payment processed successfully")
            
            # Ship order
            if processor.ship_order(order.id, "TRK123456789"):
                print("Order shipped successfully")
