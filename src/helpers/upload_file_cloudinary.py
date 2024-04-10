import cloudinary
from cloudinary.uploader import upload
import io
from fastapi import UploadFile


# Define the upload_file function as an async function
async def upload_file(file: UploadFile, new_img_file_name: str, dir_address: str):
    try:

        # Upload the file to Cloudinary
        result = upload(
            file=file.file,
            resource_type="auto",
            public_id=new_img_file_name,
            folder=dir_address,
        )

        return result
    except Exception as error:
        print(error)
        raise error
