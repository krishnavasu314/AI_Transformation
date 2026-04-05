# AI-Powered Task & Knowledge Management System

This project is a full-stack MVP for a task and knowledge management workflow where:

- Admins upload documents and assign tasks
- Users search the knowledge base with semantic search
- Users complete assigned tasks from the same application

The solution was built to match the assignment requirements with a clean backend structure, a usable React dashboard, MySQL-based relational storage, and FAISS-based vector search.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PyMySQL, JWT, Passlib
- Frontend: React, Vite, Axios
- Database: MySQL 8
- AI Search: Sentence Transformers + FAISS
- File Handling: `.txt` document upload and chunking

## Core Features

- JWT authentication
- Role-based access control with `admin` and `user`
- MySQL relational schema with PK/FK relationships
- Task creation, assignment, and status updates
- Document upload and metadata storage
- Embedding-based semantic search
- Activity logging
- Basic analytics dashboard
- Task filtering support

## Roles

### Admin

- Login to the system
- Upload `.txt` documents
- Create and assign tasks
- View analytics and search trends

### User

- Login to the system
- View assigned tasks
- Search uploaded documents
- Update task status from `pending` to `completed`

## Required APIs Implemented

- `POST /auth/login`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `GET /documents`
- `POST /documents`
- `POST /search`
- `GET /analytics`

Additional helper endpoint:

- `GET /users`

## Project Structure

```text
Transformation/
  backend/
    app/
      api/routes/
      core/
      models/
      schemas/
      services/
      utils/
    storage/
    requirements.txt
    docker-compose.yml
  frontend/
    src/
  README.md
```

## Database Design

The application uses MySQL with the following core tables:

- `roles`
- `users`
- `tasks`
- `documents`
- `activity_logs`

Key relationships:

- One role can have many users
- One user can create many tasks
- One user can be assigned many tasks
- One user can upload many documents
- One user can create many activity logs

## Semantic Search Flow

1. Admin uploads a `.txt` document
2. The backend reads and chunks the text into smaller passages
3. Each passage is converted into an embedding using a Sentence Transformer model
4. Embeddings are stored in a FAISS index
5. When a user searches, the query is embedded
6. FAISS returns the closest matching passages
7. Matching passages are shown in the frontend

This ensures the search is embedding-based and not dependent only on LLM API calls.

## Setup Instructions

## Prerequisites

Make sure these are installed:

- Python 3.13+
- Node.js + npm
- Docker Desktop or MySQL installed locally

## 1. Clone or open the project

```bash
cd Transformation
```

## 2. Backend environment setup

Go to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv env
```

Activate it on Windows PowerShell:

```bash
.\env\Scripts\Activate.ps1
```

If PowerShell blocks execution:

```bash
Set-ExecutionPolicy -Scope Process Bypass
.\env\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Create `.env` inside `backend/` from the example:

```bash
copy .env.example .env
```

Use values like this:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/task_knowledge_db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_INDEX_PATH=storage/faiss.index
VECTOR_METADATA_PATH=storage/faiss_meta.json
DOCUMENTS_DIR=storage/documents
CORS_ORIGINS=http://localhost:5173
```

Notes:

- Change `DATABASE_URL` if your MySQL username or password is different
- Change `JWT_SECRET_KEY` to your own random secret
- The storage paths can stay unchanged for local development

## 4. Start MySQL

### Option A: Docker

From `backend/`:

```bash
docker compose up -d
```

This starts MySQL on port `3306`.

### Option B: Local MySQL

If you already have MySQL installed locally:

- make sure the MySQL server is running
- create the database:

```sql
CREATE DATABASE task_knowledge_db;
```

## 5. Run the backend

From `backend/` with the virtual environment active:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## 6. Run the frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

- `http://localhost:5173`

## Default Credentials

- Admin: `admin` / `admin123`
- User: `user1` / `user123`

## How to Test the Flow

### Admin flow

1. Login as admin
2. Upload a `.txt` file
3. Create a task and assign it to `user1`
4. View analytics and search trends

### User flow

1. Login as user
2. View assigned tasks
3. Search the uploaded document
4. Mark the assigned task as completed

## Filtering Support

The tasks API supports dynamic filtering:

- `GET /tasks?status=completed`
- `GET /tasks?assigned_to=1`

## Activity Logging

The system records:

- Login
- Task update
- Document upload
- Search

These logs are stored in MySQL and used for analytics.

## Analytics Included

The dashboard shows:

- Total tasks
- Completed tasks
- Pending tasks
- Total searches
- Top searched queries

## Short Explanation

This application combines task management and document retrieval into one workflow. Admins build a small internal knowledge base by uploading text documents and assigning work. Users search those documents using embedding similarity, retrieve relevant passages, and complete tasks using the information they find. The backend is organized into routes, models, schemas, and services so the code stays maintainable and easy to extend.
