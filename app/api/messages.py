import logging
from sqlalchemy.orm import Session
from fastapi import  Depends, Query
from app.models import  Messages
from app.db import get_db

logging.basicConfig(level=logging.INFO)


def get_pagination_params(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return {"page": page, "page_size": page_size}


async def list_latest_messages(
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_db)
):
    logging.info("Listing User Messages...")
    page = pagination["page"]
    page_size = pagination["page_size"]
    offset = (page - 1) * page_size

    messages = db.query(Messages).order_by(Messages.created_at.desc()).offset(offset).limit(page_size).all()
    return messages
