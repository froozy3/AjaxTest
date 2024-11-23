import uvicorn
from fastapi import FastAPI, Depends
from db import get_db, Status

app = FastAPI()

SessionLocal = get_db()


@app.post("/setStatus")
def create(status: str, session: SessionLocal = Depends(get_db)):
    status_db = Status(status=status)
    session.add(status_db)
    session.commit()
    return {"message": "status created successfully!"}


@app.patch("/updateStatus")
def update(id: int, version: str, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    status_db.version = version
    session.commit()
    return {"message": "status updated successfully!"}


@app.put("/rewriteStatus")
def rewrite(id: int, status: str, version: str, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    status_db.status, status_db.version = status, version
    session.commit()
    return {"message": "status updated successfully!"}


@app.delete("/updateStatus/{id}")
def delete(id: int, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    session.delete(status_db)
    session.commit()
    return {"message": "status deleted successfully!"}


@app.get("/status/{id}")
def get(id: int, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    return {"message": status_db}

#
# @app.post('/rollbackStatusVersion')
# def rollback()

if __name__ == "__main__":
    uvicorn.run(app=app)
