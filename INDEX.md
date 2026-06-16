# FinSight Project - File Index

## 📂 Project Structure

```
finsight-app/
├── 📄 Core Application Files
│   ├── backend.py                 # FastAPI backend server (650+ lines)
│   ├── App.jsx                    # React main component (500+ lines)
│   ├── App.css                    # Complete styling (700+ lines)
│   └── seed_data.py              # Demo data generator
│
├── 📦 Configuration Files
│   ├── requirements.txt           # Python dependencies
│   ├── package.json              # Node.js dependencies
│   ├── .env                      # Environment variables
│   ├── .gitignore                # Git ignore rules
│   └── .env.example              # Example environment file
│
├── 🐳 Docker Files
│   ├── docker-compose.yml        # Docker Compose configuration
│   ├── Dockerfile.backend        # Python backend Docker image
│   ├── Dockerfile.frontend       # React frontend Docker image
│   ├── nginx.conf                # Nginx reverse proxy config
│   └── .dockerignore             # Docker ignore rules
│
├── 🚀 Setup & Deployment
│   ├── setup.sh                  # Linux/Mac setup script
│   ├── setup.bat                 # Windows setup script
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── TESTING.md                # Testing guide
│   └── ARCHITECTURE.md           # Architecture documentation
│
└── 📚 Documentation
    ├── README.md                 # Main documentation
    ├── INDEX.md                  # This file
    ├── API.md                    # API documentation
    ├── FEATURES.md               # Feature descriptions
    ├── TROUBLESHOOTING.md        # Troubleshooting guide
    └── CONTRIBUTING.md           # Contributing guide
```

---

## 📄 File Descriptions

### Core Application Files

#### `backend.py` (650+ lines)
**Purpose:** FastAPI backend server with all business logic
**Key Components:**
- Database models (User, Transaction, Budget, Goal)
- API endpoints for all features
- ML prediction engine using scikit-learn
- Gemini API integration for AI coach
- Health score calculation algorithm

**Main Endpoints:**
```
POST   /users                      - Create user account
GET    /users/{user_id}            - Get user profile
POST   /transactions               - Add transaction
GET    /predictions/{user_id}      - Get cash crunch prediction
POST   /what-if                    - Simulate purchase
GET    /health-score/{user_id}     - Get financial health score
POST   /coach                      - Get AI advice
GET    /opportunities/{user_id}    - Get opportunities
```

**Technologies:**
- FastAPI - Web framework
- SQLAlchemy - ORM
- Scikit-learn - ML predictions
- Google Generative AI - Gemini API

#### `App.jsx` (500+ lines)
**Purpose:** Main React component with all UI screens
**Key Components:**
- LoginScreen - User registration
- Dashboard - Main dashboard view
- PredictionsScreen - Cash crunch predictor
- WhatIfScreen - Purchase simulator
- HealthScoreScreen - Financial health score
- CoachScreen - AI financial advisor
- OpportunitiesScreen - Opportunities list
- TransactionsScreen - Transaction history

**Features:**
- State management with React hooks
- API communication with fetch
- Responsive component layout
- Form handling and validation

#### `App.css` (700+ lines)
**Purpose:** Complete styling for entire application
**Key Sections:**
- CSS Variables (colors, shadows, border-radius)
- Layout & Grid systems
- Component styling
- Animations & transitions
- Responsive design (mobile-first)
- Dark mode support ready

**Color Scheme:**
- Primary: #FF6B6B (Red)
- Secondary: #4ECDC4 (Teal)
- Accent: #FFD93D (Yellow)
- Dark: #2C3E50

#### `seed_data.py` (200+ lines)
**Purpose:** Populate database with realistic demo data
**Features:**
- Creates demo user (Priya Sharma)
- Generates 30 days of transactions
- Tests all API endpoints
- Displays verification results

**Usage:**
```bash
python seed_data.py
```

---

### Configuration Files

#### `requirements.txt`
Python package dependencies:
- fastapi==0.104.1
- sqlalchemy==2.0.23
- scikit-learn==1.3.2
- google-generativeai==0.3.0
- uvicorn==0.24.0
- numpy==1.26.2

#### `package.json`
Node.js dependencies:
- react@18
- react-dom@18
- react-scripts@5.0.1

#### `.env` (create during setup)
```
REACT_APP_API_URL=http://localhost:8000
DATABASE_URL=sqlite:///./finsight.db
GOOGLE_API_KEY=your-key-here (optional)
```

---

### Docker Files

#### `docker-compose.yml`
Complete Docker Compose configuration:
- Backend service (FastAPI)
- Frontend service (React)
- Nginx reverse proxy
- Health checks
- Volume management
- Network configuration

**Start with:**
```bash
docker-compose up
```

#### `Dockerfile.backend`
Multi-stage Docker build for Python:
- Python 3.11 slim base
- Install dependencies
- Copy application
- Expose port 8000
- Run with Uvicorn

#### `Dockerfile.frontend`
Multi-stage Docker build for React:
- Node 18 builder stage
- Install dependencies
- Build optimized bundle
- Serve with 'serve' package
- Expose port 3000

#### `nginx.conf`
Nginx configuration:
- Reverse proxy setup
- Rate limiting
- CORS headers
- Gzip compression
- SSL ready (commented)
- Static asset caching

---

### Setup & Deployment Scripts

#### `setup.sh` (for Linux/Mac)
Automated setup script:
- Checks Python/Node installation
- Creates virtual environment
- Installs dependencies
- Generates .env file
- Provides startup instructions

**Run with:**
```bash
chmod +x setup.sh
./setup.sh
```

#### `setup.bat` (for Windows)
Windows batch equivalent of setup.sh:
- Same functionality for Windows
- Uses `venv\Scripts\activate.bat`
- Creates .env file
- Provides startup instructions

**Run with:**
```bash
setup.bat
```

---

### Documentation Files

#### `README.md`
Complete project documentation:
- Feature overview
- Quick start guide
- Architecture diagram
- API endpoints
- Configuration options
- Troubleshooting guide
- Deployment instructions
- Contributing guidelines

#### `ARCHITECTURE.md` (if created)
Technical architecture:
- System design
- Data flow
- Database schema
- API design patterns
- ML model explanation
- Performance considerations

#### `API.md` (if created)
API documentation:
- Endpoint details
- Request/response examples
- Error codes
- Authentication
- Rate limiting
- Webhook setup

#### `DEPLOYMENT.md` (if created)
Deployment guide:
- Local development
- Docker deployment
- Cloud platforms (AWS, Heroku, Azure)
- Database migration
- Scaling considerations
- Monitoring

#### `TESTING.md` (if created)
Testing guide:
- Unit tests
- Integration tests
- API testing
- Frontend testing
- Performance testing
- Security testing

---

## 🔄 File Dependencies

```
backend.py
  ├── Requires: requirements.txt
  ├── Creates: finsight.db (SQLite)
  └── Needs: GOOGLE_API_KEY (optional)

App.jsx
  ├── Requires: App.css
  ├── Communicates with: backend.py
  └── Needs: package.json (node_modules)

seed_data.py
  ├── Requires: requirements.txt
  ├── Depends on: backend.py running
  └── Populates: finsight.db

docker-compose.yml
  ├── References: Dockerfile.backend
  ├── References: Dockerfile.frontend
  ├── References: nginx.conf
  └── Networks: all services

nginx.conf
  ├── Proxies to: backend (8000)
  ├── Proxies to: frontend (3000)
  └── Listens on: 80, 443

setup.sh / setup.bat
  ├── Creates: venv
  ├── Creates: node_modules
  └── Creates: .env
```

---

## 🚀 Getting Started

### Minimal Setup (Local Development)

1. **Install Python and Node:**
   ```bash
   # Check versions
   python --version  # Should be 3.9+
   node --version    # Should be 16+
   ```

2. **Clone and enter project:**
   ```bash
   cd finsight-app
   ```

3. **Run setup script:**
   ```bash
   # Linux/Mac
   chmod +x setup.sh && ./setup.sh
   
   # Windows
   setup.bat
   ```

4. **Start services** (in separate terminals):
   ```bash
   # Terminal 1 - Backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python backend.py
   
   # Terminal 2 - Frontend
   npm start
   
   # Terminal 3 - Load demo data (after both above are running)
   python seed_data.py
   ```

5. **Open application:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Docker Setup (Complete Stack)

```bash
docker-compose up
```

This starts:
- Backend on http://localhost:8000
- Frontend on http://localhost:3000
- Nginx on http://localhost:80

---

## 📊 Code Statistics

| Component | Lines | Description |
|-----------|-------|-------------|
| backend.py | 650+ | FastAPI backend |
| App.jsx | 500+ | React components |
| App.css | 700+ | Styling |
| seed_data.py | 200+ | Demo data |
| requirements.txt | 8 | Python deps |
| package.json | 25 | Node deps |
| docker-compose.yml | 50 | Docker setup |
| nginx.conf | 80 | Proxy config |

**Total: ~2,200+ lines of code**

---

## 🔐 Security & Privacy

### Files Handling Sensitive Data
- `backend.py` - User profile and transaction data
- `finsight.db` - SQLite database (local only)
- `.env` - API keys and credentials

### Security Checklist
- [ ] Never commit `.env` with real API keys
- [ ] Use `.gitignore` to exclude sensitive files
- [ ] Review Docker security best practices
- [ ] Enable HTTPS in production (nginx.conf)
- [ ] Add authentication for production
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Sanitize user inputs

---

## 📦 Deployment Targets

### Local Development
- Frontend: `npm start`
- Backend: `python backend.py`

### Docker
- `docker-compose up`
- All services containerized
- Ready for cloud deployment

### Cloud Platforms
- **Heroku:** Deploy both services
- **AWS:** ECS + RDS + CloudFront
- **Azure:** App Service + Azure SQL
- **GCP:** Cloud Run + Cloud SQL

---

## 🛠️ Common Tasks

### Add New API Endpoint
1. Edit `backend.py`
2. Add route decorator: `@app.get("/endpoint")`
3. Test with curl or Postman
4. Update `API.md` documentation

### Add New Frontend Screen
1. Create component in `App.jsx`
2. Add CSS in `App.css`
3. Add navigation in Dashboard
4. Test responsive design

### Change Database Structure
1. Modify models in `backend.py`
2. Delete `finsight.db`
3. Restart backend (recreates DB)
4. Run `seed_data.py` again

### Deploy to Production
1. Set `REACT_APP_API_URL` to production URL
2. Build frontend: `npm run build`
3. Configure Docker with production settings
4. Set up database (MySQL instead of SQLite)
5. Configure nginx with SSL
6. Deploy to cloud platform

---

## 📞 Support & Troubleshooting

### Check System Setup
```bash
# Verify Python
python --version
pip list | grep -E "fastapi|sqlalchemy|scikit"

# Verify Node
node --version
npm list | head -20

# Verify ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
```

### Common Issues
See `TROUBLESHOOTING.md` for detailed solutions.

---

## 📚 Learning Resources

### Understanding the Stack
1. **FastAPI:** https://fastapi.tiangolo.com/
2. **React:** https://react.dev/
3. **SQLAlchemy:** https://docs.sqlalchemy.org/
4. **Scikit-learn:** https://scikit-learn.org/
5. **Docker:** https://docs.docker.com/

### Code Quality
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Add type hints in Python
- Use PropTypes in React

### Testing
- Add pytest for backend
- Add Jest/React Testing Library for frontend
- Test all API endpoints
- Test UI interactions

---

## 🤝 Contributing

To contribute:
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

See `CONTRIBUTING.md` for detailed guidelines.

---

## 📄 License

MIT License - See LICENSE file for details

---

**Last Updated:** January 2024
**Project:** FinSight v1.0.0
**Team:** Ctrl Cmd Conquer
