# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Start XAMPP MySQL (1 minute)

1. **Open XAMPP Control Panel**
2. **Click "Start" next to MySQL** (wait for green indicator)
3. **Open phpMyAdmin**: Click "Admin" next to MySQL
4. **Create Database**: Click "New" → Name: `food_delivery` → Click "Create"
5. **Import SQL**: Select `food_delivery` → Click "Import" → Choose `backend/database.sql` → Click "Go"

**OR using Command Line:**
```bash
mysql -u root < backend/database.sql
```

### Step 2: Start Backend (2 minutes)

```bash
# Terminal 1
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app.py
```

✅ Backend runs at: http://localhost:5000
✅ **Make sure XAMPP MySQL is running!**

### Step 3: Start Frontend (2 minutes)

```bash
# Terminal 2
cd frontend
npm install
npm start
```

✅ Frontend opens at: http://localhost:3000

## 🧪 Testing the App

1. **Home Page**: Should see 5 restaurants with images
2. **Click Restaurant**: Navigate to menu page with 4 items
3. **Add Items**: Click "Add to Cart" button
4. **Checkout**: Click "Proceed to Checkout"
5. **Place Order**: Confirm order in modal
6. **View Orders**: Go to "My Orders" to see created order

## 🐛 Quick Troubleshooting

| Issue                 | Solution                                   |
| --------------------- | ------------------------------------------ |
| Backend won't start   | Ensure XAMPP MySQL is running (green indicator) |
| MySQL connection error | Check XAMPP MySQL is started, verify credentials |
| CORS error in console | Backend must be on port 5000               |
| 'npm' not found       | Install Node.js from nodejs.org            |
| Database error        | Import `database.sql` via phpMyAdmin      |
| React page blank      | Check browser console for errors (F12)     |

## 📋 Checklist

- [ ] XAMPP installed and MySQL service running (green)
- [ ] Database `food_delivery` created and imported via phpMyAdmin
- [ ] Python 3.8+ installed
- [ ] Node.js & npm installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend running on :5000 (Terminal 1)
- [ ] Frontend running on :3000 (Terminal 2)
- [ ] Can view restaurants on home page
- [ ] Can place a test order
- [ ] Can view order in Orders page

## 🎬 Demo Scenarios

### Scenario 1: Browse & Order Pizza

1. Go to home page
2. Click "Pizza Palace"
3. Add "Margherita Pizza" (x2) and "Garlic Bread" (x1)
4. Click "Proceed to Checkout"
5. Confirm order
6. Go to "My Orders" to see it

### Scenario 2: Order from Multiple Restaurants

1. Place order from Pizza Palace
2. Go back to home
3. Place another order from Sushi Supreme
4. Go to "My Orders" to see both orders

### Scenario 3: Manage Orders

1. Place multiple orders
2. Go to "My Orders"
3. Click "Delete" on any order
4. Verify it's removed from the list

---

For detailed documentation, see `README.md`
