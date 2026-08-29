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
    conn = get_connection()
    cursor = conn.execute("INSERT INTO tasks (title, done) VALUES (?, ?)",(task["title"], 0))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": task["title"], "done": False}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: dict):
    if not updates or ("title" not in updates and "done" not in updates):
        return JSONResponse(status_code=400, content={"error": "Request body must include title or done"})
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    title = updates.get("title", row["title"])
    done = updates.get("done", row["done"])
    conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
    conn.commit()
    conn.close()
    return {"id": task_id, "title": title, "done": bool(done)}
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})