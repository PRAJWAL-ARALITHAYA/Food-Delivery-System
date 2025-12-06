# Environment Configuration

## Backend Configuration

### Windows

```batch
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Mac/Linux

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## MySQL Setup

### Windows

1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Install MySQL Server
3. During installation, set password for root user
4. Open Command Prompt and verify:
   ```
   mysql --version
   ```

### Mac

```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

## Database Connection

Edit `backend/app.py` if your MySQL setup is different:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Your password here
app.config['MYSQL_DB'] = 'food_delivery'
```

## Frontend Configuration

### Node.js Installation

- Download from: https://nodejs.org/
- Recommended: LTS version
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

### API Endpoint Configuration

If you want to use a different backend URL, edit `frontend/src/api.js`:

```javascript
const API_BASE_URL = "http://localhost:5000/api";
```

## Environment Variables (Optional)

### Backend (.env file)

```
FLASK_ENV=development
FLASK_DEBUG=True
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=food_delivery
```

### Frontend (.env file)

```
REACT_APP_API_URL=http://localhost:5000/api
```

## Ports Used

- **Frontend**: 3000
- **Backend**: 5000
- **MySQL**: 3306

Make sure these ports are not in use by other applications.

## Verification Commands

```bash
# Check Python
python --version

# Check Node.js
node --version
npm --version

# Check MySQL
mysql --version
mysql -u root -p -e "SELECT VERSION();"

# Check if ports are available
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :3000
lsof -i :5000
```

## Troubleshooting Environment Setup

### Python virtual environment not activating

- Windows: Try running as Administrator
- Mac/Linux: Use `bash` instead of `zsh`

### MySQL connection refused

- Ensure MySQL service is running
- Windows: Check Services panel
- Mac: `brew services list`
- Linux: `sudo systemctl status mysql`

### npm install fails

- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again
- Try `npm cache clean --force`

### Port already in use

- Change port in `app.py` (Flask): `app.run(port=5001)`
- Change port in frontend: `PORT=3001 npm start`
- Kill existing process using the port
