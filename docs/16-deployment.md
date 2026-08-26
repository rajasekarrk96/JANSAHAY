# 16 — JANSAHAY Deployment & Run Guide

## 1. Local Development Environment

### 1.1 Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- SQLite (default for instant zero-dependency local run) or PostgreSQL

### 1.2 Quickstart Commands
```bash
# 1. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.db.init_db

# 2. Start Backend API Server (Port 8000)
uvicorn app.main:app --reload --port 8000

# 3. Frontend Setup
cd ../frontend
npm install
npm run dev # Runs on Port 3000
```

---

## 2. Environment Variables (`.env`)
```env
ENVIRONMENT=development
SECRET_KEY=jansahay-super-secret-jwt-key-for-hackathon-2026
DATABASE_URL=sqlite+aiosqlite:///./jansahay.db
STORAGE_PATH=./storage/documents
OPENAI_API_KEY=mock-or-optional-key
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
