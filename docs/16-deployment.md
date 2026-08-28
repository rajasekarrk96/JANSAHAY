# 16 — JANSAHAY Deployment & Run Guide

## 1. Docker Compose (Recommended Zero-Setup Method)

The fastest and most isolated way to run the entire JANSAHAY platform (Backend API, Embedded Frontend SPA, SQLite Engine, and Pre-seeded Database) is via Docker Compose:

### 1.1 Quickstart
```bash
# 1. Build and launch container in foreground
docker compose up --build

# Or run in detached daemon mode
docker compose up -d --build
```

### 1.2 Service Endpoints
- **Interactive Web App & Citizen/Officer Portal**: [http://localhost:8000](http://localhost:8000)
- **Interactive OpenAPI Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **API Healthcheck**: `GET http://localhost:8000/health`

### 1.3 Container Architecture & Volume Mapping
- **Context**: `./backend`
- **Port**: `8000:8000`
- **Volume Mount**: `jansahay_storage:/app/storage` (preserves uploaded documents across container restarts)
- **Database Initialization**: Auto-executes `python -m app.db.init_db` during build to prime synthetic test personas and demo records.

---

## 2. Local Development Environment (Native Python)

### 2.1 Prerequisites
- Python 3.11+
- Node.js 18+ & npm (Optional, only if running standalone Vite dev server)
- SQLite (default zero-dependency database)

### 2.2 Quickstart Commands
```bash
# 1. Backend Setup & Virtual Environment
cd backend
python -m venv venv
venv\Scripts\activate       # On Linux/macOS: source venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Seed Database with Personas & Demo Cases
python -m app.db.init_db

# 4. Start Backend API & Embedded Web Server (Port 8000)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 5. Run Automated Security Test Suite
pytest tests/test_platform.py -v
```

---

## 3. Environment Variables Reference

| Variable | Default Value | Description |
|:---|:---|:---|
| `ENVIRONMENT` | `production` | Runtime mode (`development`, `testing`, `production`) |
| `SECRET_KEY` | `jansahay-demo-secret-key-2026` | Secret key used for cryptographic JWT signing |
| `ALGORITHM` | `HS256` | Cryptographic algorithm for access tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` | Access token lifespan (8 hours for demo evaluation) |
| `DATABASE_URL` | `sqlite+aiosqlite:///./jansahay.db` | Async database connection string |
| `STORAGE_PATH` | `./storage/documents` | Sandboxed local filesystem directory for document uploads |
| `CORS_ORIGINS` | `*` | Allowed CORS origins for cross-origin client integration |

---

## 4. Troubleshooting & Known Resolutions

- **Bcrypt Compatibility**: Ensure `bcrypt<4.1.0` is installed when using `passlib` to prevent the 72-byte password length validation error in passlib's legacy initialization probe.
- **Port Conflict (8000)**: If port 8000 is occupied, change the host port in `docker-compose.yml` (e.g. `8080:8000`).
- **Database Reset**: To re-seed fresh demo data at any time, run `python -m app.db.init_db` or trigger `POST /api/demo/reset` with admin credentials.

