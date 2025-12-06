# 🚀 Step-by-Step Guide to Run the Food App

## Prerequisites Checklist

Before starting, make sure you have:
- ✅ **XAMPP** installed (with MySQL)
- ✅ **Python 3.8+** installed
- ✅ **Node.js 14+** and npm installed
- ✅ **Git** (optional, for cloning)

---

## Step 1: Start XAMPP MySQL Server

1. **Open XAMPP Control Panel**
   - Find XAMPP in your Start Menu or Desktop
   - Launch the XAMPP Control Panel

2. **Start MySQL Service**
   - Click the **"Start"** button next to MySQL
   - Wait until the status shows **"Running"** (green)
   - MySQL is now running on `localhost:3306`

3. **Verify MySQL is Running**
   - You should see a green indicator next to MySQL
   - If it shows errors, check the logs in XAMPP

---

## Step 2: Create and Import Database

### Option A: Using phpMyAdmin (Recommended - Easy)

1. **Open phpMyAdmin**
   - In XAMPP Control Panel, click **"Admin"** next to MySQL
   - OR open browser and go to: `http://localhost/phpmyadmin`

2. **Create Database**
   - Click **"New"** in the left sidebar
   - Database name: `food_delivery`
   - Collation: `utf8mb4_general_ci` (or leave default)
   - Click **"Create"**

3. **Import SQL File**
   - Select the `food_delivery` database from left sidebar
   - Click **"Import"** tab at the top
   - Click **"Choose File"** button
   - Navigate to: `C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend\database.sql`
   - Click **"Go"** button at the bottom
   - Wait for success message: "Import has been successfully finished"

4. **Verify Data Imported**
   - Click on `food_delivery` database
   - You should see 4 tables: `restaurants`, `menu_items`, `orders`, `order_items`
   - Click on `restaurants` table → should see 5 restaurants
   - Click on `menu_items` table → should see 20 menu items

### Option B: Using MySQL Command Line

1. **Open Command Prompt** (as Administrator)

2. **Navigate to MySQL bin folder** (if MySQL is not in PATH):
   ```bash
   cd C:\xampp\mysql\bin
   ```

3. **Import Database**:
   ```bash
   mysql -u root -p < "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend\database.sql"
   ```
   - If prompted for password, press Enter (XAMPP default is blank)
   - If MySQL is in PATH, you can run from anywhere:
     ```bash
     mysql -u root < "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend\database.sql"
     ```

---

## Step 3: Setup Backend (Python Flask)

1. **Open Command Prompt** or **PowerShell**

2. **Navigate to Backend Folder**:
   ```bash
   cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend"
   ```

3. **Create Virtual Environment** (Optional but Recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate Virtual Environment**:
   ```bash
   venv\Scripts\activate
   ```
   - You should see `(venv)` prefix in your command prompt

5. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - This installs: Flask, Flask-CORS, mysql-connector-python
   - Wait for installation to complete

6. **Verify Database Connection** (Optional):
   - The app uses default XAMPP MySQL settings:
     - Host: `localhost`
     - User: `root`
     - Password: `` (blank/empty)
     - Database: `food_delivery`
   - If your MySQL has a password, set environment variable:
     ```bash
     set DB_PASSWORD=your_password
     ```

---

## Step 4: Start Backend Server

1. **Make sure you're in backend folder**:
   ```bash
   cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend"
   ```

2. **Activate Virtual Environment** (if you created one):
   ```bash
   venv\Scripts\activate
   ```

3. **Start Flask Server**:
   ```bash
   python app.py
   ```

4. **Verify Backend is Running**:
   - You should see output like:
     ```
     * Running on http://127.0.0.1:5000
     * Debug mode: on
     ```
   - Open browser and go to: `http://localhost:5000/api/health`
   - You should see: `{"status":"Backend is running"}`

5. **Keep this terminal window open** - Backend must stay running!

---

## Step 5: Setup Frontend (React)

1. **Open a NEW Command Prompt** or **PowerShell** window
   - Keep the backend terminal running in the first window

2. **Navigate to Frontend Folder**:
   ```bash
   cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\frontend"
   ```

3. **Install Node Dependencies** (First time only):
   ```bash
   npm install
   ```
   - This may take 2-5 minutes
   - Wait for "added X packages" message

---

## Step 6: Start Frontend Server

1. **Make sure you're in frontend folder**:
   ```bash
   cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\frontend"
   ```

2. **Start React Development Server**:
   ```bash
   npm start
   ```

3. **Browser Should Open Automatically**:
   - If not, manually open: `http://localhost:3000`
   - You should see the Food App homepage with restaurants

4. **Keep this terminal window open** - Frontend must stay running!

---

## Step 7: Verify Everything Works

### ✅ Backend Check:
- Terminal shows: `Running on http://127.0.0.1:5000`
- Browser `http://localhost:5000/api/health` returns JSON

### ✅ Frontend Check:
- Browser shows: `http://localhost:3000`
- Homepage displays 5 restaurants (Pizza Palace, Burger Bistro, etc.)

### ✅ Database Check:
- phpMyAdmin shows `food_delivery` database with 4 tables
- `restaurants` table has 5 rows
- `menu_items` table has 20 rows

### ✅ Test the App:
1. **Click on a restaurant** (e.g., "Pizza Palace")
2. **Add items to cart** (click "Add to Cart")
3. **Proceed to Checkout**
4. **Place Order**
5. **Go to "My Orders"** - Should see your order

---

## 🎯 Quick Reference: Running the App

### Every Time You Want to Run the App:

**Terminal 1 - Backend:**
```bash
cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\backend"
venv\Scripts\activate    # If using virtual environment
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd "C:\Users\Kanna\Documents\5th_sem\DBMS\Food App\frontend"
npm start
```

**XAMPP:**
- Make sure MySQL is running (green indicator)

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip install mysql-connector-python
```

### Problem: "Access denied for user 'root'@'localhost'"
**Solution:**
- Check if MySQL is running in XAMPP
- If you set a MySQL password, set environment variable:
  ```bash
  set DB_PASSWORD=your_password
  ```

### Problem: "Can't connect to MySQL server"
**Solution:**
- Make sure MySQL is started in XAMPP Control Panel
- Check if port 3306 is available

### Problem: "Database 'food_delivery' doesn't exist"
**Solution:**
- Go back to Step 2 and create/import the database

### Problem: Frontend shows "Failed to fetch restaurants"
**Solution:**
- Make sure backend is running on port 5000
- Check browser console (F12) for errors
- Verify `http://localhost:5000/api/health` works

### Problem: Port 5000 or 3000 already in use
**Solution:**
- Find and close the process using the port:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

---

## 📝 Summary

You need **3 things running simultaneously**:

1. ✅ **XAMPP MySQL** (Control Panel - MySQL service)
2. ✅ **Backend Server** (Terminal 1 - `python app.py`)
3. ✅ **Frontend Server** (Terminal 2 - `npm start`)

Then open: **http://localhost:3000** in your browser!

---

## 🎉 Success Indicators

- ✅ MySQL running in XAMPP (green)
- ✅ Backend terminal shows "Running on http://127.0.0.1:5000"
- ✅ Frontend terminal shows "Compiled successfully!"
- ✅ Browser shows restaurant homepage
- ✅ Can place orders and see them in "My Orders"

---

**Need Help?** Check the main `README.md` for more details!

