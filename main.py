from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import get_connection
from database import init_db

app = FastAPI()
init_db()

tasks = [{"id":1,"title":"Buy milk","done":False},{"id":2,"title":"Walk the dog","done":False},{"id":3,"title":"Finish assignment","done":True},]

@app.get("/")
def read_root():
     return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
@app.get("/health")
def health_check():
     return {"status": "ok"}
@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]
@app.post("/tasks",status_code=201)
def create_task(task: dict):
    if "title" not in task or not task["title"]:
     return JSONResponse(status_code=400, content={"error": "Title is required"})       
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id,"title": task["title"],"done":False}
    tasks.append(new_task)
    return new_task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: dict):
    if not updates or ("title" not in updates and "done" not in updates):
        return JSONResponse(status_code=400, content={"error": "Request body must include title or done"})
    for task in tasks:
        if task["id"] == task_id:
            if "title" in updates:
                task["title"] = updates["title"]
            if "done" in updates:
                task["done"] = updates["done"]
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})