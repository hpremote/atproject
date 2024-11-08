import uuid
import logging
import markdown
import pytesseract
from PIL import Image
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, Depends, Query
from app.models import UserFiles, Messages
from app.db import get_db
from app.handlers.files3 import file_handler
from app.handlers.img_processing import ImgDetection


ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"]


def get_pagination_params(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return {"page": page, "page_size": page_size}


async def upload_image(file: UploadFile, db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Image type not supported. Only jpeg, jpg, png allowed.")

    file_content = await file.read()

    try:
        s3_url = file_handler.store_s3(file.file, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_file = UserFiles(
        filetype=file.content_type,
        filename=file.filename,
        type="image",
        description=None,
        url=s3_url['url']
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    img = ImgDetection()
    res = img.detect(image_file=file_content)

    user_msg = Messages(
        msg="detect bottles in image",
        sys_msg=res,
        file_id=new_file.id
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    context = {
        'file': {
            'id': new_file.id,
            'name': new_file.filename,
            'url': new_file.url,
        },
        'message': res,
        'message_html': markdown.markdown(res)
    }

    return context


async def list_images(
    filetype: str = 'image',
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_db)
):
    page = pagination["page"]
    page_size = pagination["page_size"]
    offset = (page - 1) * page_size

    query = db.query(UserFiles).order_by(UserFiles.created_at.desc())

    if filetype:
        query = query.filter(UserFiles.type == filetype)

    user_files = query.offset(offset).limit(page_size).all()
    return user_files


async def get_image_text(file: UploadFile, db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Image type not supported. Only jpeg, jpg, png allowed.")

    file_content = await file.read()

    try:
        s3_url = file_handler.store_s3(file.file, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_file = UserFiles(
        filetype=file.content_type,
        filename=file.filename,
        type="image",
        description=None,
        url=s3_url['url']
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # extract text from image
    res = "Failed to extract text!"
    try:
        img = Image.open(file_content)
        res = pytesseract.image_to_string(img)
    except Exception as ocr_err:
        res = str(ocr_err)

    user_msg = Messages(
        msg="detect bottles in image",
        sys_msg=res,
        file_id=new_file.id
    )

    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    context = {
        'file': {
            'id': new_file.id,
            'name': new_file.filename,
            'url': new_file.url,
        },
        'message': res,
        'message_html': markdown.markdown(res)
    }

    return context
