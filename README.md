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

\`\`\`
curl -i http://127.0.0.1:8000/tasks
\`\`\`

## Swagger UI

![Swagger UI](Full%20Crud%20Api.png)