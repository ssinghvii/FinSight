#!/bin/bash

# FinSight Quick Start Script
# This script sets up and runs the entire FinSight application

set -e

echo "================================"
echo "  FinSight - Quick Start Setup   "
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python and Node.js detected${NC}"
echo ""

# Setup Python backend
echo -e "${BLUE}Setting up Python Backend...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv\Scripts\activate" ]; then
    source venv/Scripts/activate
else
    echo "Could not activate venv"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo -e "${GREEN}✅ Python backend ready${NC}"
echo ""

# Setup Node frontend
echo -e "${BLUE}Setting up React Frontend...${NC}"
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install --quiet
else
    echo "Node modules already installed"
fi

echo -e "${GREEN}✅ React frontend ready${NC}"
echo ""

# Create .env file
echo -e "${BLUE}Configuring environment...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << EOF
# FinSight Environment Configuration
REACT_APP_API_URL=http://localhost:8000
DATABASE_URL=sqlite:///./finsight.db

# Optional: Add your Google API key for Gemini
# GOOGLE_API_KEY=your-key-here
EOF
    echo "Created .env file"
fi

echo -e "${GREEN}✅ Environment configured${NC}"
echo ""

# Summary
echo "================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================"
echo ""
echo "To start the application:"
echo ""
echo "  Option 1: Run everything (requires 3 terminals)"
echo "    Terminal 1: python backend.py"
echo "    Terminal 2: npm start"
echo "    Terminal 3: python seed_data.py (after backend/frontend start)"
echo ""
echo "  Option 2: Using Docker (requires Docker & Docker Compose)"
echo "    docker-compose up"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "First user credentials (after seed_data.py):"
echo "  Email: priya.sharma@college.com"
echo "  Amount: ₹15,000"
echo ""
echo -e "${YELLOW}💡 Tip: Set GOOGLE_API_KEY in .env for AI Coach feature${NC}"
echo ""
