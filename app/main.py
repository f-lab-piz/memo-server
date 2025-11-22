from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Memo Server", version="0.1.0")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.get("/memos", response_model=list[schemas.MemoRead], tags=["memos"])
def list_memos(db: Session = Depends(get_db)):
    return crud.list_memos(db)


@app.post(
    "/memos",
    response_model=schemas.MemoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["memos"],
)
def create_memo(memo_in: schemas.MemoCreate, db: Session = Depends(get_db)):
    return crud.create_memo(db, memo_in)


@app.get("/memos/{memo_id}", response_model=schemas.MemoRead, tags=["memos"])
def read_memo(memo_id: int, db: Session = Depends(get_db)):
    memo = crud.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return memo


@app.put("/memos/{memo_id}", response_model=schemas.MemoRead, tags=["memos"])
def update_memo(memo_id: int, memo_in: schemas.MemoUpdate, db: Session = Depends(get_db)):
    memo = crud.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return crud.update_memo(db, memo, memo_in)


@app.delete("/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["memos"])
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    memo = crud.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    crud.delete_memo(db, memo)
    return None
