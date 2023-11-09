import logging
from fastapi import (
    HTTPException,
    status,
    APIRouter,
    Depends,
    File,
    UploadFile
)

from source.db.models import User
from source.schemas.users import UserDBModel
from source.services.auth import auth_service
from source.db.connect_db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from source.crud import crud_users
from source.services.cloudinary_service import Cloudinary
from source.services.redis_service import get_redis

router = APIRouter(prefix="/users", tags=["Users"])
cloudinary_service = Cloudinary()


# Get current user's data profile
@router.get("/my_profile", response_model=UserDBModel)
async def get_profile(current_user: User = Depends(auth_service.get_current_user)):
    
    """
    ***Description:***
    
    This endpoint is used to get the current user's data profile. 
    It uses the auth_service to get the current user from the request.
    If the current user is found, it returns a JSON response with the user's data model.
    """
    
    if current_user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    return current_user


# Update user's avatar
@router.patch("/update_avatar", response_model=UserDBModel)
async def update_avatar(
    file: UploadFile = File(), 
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_session)
    ):
    
    """
    ***Description:***
    
    This endpoint is used to update the user's avatar. 
    It accepts a file as an argument, which is the image to be uploaded as the new avatar.
    It uses the cloudinary_service to upload the image and get the source URL.
    It then uses the crud_users to update the user's avatar in the database with the new URL.
    If the user is found and the avatar is updated, it returns a JSON response with the user's data model.
    """
    
    upload_file = file.file
    src_url = cloudinary_service.upload_image(upload_file, current_user.username)
    
    user = await crud_users.update_avatar(current_user.email, src_url, db)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    return user


# Delete user's profile
@router.delete("/delete_profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_session)
    ):
    
    """
    ***Description:***
    
    This endpoint is used to delete the user's profile. It uses the auth_service to get the current user from the request.
    It then uses the crud_users to delete the user from the database by their email.
    If the user is found and deleted, it returns a 204 status code with no content.
    It also uses the redis_service to delete the user's cache data from Redis.
    """
    
    user = await crud_users.delete_user(current_user.email, db)
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        
    async with get_redis() as redis:
        cache_key = f"user:{current_user.email}"
        print(cache_key)
        cache_data = await redis.get(cache_key)
        print(cache_data)
        if cache_data is not None:
            logging.info(
                f"\nRedis: Cache data for user: {current_user.email} deleted from Redis cache.\n"
            )

            await redis.delete(cache_key)
    return user