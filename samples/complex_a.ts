// Complex TypeScript Example A - E-commerce Order Processing System

export enum OrderStatus {
    PENDING = "pending",
    CONFIRMED = "confirmed",
    SHIPPED = "shipped", 
    DELIVERED = "delivered",
    CANCELLED = "cancelled"
}

export interface Product {
    id: string;
    name: string;
    price: number;
    category: string;
    stockQuantity: number;
}

export interface OrderItem {
    product: Product;
    quantity: number;
    unitPrice: number;
}

export class ProductManager {
    static isAvailable(product: Product, quantity: number = 1): boolean {
        return product.stockQuantity >= quantity;
    }
    
    static reduceStock(product: Product, quantity: number): boolean {
        if (this.isAvailable(product, quantity)) {
            product.stockQuantity -= quantity;
            return true;
        }
        return false;
    }
    
    static getTotalPrice(item: OrderItem): number {
        return item.quantity * item.unitPrice;
    }
}

export class OrderProcessor {
    private orders: Map<string, Order> = new Map();
    private products: Map<string, Product> = new Map();
    
    addProduct(product: Product): void {
        this.products.set(product.id, product);
    }
    
    createOrder(customerId: string, items: Array<{productId: string, quantity: number}>): Order | null {
        const orderItems: OrderItem[] = [];
        let totalAmount = 0;
        
        // Validate and process each item
        for (const itemData of items) {
            const product = this.products.get(itemData.productId);
            if (!product) {
                console.log(`Product ${itemData.productId} not found`);
                return null;
            }
            
            if (!ProductManager.isAvailable(product, itemData.quantity)) {
                console.log(`Insufficient stock for ${product.name}`);
                return null;
            }
            
            const orderItem: OrderItem = {
                product: product,
                quantity: itemData.quantity,
                unitPrice: product.price
            };
            
            orderItems.push(orderItem);
            totalAmount += ProductManager.getTotalPrice(orderItem);
        }
        
        // Create order if all validations pass
        const orderId = `ORD_${new Date().toISOString().replace(/[-:]/g, '').slice(0, 15)}_${customerId}`;
        const order = new Order(
            orderId,
            customerId,
            orderItems,
            totalAmount,
            OrderStatus.PENDING,
            new Date()
        );
        
        // Reserve stock
        for (const item of orderItems) {
            ProductManager.reduceStock(item.product, item.quantity);
        }
        
        this.orders.set(orderId, order);
        return order;
    }
    
    processPayment(orderId: string, paymentMethod: string): boolean {
        const order = this.orders.get(orderId);
        if (!order || order.status !== OrderStatus.PENDING) {
            return false;
        }
        
        // Simulate payment processing
        if (this.validatePayment(order.totalAmount, paymentMethod)) {
            order.status = OrderStatus.CONFIRMED;
            order.paymentMethod = paymentMethod;
            return true;
        }
        return false;
    }
    
    private validatePayment(amount: number, method: string): boolean {
        const validMethods = ['credit_card', 'debit_card', 'paypal'];
        return amount > 0 && validMethods.includes(method);
    }
    
    shipOrder(orderId: string, trackingNumber: string): boolean {
        const order = this.orders.get(orderId);
        if (!order || order.status !== OrderStatus.CONFIRMED) {
            return false;
        }
        
        order.status = OrderStatus.SHIPPED;
        order.trackingNumber = trackingNumber;
        order.shippedAt = new Date();
        return true;
    }
    
    getOrder(orderId: string): Order | undefined {
        return this.orders.get(orderId);
    }
}

export class Order {
    constructor(
        public id: string,
        public customerId: string,
        public items: OrderItem[],
        public totalAmount: number,
        public status: OrderStatus,
        public createdAt: Date,
        public paymentMethod?: string,
        public trackingNumber?: string,
        public shippedAt?: Date
    ) {}
    
    toJSON(): object {
        return {
            id: this.id,
            customerId: this.customerId,
            totalAmount: this.totalAmount,
            status: this.status,
            createdAt: this.createdAt.toISOString(),
            items: this.items.map(item => ({
                productId: item.product.id,
                productName: item.product.name,
                quantity: item.quantity,
                unitPrice: item.unitPrice,
                totalPrice: ProductManager.getTotalPrice(item)
            }))
        };
    }
}

// Usage example and test data
function runDemo(): void {
    const processor = new OrderProcessor();
    
    // Add sample products
    const products: Product[] = [
        {
            id: "LAPTOP001",
            name: "Gaming Laptop",
            price: 1299.99,
            category: "Electronics",
            stockQuantity: 10
        },
        {
            id: "MOUSE001", 
            name: "Wireless Mouse",
            price: 49.99,
            category: "Electronics",
            stockQuantity: 50
        },
        {
            id: "BOOK001",
            name: "TypeScript Programming Guide",
            price: 39.99,
            category: "Books",
            stockQuantity: 25
        }
    ];
    
    products.forEach(product => processor.addProduct(product));
    
    // Create sample order
    const orderItems = [
        { productId: 'LAPTOP001', quantity: 1 },
        { productId: 'MOUSE001', quantity: 2 }
    ];
    
    const order = processor.createOrder("CUST001", orderItems);
    if (order) {
        console.log(`Order created: ${order.id}`);
        console.log(`Total amount: $${order.totalAmount}`);
        
        // Process payment
        if (processor.processPayment(order.id, "credit_card")) {
            console.log("Payment processed successfully");
            
            // Ship order
            if (processor.shipOrder(order.id, "TRK123456789")) {
                console.log("Order shipped successfully");
            }
        }
    }
}

// Execute demo
runDemo();
