import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from db import get_db, Status

app = FastAPI()

SessionLocal = get_db()


@app.post("/setStatus")
def create(status: str, session: SessionLocal = Depends(get_db)):
    existing_status = session.query(Status).filter(Status.status == status).first()

    if existing_status:
        raise HTTPException(status_code=422, detail="Such a status already exists")

    status_db = Status(status=status)
    session.add(status_db)
    session.commit()
    return {"message": "status created successfully!"}


@app.patch("/updateStatus")
def update(id: int, version: float, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    if not status_db:
        raise HTTPException(status_code=404, detail=f"Status not found by id")

    if version <= 0:
        raise HTTPException(status_code=400, detail="Version must be positive float or greater than 0")

    if version != (round(status_db.version + 0.1, 1)):
        raise HTTPException(status_code=400, detail="Version can only increase by 0.1")

    status_db.version = version
    session.commit()
    return {"message": "status updated successfully!"}


@app.put("/rewriteStatus")
def rewrite(id: int, status: str, version: float, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)
    if not status_db:
        raise HTTPException(status_code=404, detail=f"Status not found by id")

    if version <= 0:
        raise HTTPException(status_code=400, detail="Version must be positive float or greater than 0")

    if version != (round(status_db.version + 1)):
        raise HTTPException(status_code=400, detail="Version can only increase by 1")

    status_db.status, status_db.version = status, version
    session.commit()
    return {"message": "status rewrote successfully!"}


@app.delete("/removeStatus/{id}")
def delete(id: int, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)

    if not status_db:
        raise HTTPException(status_code=404, detail=f"Status not found by id")
    session.delete(status_db)
    session.commit()
    return {"message": "status deleted successfully!"}


@app.get("/status/{id}")
def get(id: int, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)

    if not status_db:
        raise HTTPException(status_code=404, detail=f"Status not found by id")

    return {"message": status_db}


@app.post('/rollbackStatusVersion')
def rollback(id: int, session: SessionLocal = Depends(get_db)):
    status_db = session.get(Status, id)

    if not status_db:
        raise HTTPException(status_code=404, detail=f"Status not found by id")

    if status_db.version > 1:

        if round(status_db.version - 1, 1) < 1:
            raise HTTPException(status_code=400, detail="Cannot rollback. Version cannot go below 1.")

        status_db.version -= 1
        session.commit()
        return {"message": "status rolled back successfully!"}
    raise HTTPException(status_code=400, detail="Ooops! Status has a version smaller than 1 or stored value is 1")


if __name__ == "__main__":
    uvicorn.run(app=app)
