# Complex Python Example C - Plagiarized/Modified Version of Example A
import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

# Slightly modified enum names but same concept
class Status(Enum):
    WAITING = "waiting"
    APPROVED = "approved" 
    SENT = "sent"
    RECEIVED = "received"
    CANCELED = "canceled"

@dataclass
class Item:
    product_id: str
    product_name: str
    cost: float
    category: str
    inventory_count: int
    
    def has_stock(self, needed_quantity: int = 1) -> bool:
        """Verify if item has enough inventory"""
        return self.inventory_count >= needed_quantity
    
    def update_stock(self, used_quantity: int) -> bool:
        """Update inventory if sufficient stock exists"""
        if self.has_stock(used_quantity):
            self.inventory_count -= used_quantity
            return True
        return False

@dataclass  
class PurchaseItem:
    item: Item
    amount: int
    price_each: float
    
    @property
    def item_total(self) -> float:
        return self.amount * self.price_each

class PurchaseManager:
    def __init__(self):
        self.purchase_orders: Dict[str, 'PurchaseOrder'] = {}
        self.item_catalog: Dict[str, Item] = {}
        
    def register_item(self, item: Item) -> None:
        """Register an item in the catalog"""
        self.item_catalog[item.product_id] = item
        
    def generate_order(self, buyer_id: str, requested_items: List[Dict]) -> Optional['PurchaseOrder']:
        """Generate a new purchase order with validation"""
        purchase_items = []
        grand_total = 0.0
        
        # Process and validate each requested item
        for request in requested_items:
            item_id = request.get('product_id')
            needed_amount = request.get('quantity', 1)
            
            catalog_item = self.item_catalog.get(item_id)
            if not catalog_item:
                print(f"Item {item_id} not in catalog")
                return None
                
            if not catalog_item.has_stock(needed_amount):
                print(f"Not enough inventory for {catalog_item.product_name}")
                return None
                
            purchase_item = PurchaseItem(
                item=catalog_item,
                amount=needed_amount,
                price_each=catalog_item.cost
            )
            purchase_items.append(purchase_item)
            grand_total += purchase_item.item_total
            
        # Build order when validation succeeds
        order_reference = f"PO_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{buyer_id}"
        purchase_order = PurchaseOrder(
            reference=order_reference,
            buyer_id=buyer_id,
            items=purchase_items,
            grand_total=grand_total,
            current_status=Status.WAITING,
            order_timestamp=datetime.datetime.now()
        )
        
        # Update inventory levels
        for purchase_item in purchase_items:
            purchase_item.item.update_stock(purchase_item.amount)
            
        self.purchase_orders[order_reference] = purchase_order
        return purchase_order
        
    def handle_payment(self, order_reference: str, payment_type: str) -> bool:
        """Handle payment processing for purchase order"""
        purchase_order = self.purchase_orders.get(order_reference)
        if not purchase_order or purchase_order.current_status != Status.WAITING:
            return False
            
        # Process payment
        if self._check_payment(purchase_order.grand_total, payment_type):
            purchase_order.current_status = Status.APPROVED
            purchase_order.payment_type = payment_type
            return True
        return False
        
    def _check_payment(self, total: float, payment_type: str) -> bool:
        """Check if payment is valid"""
        return total > 0 and payment_type in ['credit', 'debit', 'paypal']
        
    def send_order(self, order_reference: str, delivery_code: str) -> bool:
        """Send order for delivery"""
        purchase_order = self.purchase_orders.get(order_reference)
        if not purchase_order or purchase_order.current_status != Status.APPROVED:
            return False
            
        purchase_order.current_status = Status.SENT
        purchase_order.delivery_code = delivery_code
        purchase_order.sent_timestamp = datetime.datetime.now()
        return True

@dataclass
class PurchaseOrder:
    reference: str
    buyer_id: str
    items: List[PurchaseItem]
    grand_total: float
    current_status: Status
    order_timestamp: datetime.datetime
    payment_type: Optional[str] = None
    delivery_code: Optional[str] = None
    sent_timestamp: Optional[datetime.datetime] = None
    
    def export_data(self) -> Dict:
        """Export purchase order as dictionary"""
        return {
            'reference': self.reference,
            'buyer_id': self.buyer_id,
            'grand_total': self.grand_total,
            'current_status': self.current_status.value,
            'order_timestamp': self.order_timestamp.isoformat(),
            'items': [
                {
                    'product_id': purchase_item.item.product_id,
                    'product_name': purchase_item.item.product_name,
                    'amount': purchase_item.amount,
                    'price_each': purchase_item.price_each,
                    'item_total': purchase_item.item_total
                }
                for purchase_item in self.items
            ]
        }

# Test implementation
if __name__ == "__main__":
    manager = PurchaseManager()
    
    # Setup catalog
    catalog_items = [
        Item("COMP001", "Gaming Computer", 1299.99, "Technology", 10),
        Item("PERIPHERAL001", "Gaming Mouse", 49.99, "Technology", 50),
        Item("MANUAL001", "Programming Manual", 39.99, "Education", 25)
    ]
    
    for catalog_item in catalog_items:
        manager.register_item(catalog_item)
    
    # Generate test order
    requested_items = [
        {'product_id': 'COMP001', 'quantity': 1},
        {'product_id': 'PERIPHERAL001', 'quantity': 2}
    ]
    
    new_order = manager.generate_order("BUYER001", requested_items)
    if new_order:
        print(f"Purchase order created: {new_order.reference}")
        print(f"Total cost: ${new_order.grand_total}")
        
        # Handle payment
        if manager.handle_payment(new_order.reference, "credit"):
            print("Payment handled successfully")
            
            # Send order
            if manager.send_order(new_order.reference, "DEL123456789"):
                print("Order sent for delivery")
