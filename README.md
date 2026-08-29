# Task CRUD API

A small CRUD API for managing tasks, built with FastAPI. Stores tasks in memory (no database yet).

## How to run

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate`
3. Install dependencies: `pip install fastapi uvicorn`
4. Run the server: `uvicorn main:app --reload`
5. Visit `http://127.0.0.1:8000/docs` for interactive API docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | API info |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create a task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example request


curl -i http://127.0.0.1:8000/tasks

Response:

HTTP/1.1 200 OK
date: Sat, 29 Aug 2026 20:22:20 GMT
server: uvicorn
content-length: 125
content-type: application/json

[{"id":1,"title":"Buy milk","done":0},{"id":2,"title":"Walk the dog","done":0},{"id":3,"title":"Finish assignment","done":1}]


## Swagger UI

![Swagger UI](./Full%20Crud%20Api.png)

## Database (Week 3)

Tasks are now stored in a SQLite database (`tasks.db`) instead of memory. Data survives server restarts.

**Why SQLite:** no separate server to install, the whole database is one file, perfect for a small project like this.

**Database file:** `tasks.db`, created automatically on first run. The `tasks` table is created if missing, and 3 example tasks are seeded only if the table is empty (so restarting never duplicates them).

**Example SQL query:**
\`\`\`sql
SELECT * FROM tasks WHERE done = 1;
\`\`\`
This returns only the tasks marked as completed.

![DB Browser screenshot](./Database.png)