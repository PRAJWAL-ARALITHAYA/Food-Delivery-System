# 🍕 FoodHub - Online Food Delivery System

A full-stack web application for ordering food from multiple restaurants with real-time order management.

## 📋 Quick Start (Windows)

### Step 1: Setup Database (One-time only)

Double-click `setup_db.bat` to initialize the SQLite database.

### Step 2: Start Backend Server

Double-click `run_backend.bat` to start the Flask backend on `http://localhost:5000`

### Step 3: Start Frontend Server (In a new terminal/window)

Double-click `run_frontend.bat` to start the React app on `http://localhost:3000`

### Step 4: Open in Browser

Navigate to: **http://localhost:3000**

---

## 🛠️ Manual Setup (Command Line)

### Prerequisites

- Python 3.11+ installed
- Node.js & npm installed
- Git (optional)

### Installation

```bash
# 1. Navigate to project directory
cd "c:\Users\Kanna\Documents\5th_sem\DBMS\Food App"

# 2. Initialize database (one time)
python init_db.py

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt

# 4. Install frontend dependencies
cd ..\frontend
npm install
```

### Running the Application

**Terminal 1 - Backend:**

```bash
cd backend
python app.py
```

Backend will start on: `http://localhost:5000`

**Terminal 2 - Frontend:**

```bash
cd frontend
npm start
```

Frontend will open on: `http://localhost:3000`

---

## 📚 Features

### Frontend (React)

- **Home Page** - Browse 5 restaurants with ratings & delivery time
- **Menu Page** - View menu items with prices & descriptions
- **Shopping Cart** - Add/remove items before checkout
- **Orders Page** - View all orders with status tracking
- **Manage Items** - Add or remove items from placed orders
- **Edit Status** - Update order status (Pending → Delivered)

### Backend (Flask)

- **REST API** with 15+ endpoints
- **CORS enabled** for frontend communication
- **SQLite Database** with 4 tables (restaurants, menu_items, orders, order_items)
- **Order Management** - Create, update, delete orders
- **Item Management** - Add/remove items from existing orders
- **Automatic Price Calculation** - Total price updates in real-time

---

## 🎯 Usage Guide

### Placing an Order

1. Click on a restaurant from the Home page
2. Select items and add to cart
3. View cart and proceed to checkout
4. Confirm order (Status: Pending)

### Managing Orders

1. Go to "My Orders" page
2. Click "Manage Items" button to:
   - View current items in order
   - Remove items (price updates automatically)
   - Add new items from restaurant menu
3. Click "Edit" to change order status
4. Click "Delete" to cancel order

---

## 📊 Database Schema

### Restaurants

```
id (int, PK)
name (string)
cuisine (string)
rating (float)
delivery_time (int)
image_url (string)
```

### Menu Items

```
id (int, PK)
restaurant_id (int, FK)
name (string)
description (text)
price (decimal)
image_url (string)
category (string)
```

### Orders

```
id (int, PK)
restaurant_id (int, FK)
total_price (decimal)
status (string)
created_at (timestamp)
updated_at (timestamp)
```

### Order Items

```
id (int, PK)
order_id (int, FK)
menu_item_id (int, FK)
quantity (int)
price (decimal)
```

---

## 🔧 API Endpoints

### Restaurants

- `GET /api/restaurants` - List all restaurants
- `GET /api/restaurants/:id` - Get restaurant details

### Menu

- `GET /api/restaurants/:id/menu` - Get restaurant menu items
- `GET /api/menu/:id` - Get specific menu item

### Orders

- `GET /api/orders` - List all orders
- `GET /api/orders/:id` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/:id` - Update order status
- `DELETE /api/orders/:id` - Delete order

### Order Items

- `POST /api/orders/:id/items` - Add item to order
- `DELETE /api/orders/:id/items/:itemId` - Remove item from order

### Health

- `GET /api/health` - Health check

---

## ⚙️ Technology Stack

| Layer        | Technology                   |
| ------------ | ---------------------------- |
| **Frontend** | React 18, Bootstrap 5, Axios |
| **Backend**  | Flask 2.3.3, Flask-CORS      |
| **Database** | SQLite 3                     |
| **Runtime**  | Python 3.11, Node.js 16+     |

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if database exists
ls backend/food_delivery.db

# If missing, reinitialize
python init_db.py
```

### Port already in use

```bash
# Find process on port 5000 (backend)
netstat -ano | findstr :5000

# Find process on port 3000 (frontend)
netstat -ano | findstr :3000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Frontend shows "Failed to fetch restaurants"

- Ensure backend is running on `http://localhost:5000`
- Check browser console (F12) for errors
- Verify CORS is enabled in Flask

---

## 📝 Sample Data

Database comes preloaded with:

- **5 Restaurants**: Pizza Palace, Burger Bistro, Sushi Supreme, Taco Fiesta, Curry House
- **20 Menu Items**: 4 items per restaurant
- **Sample Prices**: ₹2.99 - ₹16.99

---

## 👨‍💻 Project Structure

```
Food App/
├── backend/
│   ├── app.py                 (Flask server)
│   ├── food_delivery.db       (SQLite database)
│   ├── requirements.txt        (Python dependencies)
│   └── database.sql           (Schema reference)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── api.js             (API client)
│   │   ├── components/
│   │   │   ├── HomePage.js
│   │   │   ├── MenuPage.js
│   │   │   ├── OrdersPage.js
│   │   │   └── Navigation.js
│   │   └── index.js
│   └── package.json
│
├── init_db.py                 (Database initialization)
├── run_backend.bat            (Quick start - backend)
├── run_frontend.bat           (Quick start - frontend)
├── setup_db.bat               (Database setup)
└── README.md                  (This file)
```

---

## 📌 Notes

- **Database**: SQLite file is stored in `backend/food_delivery.db`
- **CORS**: Enabled to allow frontend (port 3000) to communicate with backend (port 5000)
- **Environment**: Development mode with Flask debug enabled
- **Session**: No user authentication (session-based order management)

---

## 💡 Future Enhancements

- [ ] User authentication & login
- [ ] Order history with filtering
- [ ] Restaurant search & filtering
- [ ] Advanced payment gateway integration
- [ ] Real-time order notifications
- [ ] Admin dashboard
- [ ] Delivery tracking map
- [ ] Reviews & ratings system

---

**Created for DBMS Course Project** | 5th Semester
