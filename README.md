# GenAI-Journey
My 6-month roadmap to becoming a GenAI Engineer
# Employee Management API 🚀

A production-style REST API built with FastAPI, SQLAlchemy, and Pandas.
Built as part of my 6-month GenAI Engineering roadmap targeting Meta.

## Tech Stack
- **Python** — core language
- **FastAPI** — REST API framework
- **SQLAlchemy** — database ORM
- **SQLite** — database
- **Pandas** — data analytics
- **Uvicorn** — ASGI server

## Features
- Full CRUD operations via REST API
- Bulk employee insertion
- Auto-generated Swagger documentation
- Pandas-powered data analytics
- Clean modular project structure

## Project Structure
app/

├── database.py   → DB connection

├── models.py     → Pydantic models

└── routes.py     → API endpoints

main.py           → Entry point

requirements.txt  → Dependencies

## Setup & Run

### 1. Clone the repository
git clone https://github.com/your-username/genai-journey.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the API
uvicorn main:app --reload

### 4. Open Swagger UI
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /employees | Get all employees |
| POST | /employees | Add single employee |
| POST | /employees/bulk | Add multiple employees |
| PUT | /employees/{name} | Update salary |
| DELETE | /employees/{name} | Remove employee |

## Author
Varun Sharma — Aspiring GenAI Engineer