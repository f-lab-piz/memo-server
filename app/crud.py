from sqlalchemy.orm import Session

from . import models, schemas


def list_memos(db: Session):
    return db.query(models.Memo).order_by(models.Memo.created_at.desc()).all()


def get_memo(db: Session, memo_id: int):
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def create_memo(db: Session, memo_in: schemas.MemoCreate):
    memo = models.Memo(title=memo_in.title, content=memo_in.content)
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def update_memo(db: Session, memo: models.Memo, memo_in: schemas.MemoUpdate):
    if memo_in.title is not None:
        memo.title = memo_in.title
    if memo_in.content is not None:
        memo.content = memo_in.content
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def delete_memo(db: Session, memo: models.Memo):
    db.delete(memo)
    db.commit()
