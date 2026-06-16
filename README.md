# FinSight - AI Financial Coach for Indian Students

A full-stack financial management application built for the InnovaHack FinTech Domain challenge. Stop tracking the past, start predicting your future.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Features

### Core Features
- **🔮 Cash Crunch Predictor** - ML-based prediction of when you'll run out of money
- **❓ What-If Simulator** - Test purchase impact before spending
- **💪 Financial Health Score** - Discipline-based scoring (not wealth-based)
- **🤖 AI Financial Coach** - Personalized advice powered by Google Gemini
- **🎓 Opportunity Recommender** - Scholarships, internships, side income suggestions
- **📊 Spending Analytics** - Visual breakdown of where your money goes

### Tech Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database (easily swappable with MySQL/PostgreSQL)
- **Scikit-learn** - ML for spending predictions
- **Google Generative AI** - Gemini API for financial coaching

**Frontend:**
- **React 18** - Modern UI framework
- **CSS3** - Custom styling (no third-party UI frameworks)
- **Responsive Design** - Mobile-first approach

**Optional Production Stack:**
- **Spring Boot** + **MySQL** (as mentioned in original spec)
- **Docker** - Containerization
- **Nginx** - Reverse proxy

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- Git
- Google API Key (for Gemini API - optional for basic features)

### Installation

#### 1. Clone and Setup Project
```bash
cd finsight-app
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key (optional - app works without it)
export GOOGLE_API_KEY="your-google-api-key-here"

# Run backend
python backend.py
```

Backend will start at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### 3. Frontend Setup (in new terminal)

```bash
# Install dependencies
npm install

# Create React app structure (one-time setup)
npx create-react-app . --template cra-template
```

**Then replace the generated files:**
- Replace `src/App.jsx` with our `App.jsx`
- Replace `src/App.css` with our `App.css`
- Keep `src/index.js` unchanged

**Start frontend:**
```bash
npm start
```

Frontend will open at `http://localhost:3000`

#### 4. Load Demo Data

```bash
python seed_data.py
```

This creates a demo user with 30 days of realistic transaction data.

---

## 📊 Architecture

```
FinSight
├── Backend (FastAPI)
│   ├── Users Management
│   ├── Transaction Processing
│   ├── ML Prediction Engine
│   ├── Gemini AI Integration
│   └── Database (SQLite → MySQL)
│
├── Frontend (React)
│   ├── Dashboard
│   ├── Feature Screens
│   ├── Forms & Input
│   └── Responsive UI
│
└── Data Layer
    ├── User Profiles
    ├── Transactions
    ├── Budgets & Goals
    └── ML Models
```

### API Endpoints

```
POST   /users                          Create user
GET    /users/{user_id}                Get user profile
GET    /users                          List all users

POST   /transactions                   Add transaction
GET    /transactions/{user_id}         Get user transactions
POST   /transactions/bulk              Bulk import transactions

GET    /predictions/{user_id}          Cash crunch prediction
POST   /what-if                        Simulate purchase impact
GET    /health-score/{user_id}         Financial health score

POST   /coach                          AI financial advice
GET    /opportunities/{user_id}        Opportunity recommendations

GET    /health                         API health check
```

---

## 🎮 How to Use

### 1. Create Account
- Enter name, email, monthly allowance, budget, and financial goal
- Account is instantly created

### 2. View Dashboard
- See current balance prediction
- Check spending pattern
- View alert status (🟢 Safe / 🟡 Warning / 🔴 Critical)

### 3. Use Features

**Cash Crunch Predictor:**
- Analyzes last 30 days of spending
- Predicts days until cash runs out
- Uses linear regression ML model

**What-If Simulator:**
- Enter purchase amount and category
- See impact on cash flow
- View opportunity cost (e.g., "= 5 meals" or "= 1 course")

**Financial Health Score:**
- Score out of 100 (discipline-based, not wealth-based)
- Breakdown: Budget Discipline + Consistency + Savings Rate
- Get personalized advice

**AI Coach:**
- Ask any financial question
- Get advice based on your spending patterns
- Powered by Google Gemini API

**Opportunities:**
- Scholarships, internships, side income
- Curated for students
- AI-recommended based on goals

---

## 🏗️ Project Structure

```
finsight-app/
├── backend.py                 # FastAPI server with all endpoints
├── App.jsx                    # React main component
├── App.css                    # All styling
├── seed_data.py              # Demo data generator
├── requirements.txt          # Python dependencies
├── package.json              # Node dependencies
└── README.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Google Gemini API
export GOOGLE_API_KEY="your-key-here"

# Optional: Database URL (default: SQLite)
export DATABASE_URL="sqlite:///./finsight.db"

# Optional: Frontend API URL
export REACT_APP_API_URL="http://localhost:8000"
```

### Customization

**Change Theme Colors** (in App.css):
```css
--primary-color: #FF6B6B;
--secondary-color: #4ECDC4;
--accent-color: #FFD93D;
```

**Modify Alert Thresholds** (in backend.py):
- Change `days_until_zero < 5` for critical alert
- Adjust ML model parameters

**Add Categories** (in App.jsx):
```javascript
const categories = ['food', 'entertainment', 'education', 'shopping', 'utilities', 'other'];
```

---

## 🧪 Testing

### Test All Features
```bash
# Terminal 1: Start backend
python backend.py

# Terminal 2: Start frontend
npm start

# Terminal 3: Load demo data
python seed_data.py
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000/health

# Get predictions
curl http://localhost:8000/predictions/1

# What-if simulator
curl "http://localhost:8000/what-if?user_id=1&purchase_amount=2500&category=shopping"

# Get health score
curl http://localhost:8000/health-score/1
```

### Testing with Different Scenarios
1. **Low balance scenario** - Create user with small allowance
2. **High spender scenario** - Add many transactions
3. **Consistent spender** - Add regular daily transactions
4. **Zero transactions** - Test with new user

---

## 📈 Performance & Optimization

### Current Optimizations
- **Frontend:** React memoization for expensive components
- **Backend:** Query optimization with SQLAlchemy
- **ML:** Linear regression (fast, suitable for 30-day prediction)
- **Caching:** Consider Redis for frequently accessed data

### Future Optimizations
- Implement pagination for transactions
- Add request rate limiting
- Cache API responses on frontend
- Use more sophisticated ML models (ARIMA, Prophet)
- Implement background jobs for data processing

---

## 🔐 Security & Privacy

### Current Implementation
- User data stored locally in database
- No authentication (demo purposes)
- API open to local network only

### Production Recommendations
- Add JWT authentication
- Implement HTTPS
- Add rate limiting
- Encrypt sensitive data
- Add transaction logging
- Regular security audits

### User Data Privacy
- Transactions not shared with AI (only aggregated stats)
- No external data collection
- All data stays on your server

---

## 🚢 Deployment

### Docker Deployment
```bash
# Backend
docker build -t finsight-backend .
docker run -p 8000:8000 finsight-backend

# Frontend
docker build -t finsight-frontend .
docker run -p 3000:3000 finsight-frontend
```

### Heroku Deployment
```bash
# Backend to Heroku
git push heroku main
```

### AWS/Azure Deployment
- Containerize both services
- Deploy backend to App Service/EC2
- Deploy frontend to CloudFront/CDN
- Use RDS for MySQL database

---

## 🔄 Migration to Spring Boot + MySQL

If you want to use the original tech stack:

### Steps
1. **Convert FastAPI to Spring Boot**
   - Convert Python models to Java entities
   - Convert API endpoints to Spring controllers
   - Use Spring Data JPA for database operations

2. **Database Migration**
   - Replace SQLite with MySQL
   - Create migration scripts
   - Update connection strings

3. **ML Integration**
   - Use Python service or integrate ML4j
   - Create REST endpoint for predictions
   - Call from Spring Boot

4. **Frontend** remains the same (React)

### Resources
- Spring Boot Documentation: https://spring.io/projects/spring-boot
- Spring Data JPA: https://spring.io/projects/spring-data-jpa
- MySQL Driver: mysql-connector-java

---

## 🐛 Troubleshooting

### "API connection refused"
- Ensure backend is running: `python backend.py`
- Check port 8000 is not in use

### "Module not found" errors
- Install dependencies: `pip install -r requirements.txt`
- For frontend: `npm install`

### "Database locked" error
- Close all other instances of the app
- Delete `finsight.db` and restart

### AI Coach not responding
- Ensure GOOGLE_API_KEY is set
- Check Gemini API quota and credits
- App has fallback response if API fails

### Frontend build issues
- Clear npm cache: `npm cache clean --force`
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

---

## 📚 Learning Resources

### Code Walkthroughs
1. **Backend Entry Point:** `backend.py` lines 1-100
2. **Prediction Logic:** `backend.py` lines 200-250
3. **Frontend Flow:** `App.jsx` lines 1-50
4. **Styling System:** `App.css` - CSS variables approach

### Key Concepts Implemented
- **RESTful API Design**
- **SQLAlchemy ORM**
- **React Hooks** (useState, useEffect)
- **Machine Learning** (Linear Regression)
- **AI Integration** (Gemini API)
- **Responsive Design**

---

## 🤝 Contributing

Want to improve FinSight? 

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Make changes and commit: `git commit -m 'Add NewFeature'`
4. Push to branch: `git push origin feature/NewFeature`
5. Open Pull Request

### Ideas for Contributions
- [ ] Add bill reminders & recurring expense automation
- [ ] Implement peer comparison (anonymous benchmarking)
- [ ] Add investment recommendations
- [ ] Create mobile app with React Native
- [ ] Add Razorpay integration for upi tracking
- [ ] SMS/Email notifications for low balance
- [ ] Export reports as PDF

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Team

**Ctrl Cmd Conquer**
- **Siya Singhvi** - Team Lead
- **Ilisha Shah** - Member
- **Prisha Parikh** - Member

**Event:** InnovaHack Chapter 1 - FinTech Domain

---

## 📞 Support

For issues, questions, or feedback:
1. Check the Troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check React console for frontend errors (F12)

---

## 🎓 Building Your Own

If you want to build similar features:

1. **Prediction Engine** - Use scikit-learn, analyze 30-day patterns
2. **Scenario Simulator** - Calculate impact, use opportunity costs
3. **Health Scoring** - Multiple metrics, avoid wealth bias
4. **AI Integration** - Use Gemini, Claude, or GPT API with context
5. **Opportunities** - Curate real scholarships/internships for your region

---

## 🌟 Future Roadmap

- [ ] Mobile app (React Native/Flutter)
- [ ] Real UPI integration via RazorPay
- [ ] SMS transaction parsing
- [ ] Goal tracking with milestones
- [ ] Social features (peer challenges)
- [ ] Investment recommendations
- [ ] Credit score improvement tips
- [ ] Scholarship automation
- [ ] Expense categorization AI
- [ ] Multi-language support (Hindi, regional languages)

---

**Stop tracking the past. Start predicting your future.** 🚀

Built with ❤️ for Indian students
