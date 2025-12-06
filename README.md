# 🍕 Online Food Delivery System

A complete full-stack web application for online food delivery with React frontend, Flask backend, and MySQL database.

## 📋 Features

- **View Restaurants**: Browse a list of available restaurants with ratings and delivery times
- **Browse Menus**: Click on a restaurant to view their menu items with descriptions and prices
- **Shopping Cart**: Add/remove items to/from cart with quantity management
- **Place Orders**: Complete order checkout with order summary
- **View Orders**: Track all placed orders in a table format
- **Order Management**: Delete orders (demo functionality)

## 🏗️ Architecture

### Frontend (React)

- **Framework**: React 18.2.0
- **Routing**: React Router v6
- **UI**: Bootstrap 5 & React-Bootstrap
- **HTTP Client**: Axios
- **Components**:
  - `HomePage`: Displays list of restaurants
  - `MenuPage`: Shows menu items for a selected restaurant
  - `OrdersPage`: Displays all placed orders
  - `Navigation`: Top navigation bar

### Backend (Flask)

- **Framework**: Flask 2.3.3
- **Database**: MySQL (tested with XAMPP) via `mysql-connector-python`
- **CORS**: Enabled for cross-origin requests
- **API Endpoints**:
  - Restaurants: GET, GET (by ID)
  - Menu Items: GET (by restaurant), GET (by ID)
  - Orders: GET, GET (by ID), POST, PUT (status), DELETE

### Database (MySQL)

- **Tables**:
  - `restaurants`: Store restaurant information
  - `menu_items`: Store menu items for each restaurant
  - `orders`: Store order records
  - `order_items`: Store individual items in each order

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL Server
- Git (optional)

### Backend Setup

1. **Navigate to backend folder**:

   ```bash
   cd backend
   ```

2. **Create a Python virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database (XAMPP-friendly)**:

   - Start `MySQL` from the XAMPP Control Panel.
   - Import the schema/data from `backend/database.sql`:
     - **phpMyAdmin**: Open `http://localhost/phpmyadmin`, create a database named `food_delivery`, choose the DB, then use **Import** and select `backend/database.sql`.
     - **CLI** (if MySQL is on PATH): `mysql -u root -p < backend/database.sql`
   - Default credentials assumed by the app are `host=localhost`, `user=root`, `password=''` (blank), `db=food_delivery`.
   - To override these (e.g., if you set a password), set environment variables: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

5. **Start Flask Server**:
   ```bash
   python app.py
   ```
   - Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend folder**:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start React Development Server**:
   ```bash
   npm start
   ```
   - Application will open at `http://localhost:3000`

## 📡 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Restaurants Endpoints

#### Get All Restaurants

```
GET /restaurants
Response: [{id, name, cuisine, rating, delivery_time, image_url, created_at}, ...]
```

#### Get Restaurant by ID

```
GET /restaurants/:id
Response: [
  {
    "id": 1,
    "name": "Pizza Palace",
    "cuisine": "Italian",
    "rating": 4.5,
    "delivery_time": 30,
    "image_url": "...",
    "created_at": "..."
  }
]

```

### Menu Endpoints

#### Get Menu Items by Restaurant

```
GET /restaurants/:restaurant_id/menu
Response: [
  {
    "id": 1,
    "restaurant_id": 1,
    "name": "Margherita Pizza",
    "description": "Classic cheese pizza",
    "price": 9.99,
    "category": "Pizza",
    "image_url": "...",
    "created_at": "..."
  }
]
```

#### Get Menu Item by ID

```
GET /menu/:id
Response: {
  "id": 1,
  "restaurant_id": 1,
  "name": "Margherita Pizza",
  "description": "Classic cheese pizza",
  "price": 9.99,
  "category": "Pizza",
  "image_url": "...",
  "created_at": "..."
}
```

### Orders Endpoints

#### Get All Orders

```
GET /orders
Response: [
  {
    "id": 1,
    "restaurant_id": 1,
    "total_price": 25.97,
    "status": "Pending",
    "restaurant_name": "Pizza Palace",
    "items": [ ... ],
    "created_at": "...",
    "updated_at": "..."
  }
]

```

#### Get Order by ID

```
GET /orders/:id
Response:{
  "id": 1,
  "restaurant_id": 1,
  "total_price": 25.97,
  "status": "Pending",
  "restaurant_name": "Pizza Palace",
  "items": [ ... ],
  "created_at": "...",
  "updated_at": "..."
}

```

#### Create New Order

```
POST /orders
Request Body: {
  "restaurant_id": 1,
  "items": [
    {"menu_item_id": 1, "quantity": 2},
    {"menu_item_id": 3, "quantity": 1}
  ],
  "total_price": 25.97
}
Response: {
  "id": 1,
  "restaurant_id": 1,
  "total_price": 25.97,
  "status": "Pending",
  "message": "Order created successfully"
}

```

#### Update Order Status

```
PUT /orders/:id
Request Body:{
  "status": "Confirmed"
}

Response: {
  "message": "Order status updated"
}

```

#### Delete Order

```
DELETE /orders/:id
Response: {
  "message": "Order deleted"
}

```

#### Health Check

```
GET /health
Response: {status: "Backend is running"}
```

## 📂 Project Structure

```
Food App/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.sql        # Database schema and sample data
│   └── requirements.txt     # Python dependencies
│
└── frontend/
    ├── public/
    │   └── index.html      # HTML template
    ├── src/
    │   ├── components/
    │   │   ├── HomePage.js       # Restaurant listing component
    │   │   ├── HomePage.css
    │   │   ├── MenuPage.js       # Menu items component
    │   │   ├── MenuPage.css
    │   │   ├── OrdersPage.js     # Orders listing component
    │   │   ├── OrdersPage.css
    │   │   ├── Navigation.js     # Navigation bar component
    │   │   └── Navigation.css
    │   ├── api.js           # Axios API client
    │   ├── App.js           # Main App component
    │   ├── App.css
    │   ├── index.js         # React entry point
    │   └── index.css
    ├── package.json         # Node.js dependencies
    └── .gitignore
```

## 🎯 Application Flow

1. **Homepage** → User sees list of 5 restaurants with ratings, delivery times, and images
2. **Restaurant Details** → Click "View Menu" to see all menu items
3. **Add to Cart** → Add items to cart with quantity controls
4. **Checkout** → Review order in modal and confirm
5. **Order Placed** → API creates order in database and redirects to orders page
6. **View Orders** → See all placed orders in a table with status badges
7. **Manage Orders** → Delete orders from the system

## 💾 Sample Data

The system comes with 5 pre-loaded restaurants:

1. **Pizza Palace** - Italian cuisine
2. **Burger Bistro** - American cuisine
3. **Sushi Supreme** - Japanese cuisine
4. **Taco Fiesta** - Mexican cuisine
5. **Curry House** - Indian cuisine

Each restaurant has 4 menu items included.

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Bootstrap Styling**: Professional and clean UI using Bootstrap 5
- **Hover Effects**: Interactive card animations for better UX
- **Color-coded Badges**: Status indicators and rating badges
- **Loading States**: Spinner animations while data is loading
- **Error Handling**: User-friendly error messages
- **Toast Notifications**: Alerts for successful/failed operations
- **Sticky Cart**: Cart total remains visible at bottom when scrolling

## 🔒 Notes

- This is a **demo application** with fake orders
- No user authentication is implemented
- Database runs locally on your machine
- CORS is enabled for development purposes
- All data is stored in local MySQL database

## 🐛 Troubleshooting

### Backend Won't Start

- Ensure MySQL is running
- Check database credentials in `app.py`
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend Won't Load

- Ensure backend is running on port 5000
- Check Node.js and npm are installed
- Run `npm install` again if modules are missing
- Clear browser cache or use incognito mode

### Database Connection Error

- Verify MySQL is running
- Check username/password in `app.py`
- Ensure `food_delivery` database exists
- Run `database.sql` to create tables and sample data

### CORS Errors

- Backend CORS is already configured
- Ensure you're accessing from `localhost:3000`
- Check network tab in browser DevTools for actual error

## 📝 Future Enhancements

- User authentication and registration
- Real payment processing
- Order tracking in real-time
- Review and rating system
- Admin dashboard
- Push notifications
- Delivery partner tracking
- Multiple language support
- Dark mode

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a demonstration of full-stack web development with React, Flask, and MySQL.

---

**Happy Ordering! 🚀**
