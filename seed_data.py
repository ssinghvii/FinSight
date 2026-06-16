"""
Seed script for populating FinSight database with demo data
Run this after starting the backend to test all features
"""

import requests
import json
from datetime import datetime, timedelta
import random

API_URL = "http://localhost:8000"

# Demo user data
DEMO_USER = {
    "name": "Priya Sharma",
    "email": "priya.sharma@college.com",
    "monthly_allowance": 15000,
    "monthly_budget": 12000,
    "financial_goal": "Save ₹50,000 for gaming laptop"
}

# Sample transactions
SAMPLE_TRANSACTIONS = [
    {"amount": 350, "category": "food", "description": "Swiggy delivery - biryani", "is_recurring": False},
    {"amount": 199, "category": "entertainment", "description": "Netflix subscription", "is_recurring": True},
    {"amount": 500, "category": "education", "description": "Online course - Python", "is_recurring": False},
    {"amount": 2500, "category": "shopping", "description": "New jeans from Myntra", "is_recurring": False},
    {"amount": 400, "category": "food", "description": "Cafe coffee with friends", "is_recurring": False},
    {"amount": 99, "category": "entertainment", "description": "Prime Video", "is_recurring": True},
    {"amount": 299, "category": "utilities", "description": "Mobile recharge - Jio", "is_recurring": True},
    {"amount": 1500, "category": "food", "description": "Hostel mess subscription", "is_recurring": True},
    {"amount": 450, "category": "shopping", "description": "Books from Amazon", "is_recurring": False},
    {"amount": 200, "category": "entertainment", "description": "Movie tickets - PVR", "is_recurring": False},
    {"amount": 300, "category": "food", "description": "Pizza party with roommates", "is_recurring": False},
    {"amount": 150, "category": "utilities", "description": "WiFi at cafe", "is_recurring": False},
    {"amount": 2000, "category": "shopping", "description": "Winter clothes shopping", "is_recurring": False},
    {"amount": 400, "category": "education", "description": "Udemy courses", "is_recurring": False},
    {"amount": 600, "category": "food", "description": "Restaurant dinner", "is_recurring": False},
]

def create_user():
    """Create demo user"""
    response = requests.post(f"{API_URL}/users", json=DEMO_USER)
    if response.status_code == 200:
        user = response.json()
        print(f"✅ User created: {user['name']} (ID: {user['id']})")
        return user
    else:
        print(f"❌ Error creating user: {response.text}")
        return None

def add_transactions(user_id):
    """Add sample transactions spread over last 30 days"""
    transactions_to_add = []
    
    for i in range(30):
        # Add 1-2 random transactions per day
        num_transactions = random.choice([1, 1, 1, 2])
        for _ in range(num_transactions):
            trans = random.choice(SAMPLE_TRANSACTIONS).copy()
            trans["user_id"] = user_id
            trans["date"] = (datetime.utcnow() - timedelta(days=30-i)).isoformat()
            trans["source"] = "manual"
            transactions_to_add.append(trans)
    
    # Add transactions in batches
    response = requests.post(
        f"{API_URL}/transactions/bulk?user_id={user_id}",
        json=transactions_to_add
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Added {data.get('added', 0)} transactions")
    else:
        print(f"❌ Error adding transactions: {response.text}")

def test_endpoints(user_id):
    """Test all main endpoints"""
    print("\n🧪 Testing endpoints...")
    
    # Test predictions
    print("\n1. Testing Cash Crunch Predictor...")
    response = requests.get(f"{API_URL}/predictions/{user_id}")
    if response.status_code == 200:
        pred = response.json()
        print(f"   ✅ Days until cash runs out: {pred['days_until_zero']}")
        print(f"   ✅ Alert: {pred['alert']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test what-if simulator
    print("\n2. Testing What-If Simulator...")
    response = requests.post(
        f"{API_URL}/what-if?user_id={user_id}&purchase_amount=2500&category=shopping"
    )
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ New balance after ₹2500 purchase: ₹{result['new_balance']}")
        print(f"   ✅ Impact: {result['impact_message']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test health score
    print("\n3. Testing Financial Health Score...")
    response = requests.get(f"{API_URL}/health-score/{user_id}")
    if response.status_code == 200:
        score = response.json()
        print(f"   ✅ Score: {score['score']}/100 ({score['category']})")
        print(f"   ✅ Advice: {score['advice']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test coach
    print("\n4. Testing AI Coach...")
    response = requests.post(
        f"{API_URL}/coach?user_id={user_id}&question=How%20can%20I%20save%20more%20money%3F",
        json={}
    )
    if response.status_code == 200:
        coach = response.json()
        print(f"   ✅ Coach response: {coach['response']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test opportunities
    print("\n5. Testing Opportunities...")
    response = requests.get(f"{API_URL}/opportunities/{user_id}")
    if response.status_code == 200:
        opps = response.json()
        print(f"   ✅ Found {len(opps['opportunities'])} opportunities")
        for opp in opps['opportunities'][:2]:
            print(f"      - {opp['title']} ({opp['amount']})")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test transactions
    print("\n6. Testing Transactions...")
    response = requests.get(f"{API_URL}/transactions/{user_id}?days=30")
    if response.status_code == 200:
        trans = response.json()
        print(f"   ✅ Retrieved {len(trans)} transactions")
    else:
        print(f"   ❌ Error: {response.text}")

def main():
    print("🚀 FinSight Database Seeder\n")
    print("This script will populate your database with demo data.\n")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ API is running: {response.json()['status']}\n")
    except:
        print("❌ API is not running. Start it with: python backend.py")
        return
    
    # Create user
    user = create_user()
    if not user:
        print("Failed to create user. Exiting.")
        return
    
    user_id = user['id']
    
    # Add transactions
    print("\nAdding demo transactions...")
    add_transactions(user_id)
    
    # Test endpoints
    test_endpoints(user_id)
    
    print("\n" + "="*60)
    print("✅ Demo data loaded successfully!")
    print(f"   User ID: {user_id}")
    print(f"   Email: {user['email']}")
    print(f"   Monthly Allowance: ₹{user['monthly_allowance']}")
    print("\n💡 Use these credentials to test the app:")
    print(f"   Email: {user['email']}")
    print("\n🎯 Ready to explore FinSight!")
    print("="*60)

if __name__ == "__main__":
    main()
