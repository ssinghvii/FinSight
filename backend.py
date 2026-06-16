"""
FinSight Backend API
FastAPI server with SQLAlchemy ORM and SQLite database
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import google.generativeai as genai
import os
import json
from sklearn.linear_model import LinearRegression
import numpy as np

# Database setup
DATABASE_URL = "sqlite:///./finsight.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    monthly_allowance = Column(Float, default=0)
    monthly_budget = Column(Float, default=0)
    financial_goal = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    category = Column(String)  # food, entertainment, education, utilities, etc.
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    is_recurring = Column(Boolean, default=False)
    source = Column(String, default="manual")  # manual, upi, sms

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    category = Column(String)
    limit = Column(Float)
    spent = Column(Float, default=0)
    month = Column(String)  # "2024-01" format

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0)
    deadline = Column(DateTime)
    category = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    monthly_allowance: float
    monthly_budget: float
    financial_goal: str = ""

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    monthly_allowance: float
    monthly_budget: float
    financial_goal: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    category: str
    description: str
    date: Optional[datetime] = None
    is_recurring: bool = False
    source: str = "manual"

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    description: str
    date: datetime
    is_recurring: bool
    source: str
    
    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    days_until_zero: int
    predicted_balance: float
    alert: str
    spending_pattern: str
    recommendation: str

class WhatIfResponse(BaseModel):
    purchase_amount: float
    new_balance: float
    days_remaining: int
    impact_message: str
    opportunity_cost: str

class HealthScoreResponse(BaseModel):
    score: int
    category: str
    breakdown: dict
    advice: str

# FastAPI app
app = FastAPI(title="FinSight API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== USER ENDPOINTS ====================

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ==================== TRANSACTION ENDPOINTS ====================

@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/{user_id}", response_model=List[TransactionResponse])
def get_user_transactions(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= cutoff_date
    ).order_by(Transaction.date.desc()).all()
    return transactions

@app.post("/transactions/bulk")
def bulk_add_transactions(user_id: int, transactions: List[TransactionCreate], db: Session = Depends(get_db)):
    """Add mock transaction data"""
    added = []
    for trans in transactions:
        trans.user_id = user_id
        db_transaction = Transaction(**trans.dict())
        db.add(db_transaction)
        added.append(db_transaction)
    db.commit()
    return {"added": len(added)}

# ==================== PREDICTION & ANALYTICS ====================

@app.get("/predictions/{user_id}", response_model=PredictionResponse)
def get_cash_crunch_prediction(user_id: int, db: Session = Depends(get_db)):
    """Predict cash flow and days until running out of money"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get transactions from last 30 days
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= cutoff_date
    ).all()
    
    # Calculate daily spending
    daily_spending = {}
    for trans in transactions:
        date_key = trans.date.date()
        daily_spending[date_key] = daily_spending.get(date_key, 0) + trans.amount
    
    # ML prediction using sklearn
    if len(daily_spending) > 3:
        days = np.array(list(range(len(daily_spending)))).reshape(-1, 1)
        spending = np.array(list(daily_spending.values()))
        
        model = LinearRegression()
        model.fit(days, spending)
        
        predicted_daily_spend = max(0, model.predict([[30]])[0])
        avg_daily_spend = sum(spending) / len(spending) if spending.size > 0 else 0
    else:
        avg_daily_spend = sum(daily_spending.values()) / len(daily_spending) if daily_spending else 0
        predicted_daily_spend = avg_daily_spend
    
    # Calculate current balance (simplified)
    current_balance = user.monthly_allowance - sum([t.amount for t in transactions[-7:]])
    current_balance = max(0, current_balance)
    
    # Days until zero
    if predicted_daily_spend > 0:
        days_until_zero = int(current_balance / predicted_daily_spend)
    else:
        days_until_zero = 90
    
    # Determine alert level
    if days_until_zero < 5:
        alert = "🔴 CRITICAL - You're going broke soon!"
    elif days_until_zero < 15:
        alert = "🟡 WARNING - Cash crunch in 2 weeks"
    else:
        alert = "🟢 SAFE - You're on track"
    
    # Spending pattern
    if avg_daily_spend > user.monthly_allowance / 30:
        spending_pattern = "High spender - Exceeding daily budget"
    elif avg_daily_spend > user.monthly_allowance / 50:
        spending_pattern = "Moderate spender - Within limits"
    else:
        spending_pattern = "Conservative spender - Well managed"
    
    return PredictionResponse(
        days_until_zero=max(0, days_until_zero),
        predicted_balance=max(0, current_balance),
        alert=alert,
        spending_pattern=spending_pattern,
        recommendation=f"Reduce daily spending to ₹{user.monthly_allowance/30:.0f} to be safe"
    )

@app.post("/what-if")
def what_if_simulator(user_id: int, purchase_amount: float, category: str, db: Session = Depends(get_db)):
    """Simulate impact of a purchase before making it"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get current prediction
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= cutoff_date
    ).all()
    
    current_balance = user.monthly_allowance - sum([t.amount for t in transactions[-7:]])
    new_balance = current_balance - purchase_amount
    
    # Calculate impact on cash crunch
    avg_daily_spend = sum([t.amount for t in transactions[-7:]]) / 7 if len(transactions) >= 7 else 0
    if avg_daily_spend > 0:
        days_remaining = int(new_balance / avg_daily_spend) if new_balance > 0 else 0
    else:
        days_remaining = 30
    
    # Opportunity cost framing
    opportunity_cost_mapping = {
        "food": f"= {purchase_amount/50:.0f} college meals",
        "entertainment": f"= {purchase_amount/199:.0f} months of streaming",
        "shopping": f"= {purchase_amount/299:.0f} quality shirts",
        "education": f"= {purchase_amount/500:.0f} online courses",
        "utilities": f"= {purchase_amount/100:.0f} mobile recharges",
    }
    
    opportunity = opportunity_cost_mapping.get(category, f"= important expenses you could afford instead")
    
    if new_balance < 500:
        impact = "⚠️ RISKY - This will leave you critically low"
    elif days_remaining < 10:
        impact = "⚠️ CAUTION - This reduces your safety buffer"
    else:
        impact = "✅ SAFE - You can afford this"
    
    return WhatIfResponse(
        purchase_amount=purchase_amount,
        new_balance=max(0, new_balance),
        days_remaining=max(0, days_remaining),
        impact_message=impact,
        opportunity_cost=opportunity
    )

@app.get("/health-score/{user_id}", response_model=HealthScoreResponse)
def get_financial_health_score(user_id: int, db: Session = Depends(get_db)):
    """Calculate discipline-based financial health score"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get transactions
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= cutoff_date
    ).all()
    
    total_spent = sum([t.amount for t in transactions])
    budget = user.monthly_budget or user.monthly_allowance
    
    # Scoring metrics
    budget_discipline = 0
    consistency = 0
    savings_rate = 0
    
    # Budget discipline (0-40 points)
    if total_spent <= budget:
        budget_discipline = 40
    elif total_spent <= budget * 1.2:
        budget_discipline = 30
    else:
        budget_discipline = max(0, 40 - (total_spent - budget) / budget * 20)
    
    # Consistency (0-30 points)
    if len(transactions) > 7:
        daily_spending = {}
        for trans in transactions:
            date_key = trans.date.date()
            daily_spending[date_key] = daily_spending.get(date_key, 0) + trans.amount
        
        spending_values = list(daily_spending.values())
        if len(spending_values) > 1:
            variance = np.var(spending_values)
            consistency = max(0, 30 - min(variance / 100, 30))
        else:
            consistency = 20
    
    # Savings rate (0-30 points)
    if user.monthly_allowance > 0:
        saved = user.monthly_allowance - total_spent
        save_rate = (saved / user.monthly_allowance) * 100
        if save_rate >= 30:
            savings_rate = 30
        elif save_rate >= 15:
            savings_rate = 20
        else:
            savings_rate = max(0, save_rate / 30 * 10)
    
    score = int(budget_discipline + consistency + savings_rate)
    
    if score >= 85:
        category = "Excellent"
        advice = "Outstanding discipline! Keep maintaining this level."
    elif score >= 70:
        category = "Good"
        advice = "You're doing well. Minor tweaks could improve your score."
    elif score >= 50:
        category = "Fair"
        advice = "You have room for improvement. Set smaller targets."
    else:
        category = "Needs Improvement"
        advice = "Focus on consistent tracking and gradual expense reduction."
    
    return HealthScoreResponse(
        score=min(100, score),
        category=category,
        breakdown={
            "budget_discipline": round(budget_discipline, 1),
            "consistency": round(consistency, 1),
            "savings_rate": round(savings_rate, 1)
        },
        advice=advice
    )

# ==================== AI COACH ENDPOINT ====================

@app.post("/coach")
def financial_coach(user_id: int, question: str, db: Session = Depends(get_db)):
    """AI financial advisor powered by Gemini"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recent transactions for context
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= cutoff_date
    ).all()
    
    total_spent = sum([t.amount for t in transactions])
    categories = {}
    for trans in transactions:
        categories[trans.category] = categories.get(trans.category, 0) + trans.amount
    
    # Build context
    context = f"""
    You are FinSight, an AI financial coach for Indian students.
    
    Student Profile:
    - Name: {user.name}
    - Monthly Allowance: ₹{user.monthly_allowance:.0f}
    - Monthly Budget: ₹{user.monthly_budget:.0f}
    - Goal: {user.financial_goal}
    
    Recent Spending (Last 30 days):
    - Total: ₹{total_spent:.0f}
    - By Category: {json.dumps(categories, indent=2)}
    
    Provide friendly, actionable, and specific financial advice for Indian students.
    Focus on practical tips, savings strategies, and behavioral changes.
    Use Indian currency (₹) in responses.
    Keep responses to 2-3 sentences.
    """
    
    try:
        # Configure Gemini API (requires GOOGLE_API_KEY environment variable)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(context + f"\n\nStudent asks: {question}")
            coach_response = response.text
        else:
            # Fallback response
            coach_response = f"Based on your spending pattern, here's my advice: Focus on reducing {max(categories, key=categories.get)} expenses and try to save ₹{user.monthly_allowance * 0.2:.0f} monthly. You've got this! 💪"
    except Exception as e:
        coach_response = f"Financial advice: Create a spending plan, track daily expenses, and automate savings. You're taking the right step by using FinSight!"
    
    return {
        "user_id": user_id,
        "question": question,
        "response": coach_response
    }

# ==================== OPPORTUNITIES ENDPOINT ====================

@app.get("/opportunities/{user_id}")
def get_opportunities(user_id: int, db: Session = Depends(get_db)):
    """Suggest scholarships, internships, and side income opportunities"""
    opportunities = [
        {
            "type": "Scholarship",
            "title": "Merit-Based Engineering Scholarship",
            "amount": "₹50,000",
            "deadline": "2024-02-15",
            "link": "#",
            "impact": "Could fund your entire semester costs"
        },
        {
            "type": "Internship",
            "title": "Summer FinTech Internship - Goldman Sachs",
            "amount": "₹30,000/month",
            "deadline": "2024-01-31",
            "link": "#",
            "impact": "Build skills AND earn during break"
        },
        {
            "type": "Side Income",
            "title": "Content Writing for EdTech Startups",
            "amount": "₹10,000-30,000/month",
            "deadline": "Ongoing",
            "link": "#",
            "impact": "Flexible income, work from campus"
        },
        {
            "type": "Grant",
            "title": "Women in STEM Scholarship",
            "amount": "₹1,00,000",
            "deadline": "2024-03-01",
            "link": "#",
            "impact": "Could cover your entire year!"
        }
    ]
    
    return {"opportunities": opportunities}

# ==================== HEALTH CHECK ====================

@app.get("/health")
def health_check():
    return {"status": "FinSight API is running! 🎯"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
