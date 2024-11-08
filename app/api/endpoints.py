from fastapi import APIRouter
from .images import upload_image, list_images
from .messages import list_latest_messages


api_router = APIRouter()


api_router.add_api_route('/images', upload_image, methods=['POST'])
api_router.add_api_route('/images', list_images, methods=['GET'])
api_router.add_api_route('/messages', list_latest_messages, methods=['GET'])
