# Complex Python Example B - E-commerce Order Management (Alternative Implementation)
import json
import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid

class OrderState(Enum):
    NEW = "new"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    REFUNDED = "refunded"

@dataclass
class Item:
    sku: str
    title: str
    cost: float
    category_name: str
    available_stock: int
    
    def check_stock(self, requested_qty: int = 1) -> bool:
        """Verify if item has enough stock available"""
        return self.available_stock >= requested_qty
    
    def decrease_inventory(self, qty: int) -> bool:
        """Decrease inventory if stock is sufficient"""
        if self.check_stock(qty):
            self.available_stock -= qty
            return True
        return False

@dataclass  
class LineItem:
    item: Item
    qty: int
    price_per_unit: float
    
    @property
    def line_total(self) -> float:
        return self.qty * self.price_per_unit

class ShoppingCartManager:
    def __init__(self):
        self.customer_orders: Dict[str, 'CustomerOrder'] = {}
        self.inventory: Dict[str, Item] = {}
        
    def register_item(self, item: Item) -> None:
        """Register an item in the inventory system"""
        self.inventory[item.sku] = item
        
    def place_order(self, user_id: str, cart_items: List[Dict]) -> Optional['CustomerOrder']:
        """Place a new customer order with inventory validation"""
        line_items = []
        order_total = 0.0
        
        # Process each cart item
        for cart_item in cart_items:
            sku = cart_item.get('sku')
            requested_qty = cart_item.get('qty', 1)
            
            inventory_item = self.inventory.get(sku)
            if not inventory_item:
                print(f"Item with SKU {sku} not available")
                return None
                
            if not inventory_item.check_stock(requested_qty):
                print(f"Not enough stock for {inventory_item.title}")
                return None
                
            line_item = LineItem(
                item=inventory_item,
                qty=requested_qty,
                price_per_unit=inventory_item.cost
            )
            line_items.append(line_item)
            order_total += line_item.line_total
            
        # Generate order if validation successful
        order_number = str(uuid.uuid4())
        customer_order = CustomerOrder(
            order_id=order_number,
            user_id=user_id,
            line_items=line_items,
            order_total=order_total,
            current_state=OrderState.NEW,
            order_date=datetime.datetime.now()
        )
        
        # Update inventory
        for line_item in line_items:
            line_item.item.decrease_inventory(line_item.qty)
            
        self.customer_orders[order_number] = customer_order
        return customer_order
        
    def handle_payment(self, order_number: str, payment_type: str) -> bool:
        """Handle payment processing for order"""
        customer_order = self.customer_orders.get(order_number)
        if not customer_order or customer_order.current_state != OrderState.NEW:
            return False
            
        # Payment validation
        if self._process_payment_method(customer_order.order_total, payment_type):
            customer_order.current_state = OrderState.PROCESSING
            customer_order.payment_type = payment_type
            return True
        return False
        
    def _process_payment_method(self, total: float, payment_type: str) -> bool:
        """Process payment using specified method"""
        valid_methods = ['visa', 'mastercard', 'amex', 'paypal', 'apple_pay']
        return total > 0 and payment_type in valid_methods
        
    def dispatch_order(self, order_number: str, shipment_id: str) -> bool:
        """Dispatch order for shipping"""
        customer_order = self.customer_orders.get(order_number)
        if not customer_order or customer_order.current_state != OrderState.PROCESSING:
            return False
            
        customer_order.current_state = OrderState.SHIPPED
        customer_order.shipment_id = shipment_id
        customer_order.dispatch_date = datetime.datetime.now()
        return True
        
    def get_order_summary(self, order_number: str) -> Optional[Dict]:
        """Get comprehensive order summary"""
        customer_order = self.customer_orders.get(order_number)
        if not customer_order:
            return None
            
        return {
            'order_id': customer_order.order_id,
            'customer': customer_order.user_id,
            'total': customer_order.order_total,
            'status': customer_order.current_state.value,
            'order_date': customer_order.order_date.isoformat(),
            'items_purchased': [
                {
                    'sku': line.item.sku,
                    'name': line.item.title,
                    'quantity': line.qty,
                    'unit_cost': line.price_per_unit,
                    'subtotal': line.line_total
                }
                for line in customer_order.line_items
            ]
        }

@dataclass
class CustomerOrder:
    order_id: str
    user_id: str
    line_items: List[LineItem]
    order_total: float
    current_state: OrderState
    order_date: datetime.datetime
    payment_type: Optional[str] = None
    shipment_id: Optional[str] = None
    dispatch_date: Optional[datetime.datetime] = None
    
    def export_to_json(self) -> str:
        """Export order details as JSON string"""
        order_dict = {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'order_total': self.order_total,
            'current_state': self.current_state.value,
            'order_date': self.order_date.isoformat()
        }
        return json.dumps(order_dict, indent=2)

# Demonstration and testing
def run_demo():
    cart_manager = ShoppingCartManager()
    
    # Setup inventory
    test_items = [
        Item("COMP001", "High-End Gaming PC", 2499.99, "Computers", 5),
        Item("KEY001", "Mechanical Keyboard", 129.99, "Accessories", 30),
        Item("MON001", "4K Gaming Monitor", 599.99, "Displays", 15)
    ]
    
    for item in test_items:
        cart_manager.register_item(item)
    
    # Simulate customer purchase
    shopping_cart = [
        {'sku': 'COMP001', 'qty': 1},
        {'sku': 'KEY001', 'qty': 1},
        {'sku': 'MON001', 'qty': 2}
    ]
    
    new_order = cart_manager.place_order("USER123", shopping_cart)
    if new_order:
        print(f"New order placed: {new_order.order_id}")
        print(f"Order value: ${new_order.order_total}")
        
        # Complete payment
        if cart_manager.handle_payment(new_order.order_id, "visa"):
            print("Payment completed successfully")
            
            # Ship the order
            if cart_manager.dispatch_order(new_order.order_id, "SHIP789"):
                print("Order dispatched for delivery")
                
                # Display order summary
                summary = cart_manager.get_order_summary(new_order.order_id)
                if summary:
                    print(f"Order summary: {json.dumps(summary, indent=2)}")

if __name__ == "__main__":
    run_demo()
