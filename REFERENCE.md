# 📚 Quick Reference Card

## 🚀 Commands Cheat Sheet

### Start Everything (3 Terminals)

**Terminal 1 - MySQL**

```bash
mysql -u root -p < backend/database.sql
```

**Terminal 2 - Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

→ http://localhost:5000

**Terminal 3 - Frontend**

```bash
cd frontend
npm install
npm start
```

→ http://localhost:3000

---

## 📡 API Quick Reference

### Get Restaurants

```bash
curl http://localhost:5000/api/restaurants
```

### Get Menu

```bash
curl http://localhost:5000/api/restaurants/1/menu
```

### Create Order

```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"restaurant_id":1,"items":[{"menu_item_id":1,"quantity":1}],"total_price":8.99}'
```

### Get Orders

```bash
curl http://localhost:5000/api/orders
```

### Delete Order

```bash
curl -X DELETE http://localhost:5000/api/orders/1
```

---

## 📁 Important Files

| File                    | Purpose              |
| ----------------------- | -------------------- |
| `backend/app.py`        | Flask API            |
| `backend/database.sql`  | Database schema      |
| `frontend/package.json` | NPM dependencies     |
| `frontend/src/App.js`   | Main React component |
| `frontend/src/api.js`   | API client           |

---

## 🔑 Key Ports

- Frontend: **3000**
- Backend: **5000**
- MySQL: **3306**

---

## 🍴 Sample Restaurants

1. Pizza Palace (Italian) - ID: 1
2. Burger Bistro (American) - ID: 2
3. Sushi Supreme (Japanese) - ID: 3
4. Taco Fiesta (Mexican) - ID: 4
5. Curry House (Indian) - ID: 5

---

## 🐛 Common Issues

| Problem                | Fix                         |
| ---------------------- | --------------------------- |
| MySQL connection error | Check MySQL is running      |
| CORS error             | Backend must be on :5000    |
| npm not found          | Install Node.js             |
| Port in use            | Change port or kill process |
| Empty restaurants list | Run database.sql            |

---

## 📊 Database Tables

```sql
restaurants (5 records)
menu_items (20 records)
orders (empty)
order_items (empty)
```

---

## 🎯 App Screens

1. **Homepage** - See restaurants
2. **Menu** - Browse items
3. **Cart** - Add/remove items
4. **Checkout** - Review order
5. **Orders** - See history

---

## 🔗 Links

- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- API Docs: /api/health
- MySQL: localhost:3306

---

## 📖 Docs Map

- **Quick Start**: QUICKSTART.md
- **Full Guide**: README.md
- **Setup Help**: SETUP.md
- **API Reference**: API_TESTING.md
- **Project Info**: PROJECT_SUMMARY.md

---

## ✅ Before Going Live

- [ ] Database backup created
- [ ] Environment variables set
- [ ] All endpoints tested
- [ ] Frontend responsive checked
- [ ] Error handling verified
- [ ] Documentation reviewed

---

**Need help?** Check the relevant documentation file above!
