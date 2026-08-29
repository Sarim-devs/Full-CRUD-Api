from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import get_connection, init_db, get_task_by_id, get_all_tasks, insert_task,update_task,delete_task

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
    return get_all_tasks()
@app.post("/tasks",status_code=201)
def create_task(task: dict):
    if "title" not in task or not task["title"]:
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    return insert_task(task["title"])
@app.put("/tasks/{task_id}")
def update_task_route(task_id: int, updates: dict):
    if not updates or ("title" not in updates and "done" not in updates):
        return JSONResponse(status_code=400, content={"error": "Request body must include title or done"})
    row = get_task_by_id(task_id)
    if not row:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    title = updates.get("title", row["title"])
    done = updates.get("done", row["done"])
    return update_task(task_id, title, done)
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_route(task_id: int):
    row = get_task_by_id(task_id)
    if not row:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    delete_task(task_id)
    return
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task:
        return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})