import cloudinary
from src.config.appConfig import CLOUDINARY

cloudinary.config(
    cloud_name=CLOUDINARY.CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY.CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY.CLOUDINARY_API_SECRET,
)
