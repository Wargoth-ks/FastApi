import cloudinary
import cloudinary.uploader
from configs import settings


class Cloudinary:
    def __init__(self, settings=settings):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

    def upload_image(self, upload_file, username):
        image = cloudinary.uploader.upload(upload_file, public_id=f'fast_api_users/{username}', overwrite=True)
        image_url = cloudinary.CloudinaryImage(
            f'fast_api_users/{username}'
            ).build_url(width=250, height=250, crop='fill', version=image.get('version'))
        return image_url
