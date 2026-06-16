import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [screen, setScreen] = useState('login');
  const [formData, setFormData] = useState({});

  // Login/Registration
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const user = await response.json();
      setCurrentUser(user);
      setScreen('dashboard');
      setFormData({});
    } catch (error) {
      alert('Error creating user');
    }
  };

  if (!currentUser) {
    return <LoginScreen onLogin={handleLogin} formData={formData} setFormData={setFormData} />;
  }

  switch (screen) {
    case 'dashboard':
      return <Dashboard user={currentUser} onNavigate={setScreen} />;
    case 'predictions':
      return <PredictionsScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    case 'what-if':
      return <WhatIfScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    case 'health-score':
      return <HealthScoreScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    case 'coach':
      return <CoachScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    case 'opportunities':
      return <OpportunitiesScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    case 'transactions':
      return <TransactionsScreen user={currentUser} onBack={() => setScreen('dashboard')} />;
    default:
      return <Dashboard user={currentUser} onNavigate={setScreen} />;
  }
}

function LoginScreen({ onLogin, formData, setFormData }) {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="logo">🎯</div>
        <h1>FinSight</h1>
        <p className="tagline">AI Financial Coach for Indian Students</p>
        
        <form onSubmit={onLogin}>
          <input
            type="text"
            placeholder="Your Name"
            value={formData.name || ''}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email || ''}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Monthly Allowance (₹)"
            value={formData.monthly_allowance || ''}
            onChange={(e) => setFormData({...formData, monthly_allowance: parseFloat(e.target.value)})}
            required
          />
          <input
            type="number"
            placeholder="Monthly Budget (₹)"
            value={formData.monthly_budget || ''}
            onChange={(e) => setFormData({...formData, monthly_budget: parseFloat(e.target.value)})}
            required
          />
          <input
            type="text"
            placeholder="Financial Goal (e.g., Save for laptop)"
            value={formData.financial_goal || ''}
            onChange={(e) => setFormData({...formData, financial_goal: e.target.value})}
          />
          <button type="submit" className="btn-primary">Get Started</button>
        </form>
        
        <p className="footer-text">Stop tracking the past. Start predicting your future.</p>
      </div>
    </div>
  );
}

function Dashboard({ user, onNavigate }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPrediction();
  }, []);

  const fetchPrediction = async () => {
    try {
      const response = await fetch(`${API_URL}/predictions/${user.id}`);
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Welcome, {user.name}! 👋</h1>
          <p>Your AI Financial Coach is ready</p>
        </div>
        <div className="allowance-badge">
          ₹{user.monthly_allowance.toFixed(0)}/month
        </div>
      </header>

      {loading ? (
        <div className="loading">Loading your financial snapshot...</div>
      ) : prediction && (
        <>
          <section className="alert-section">
            <div className={`alert ${prediction.alert.includes('CRITICAL') ? 'alert-danger' : prediction.alert.includes('WARNING') ? 'alert-warning' : 'alert-success'}`}>
              <div className="alert-emoji">{prediction.alert.charAt(0)}</div>
              <div>
                <h3>{prediction.alert.split(' - ')[1]}</h3>
                <p>{prediction.days_until_zero} days until ₹0</p>
              </div>
            </div>
          </section>

          <section className="metrics-grid">
            <MetricCard
              icon="💰"
              title="Current Balance"
              value={`₹${prediction.predicted_balance.toFixed(0)}`}
              subtitle="Estimated for today"
            />
            <MetricCard
              icon="📊"
              title="Spending Pattern"
              value={prediction.spending_pattern.split(' - ')[0]}
              subtitle="Based on last 30 days"
            />
            <MetricCard
              icon="⚡"
              title="Daily Budget"
              value={`₹${(user.monthly_allowance / 30).toFixed(0)}`}
              subtitle="To stay safe"
            />
          </section>

          <section className="feature-cards">
            <FeatureCard
              icon="🔮"
              title="Cash Crunch Predictor"
              description="See when you'll run out of money"
              onClick={() => onNavigate('predictions')}
            />
            <FeatureCard
              icon="❓"
              title="What If Simulator"
              description="Test a purchase before you make it"
              onClick={() => onNavigate('what-if')}
            />
            <FeatureCard
              icon="💪"
              title="Health Score"
              description="Track your financial discipline"
              onClick={() => onNavigate('health-score')}
            />
            <FeatureCard
              icon="🤖"
              title="AI Coach"
              description="Get personalized financial advice"
              onClick={() => onNavigate('coach')}
            />
            <FeatureCard
              icon="🎓"
              title="Opportunities"
              description="Scholarships, internships, side income"
              onClick={() => onNavigate('opportunities')}
            />
            <FeatureCard
              icon="📋"
              title="Transactions"
              description="View your spending history"
              onClick={() => onNavigate('transactions')}
            />
          </section>

          <section className="recommendation-box">
            <h3>💡 Coach's Tip</h3>
            <p>{prediction.recommendation}</p>
          </section>
        </>
      )}
    </div>
  );
}

function PredictionsScreen({ user, onBack }) {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPrediction();
  }, []);

  const fetchPrediction = async () => {
    try {
      const response = await fetch(`${API_URL}/predictions/${user.id}`);
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>🔮 Cash Crunch Predictor</h1>
      </header>

      {loading ? (
        <div className="loading">Analyzing your spending patterns...</div>
      ) : prediction && (
        <div className="screen-content">
          <div className={`prediction-card ${prediction.days_until_zero < 10 ? 'danger' : 'success'}`}>
            <h2>Days Until Cash Runs Out</h2>
            <div className="big-number">{prediction.days_until_zero}</div>
            <div className="bar-chart">
              <div className="bar" style={{width: Math.min(prediction.days_until_zero * 3, 100) + '%'}}></div>
            </div>
          </div>

          <div className="info-boxes">
            <InfoBox
              title="Predicted Balance"
              value={`₹${prediction.predicted_balance.toFixed(0)}`}
              icon="💵"
            />
            <InfoBox
              title="Status"
              value={prediction.alert}
              icon="🚨"
            />
          </div>

          <div className="detail-section">
            <h3>Spending Pattern Analysis</h3>
            <p className="pattern">{prediction.spending_pattern}</p>
            
            <h3>Recommendation</h3>
            <p className="recommendation">{prediction.recommendation}</p>

            <div className="warning-box">
              <h4>⚠️ What You Need to Know</h4>
              <ul>
                <li>This prediction is based on your last 30 days of spending</li>
                <li>Recurring expenses (subscriptions, recharges) are included</li>
                <li>Your actual numbers may vary based on monthly variations</li>
                <li>Act NOW if you're in the danger zone</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function WhatIfScreen({ user, onBack }) {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('food');
  const [result, setResult] = useState(null);

  const categories = ['food', 'entertainment', 'education', 'shopping', 'utilities', 'other'];

  const handleSimulate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/what-if?user_id=${user.id}&purchase_amount=${parseFloat(amount)}&category=${category}`);
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>❓ What If Simulator</h1>
      </header>

      <div className="screen-content">
        <p className="subtitle">Test the impact of a purchase BEFORE you make it</p>

        <form onSubmit={handleSimulate} className="what-if-form">
          <div className="form-group">
            <label>Amount (₹)</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0"
              required
            />
          </div>

          <div className="form-group">
            <label>Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn-primary">Simulate Purchase</button>
        </form>

        {result && (
          <div className="result-section">
            <div className={`impact-banner ${result.impact_message.includes('SAFE') ? 'success' : result.impact_message.includes('RISKY') ? 'danger' : 'warning'}`}>
              <h2>{result.impact_message}</h2>
            </div>

            <div className="result-grid">
              <ResultBox
                title="Purchase Amount"
                value={`₹${result.purchase_amount.toFixed(0)}`}
                icon="🛍️"
              />
              <ResultBox
                title="Balance After"
                value={`₹${result.new_balance.toFixed(0)}`}
                icon="💰"
              />
              <ResultBox
                title="Days You Can Last"
                value={result.days_remaining}
                icon="📅"
              />
            </div>

            <div className="opportunity-cost">
              <h3>💡 Opportunity Cost</h3>
              <p className="highlight">₹{result.purchase_amount.toFixed(0)} {result.opportunity_cost}</p>
              <p className="small">Think of it in terms of other things you could afford instead</p>
            </div>

            <div className="decision-box">
              <h4>🤔 How to Decide?</h4>
              <ul>
                <li>Is it a need or a want?</li>
                <li>Can you wait until next month?</li>
                <li>Would this impact your goals?</li>
                <li>What's the opportunity cost worth to you?</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function HealthScoreScreen({ user, onBack }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealthScore();
  }, []);

  const fetchHealthScore = async () => {
    try {
      const response = await fetch(`${API_URL}/health-score/${user.id}`);
      const data = await response.json();
      setScore(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>💪 Financial Health Score</h1>
      </header>

      {loading ? (
        <div className="loading">Calculating your score...</div>
      ) : score && (
        <div className="screen-content">
          <div className="score-circle">
            <div className="score-number">{score.score}</div>
            <div className="score-label">/100</div>
          </div>

          <div className={`score-category ${score.category.toLowerCase()}`}>
            {score.category}
          </div>

          <div className="breakdown">
            <BreakdownItem
              label="Budget Discipline"
              value={score.breakdown.budget_discipline}
              icon="📋"
            />
            <BreakdownItem
              label="Consistency"
              value={score.breakdown.consistency}
              icon="📊"
            />
            <BreakdownItem
              label="Savings Rate"
              value={score.breakdown.savings_rate}
              icon="💎"
            />
          </div>

          <div className="advice-box">
            <h3>📈 Advice</h3>
            <p>{score.advice}</p>
          </div>

          <div className="score-info">
            <h4>How is this calculated?</h4>
            <ul>
              <li><strong>Budget Discipline (40 points):</strong> How close you stick to your budget</li>
              <li><strong>Consistency (30 points):</strong> How stable your spending patterns are</li>
              <li><strong>Savings Rate (30 points):</strong> How much of your allowance you save</li>
            </ul>
            <p className="note">Unlike other apps that judge wealth, we judge discipline. Everyone can improve their score!</p>
          </div>
        </div>
      )}
    </div>
  );
}

function CoachScreen({ user, onBack }) {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/coach?user_id=${user.id}&question=${encodeURIComponent(question)}`, {
        method: 'POST'
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setResponse('Sorry, I couldn\'t get a response. Try again!');
    } finally {
      setLoading(false);
    }
  };

  const quickQuestions = [
    'How can I save more money?',
    'Why am I spending so much on food?',
    'Should I get a part-time job?',
    'How do I build good money habits?',
    'What should I do with my savings?'
  ];

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>🤖 AI Financial Coach</h1>
      </header>

      <div className="screen-content coach-content">
        <div className="coach-intro">
          <div className="coach-avatar">🤖</div>
          <p>Hi {user.name}! I'm your AI coach. Ask me anything about money, spending, or goals!</p>
        </div>

        <form onSubmit={handleAsk} className="coach-form">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask me anything about your finances..."
            disabled={loading}
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Thinking...' : 'Ask Coach'}
          </button>
        </form>

        {response && (
          <div className="coach-response">
            <h3>Coach's Response:</h3>
            <p>{response}</p>
          </div>
        )}

        <div className="quick-questions">
          <h4>Quick Questions:</h4>
          <div className="question-list">
            {quickQuestions.map((q, idx) => (
              <button
                key={idx}
                className="quick-btn"
                onClick={() => setQuestion(q)}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function OpportunitiesScreen({ user, onBack }) {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOpportunities();
  }, []);

  const fetchOpportunities = async () => {
    try {
      const response = await fetch(`${API_URL}/opportunities/${user.id}`);
      const data = await response.json();
      setOpportunities(data.opportunities);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const typeIcons = {
    'Scholarship': '🎓',
    'Internship': '💼',
    'Side Income': '💸',
    'Grant': '🎁'
  };

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>🎓 Opportunities</h1>
      </header>

      {loading ? (
        <div className="loading">Finding opportunities for you...</div>
      ) : (
        <div className="screen-content">
          <p className="subtitle">Scholarships, internships, and side income to boost your finances</p>

          <div className="opportunities-list">
            {opportunities.map((opp, idx) => (
              <OpportunityCard key={idx} opportunity={opp} icon={typeIcons[opp.type]} />
            ))}
          </div>

          <div className="tips-box">
            <h3>💡 How to Maximize:</h3>
            <ul>
              <li>Apply for scholarships ASAP - deadlines pass quickly</li>
              <li>Internships not only pay, they build your CV</li>
              <li>Side income sources like writing/tutoring are flexible</li>
              <li>Even ₹5-10K extra per month changes everything</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

function TransactionsScreen({ user, onBack }) {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ amount: '', category: 'food', description: '' });

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await fetch(`${API_URL}/transactions/${user.id}`);
      const data = await response.json();
      setTransactions(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTransaction = async (e) => {
    e.preventDefault();
    try {
      await fetch(`${API_URL}/transactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          amount: parseFloat(formData.amount),
          category: formData.category,
          description: formData.description,
          source: 'manual'
        })
      });
      setFormData({ amount: '', category: 'food', description: '' });
      setShowForm(false);
      fetchTransactions();
    } catch (error) {
      alert('Error adding transaction');
    }
  };

  const categories = ['food', 'entertainment', 'education', 'shopping', 'utilities', 'other'];
  const categoryEmojis = {
    'food': '🍔',
    'entertainment': '🎬',
    'education': '📚',
    'shopping': '🛍️',
    'utilities': '⚡',
    'other': '📌'
  };

  return (
    <div className="screen">
      <header className="screen-header">
        <button onClick={onBack} className="btn-back">← Back</button>
        <h1>📋 Transactions</h1>
      </header>

      <div className="screen-content">
        <button onClick={() => setShowForm(!showForm)} className="btn-secondary">
          {showForm ? '✕ Cancel' : '+ Add Transaction'}
        </button>

        {showForm && (
          <form onSubmit={handleAddTransaction} className="transaction-form">
            <input
              type="number"
              placeholder="Amount"
              value={formData.amount}
              onChange={(e) => setFormData({...formData, amount: e.target.value})}
              required
            />
            <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})}>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Description"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
            <button type="submit" className="btn-primary">Add</button>
          </form>
        )}

        {loading ? (
          <div className="loading">Loading transactions...</div>
        ) : (
          <div className="transactions-list">
            {transactions.length === 0 ? (
              <p className="empty-state">No transactions yet. Add your first one!</p>
            ) : (
              transactions.map(trans => (
                <div key={trans.id} className="transaction-item">
                  <div className="trans-icon">{categoryEmojis[trans.category] || '📌'}</div>
                  <div className="trans-info">
                    <div className="trans-desc">{trans.description}</div>
                    <div className="trans-date">{new Date(trans.date).toLocaleDateString()}</div>
                  </div>
                  <div className="trans-amount">₹{trans.amount.toFixed(0)}</div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Helper Components
function MetricCard({ icon, title, value, subtitle }) {
  return (
    <div className="metric-card">
      <div className="metric-icon">{icon}</div>
      <div className="metric-content">
        <div className="metric-label">{title}</div>
        <div className="metric-value">{value}</div>
        <div className="metric-subtitle">{subtitle}</div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description, onClick }) {
  return (
    <div className="feature-card" onClick={onClick}>
      <div className="feature-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="feature-arrow">→</div>
    </div>
  );
}

function InfoBox({ title, value, icon }) {
  return (
    <div className="info-box">
      <div className="info-icon">{icon}</div>
      <div className="info-content">
        <div className="info-label">{title}</div>
        <div className="info-value">{value}</div>
      </div>
    </div>
  );
}

function ResultBox({ title, value, icon }) {
  return (
    <div className="result-box">
      <div className="result-icon">{icon}</div>
      <div className="result-label">{title}</div>
      <div className="result-value">{value}</div>
    </div>
  );
}

function BreakdownItem({ label, value, icon }) {
  return (
    <div className="breakdown-item">
      <div className="breakdown-icon">{icon}</div>
      <div className="breakdown-label">{label}</div>
      <div className="breakdown-bar">
        <div className="breakdown-fill" style={{width: value + '%'}}></div>
      </div>
      <div className="breakdown-value">{Math.round(value)}/30</div>
    </div>
  );
}

function OpportunityCard({ opportunity, icon }) {
  return (
    <div className="opportunity-card">
      <div className="opp-header">
        <div className="opp-icon">{icon}</div>
        <div>
          <div className="opp-type">{opportunity.type}</div>
          <div className="opp-title">{opportunity.title}</div>
        </div>
      </div>
      <div className="opp-body">
        <div className="opp-amount">{opportunity.amount}</div>
        <p className="opp-impact">{opportunity.impact}</p>
        <div className="opp-deadline">Deadline: {opportunity.deadline}</div>
      </div>
      <a href={opportunity.link} className="opp-link">Learn More →</a>
    </div>
  );
}
