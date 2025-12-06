# API Testing Guide

This guide shows how to test the Food Delivery API endpoints using different methods.

## Prerequisites

Ensure your backend is running:

```bash
cd backend
python app.py
```

Backend should be accessible at: `http://localhost:5000`

## Using cURL (Command Line)

### Get All Restaurants

```bash
curl http://localhost:5000/api/restaurants
```

### Get Specific Restaurant

```bash
curl http://localhost:5000/api/restaurants/1
```

### Get Menu Items for Restaurant

```bash
curl http://localhost:5000/api/restaurants/1/menu
```

### Create an Order

```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_id": 1,
    "items": [
      {"menu_item_id": 1, "quantity": 2},
      {"menu_item_id": 3, "quantity": 1}
    ],
    "total_price": 22.97
  }'
```

### Get All Orders

```bash
curl http://localhost:5000/api/orders
```

### Get Specific Order

```bash
curl http://localhost:5000/api/orders/1
```

### Update Order Status

```bash
curl -X PUT http://localhost:5000/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Confirmed"}'
```

### Delete Order

```bash
curl -X DELETE http://localhost:5000/api/orders/1
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

## Using Postman

1. **Import Collection**:

   - Download Postman: https://www.postman.com/downloads/
   - Create new collection named "Food Delivery API"

2. **Create Requests**:

   **GET /api/restaurants**

   - Method: GET
   - URL: `http://localhost:5000/api/restaurants`
   - Click Send

   **POST /api/orders**

   - Method: POST
   - URL: `http://localhost:5000/api/orders`
   - Headers: `Content-Type: application/json`
   - Body (raw):

   ```json
   {
     "restaurant_id": 1,
     "items": [{ "menu_item_id": 1, "quantity": 1 }],
     "total_price": 8.99
   }
   ```

   - Click Send

## Using Python Requests

```python
import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Get all restaurants
restaurants = requests.get(f'{BASE_URL}/restaurants')
print(restaurants.json())

# Get menu items
menu = requests.get(f'{BASE_URL}/restaurants/1/menu')
print(menu.json())

# Create order
order_data = {
    'restaurant_id': 1,
    'items': [
        {'menu_item_id': 1, 'quantity': 2},
        {'menu_item_id': 3, 'quantity': 1}
    ],
    'total_price': 22.97
}
order = requests.post(f'{BASE_URL}/orders', json=order_data)
print(order.json())

# Get all orders
orders = requests.get(f'{BASE_URL}/orders')
print(orders.json())
```

## Using JavaScript Fetch API

```javascript
const BASE_URL = "http://localhost:5000/api";

// Get all restaurants
fetch(`${BASE_URL}/restaurants`)
  .then((res) => res.json())
  .then((data) => console.log(data));

// Create order
const orderData = {
  restaurant_id: 1,
  items: [
    { menu_item_id: 1, quantity: 2 },
    { menu_item_id: 3, quantity: 1 },
  ],
  total_price: 22.97,
};

fetch(`${BASE_URL}/orders`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(orderData),
})
  .then((res) => res.json())
  .then((data) => console.log(data));
```

## Expected Response Examples

### Restaurants List

```json
[
  {
    "id": 1,
    "name": "Pizza Palace",
    "cuisine": "Italian",
    "rating": 4.5,
    "delivery_time": 30,
    "image_url": "https://via.placeholder.com/200?text=Pizza+Palace",
    "created_at": "2024-01-15 10:30:00"
  }
]
```

### Menu Items

```json
[
  {
    "id": 1,
    "restaurant_id": 1,
    "name": "Margherita Pizza",
    "description": "Classic pizza with tomato, mozzarella, and basil",
    "price": 8.99,
    "category": "Pizza",
    "image_url": "https://via.placeholder.com/150?text=Margherita",
    "created_at": "2024-01-15 10:30:00"
  }
]
```

### Order Response

```json
{
  "id": 1,
  "restaurant_id": 1,
  "total_price": 22.97,
  "status": "Pending",
  "message": "Order created successfully"
}
```

### All Orders

```json
[
  {
    "id": 1,
    "restaurant_id": 1,
    "total_price": 22.97,
    "status": "Pending",
    "restaurant_name": "Pizza Palace",
    "items": "Margherita Pizza x2, Garlic Bread x1",
    "created_at": "2024-01-15 11:00:00",
    "updated_at": "2024-01-15 11:00:00"
  }
]
```

## Error Responses

### 400 - Bad Request

```json
{
  "error": "Missing required fields"
}
```

### 404 - Not Found

```json
{
  "error": "Restaurant not found"
}
```

### 500 - Server Error

```json
{
  "error": "Database connection error"
}
```

## Testing Workflow

1. **Start with Restaurants**:

   ```bash
   curl http://localhost:5000/api/restaurants
   ```

   Note the restaurant IDs

2. **Get Menu Items**:

   ```bash
   curl http://localhost:5000/api/restaurants/1/menu
   ```

   Note the menu item IDs and prices

3. **Create an Order**:

   ```bash
   curl -X POST http://localhost:5000/api/orders \
     -H "Content-Type: application/json" \
     -d '{
       "restaurant_id": 1,
       "items": [{"menu_item_id": 1, "quantity": 1}],
       "total_price": 8.99
     }'
   ```

   Note the order ID

4. **Get All Orders**:

   ```bash
   curl http://localhost:5000/api/orders
   ```

   Verify your order appears

5. **Update Order Status**:

   ```bash
   curl -X PUT http://localhost:5000/api/orders/1 \
     -H "Content-Type: application/json" \
     -d '{"status": "Confirmed"}'
   ```

6. **Delete Order**:
   ```bash
   curl -X DELETE http://localhost:5000/api/orders/1
   ```

## Browser Console Testing

Open browser console (F12) and run:

```javascript
// Get restaurants
fetch("http://localhost:5000/api/restaurants")
  .then((r) => r.json())
  .then((d) => console.table(d));

// Create order
fetch("http://localhost:5000/api/orders", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    restaurant_id: 1,
    items: [{ menu_item_id: 1, quantity: 1 }],
    total_price: 8.99,
  }),
})
  .then((r) => r.json())
  .then((d) => console.log("Order created:", d));
```

## Performance Testing Tips

- Use the "Network" tab in browser DevTools to see response times
- Monitor backend console for any errors
- Check database query performance in MySQL
- Test with multiple concurrent requests using tools like Apache Bench

## Common Issues

| Issue              | Solution                                       |
| ------------------ | ---------------------------------------------- |
| CORS Error         | Backend must be running on localhost:5000      |
| Connection Refused | Check if Flask backend is running              |
| Invalid JSON       | Ensure proper JSON formatting in POST requests |
| 404 Not Found      | Verify resource IDs exist in database          |

---

For API documentation, see `README.md`
