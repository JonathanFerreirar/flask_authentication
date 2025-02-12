import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from cloudinary.exceptions import Error


load_dotenv()


class CloudinaryUploader:
    def __init__(self, cloud_name=os.getenv("CLOUD_NAME"), api_key=os.getenv("CLOUD_API_KEY"), api_secret=os.getenv("CLOUD_API_SECRET")):

        self.config = cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )

    def upload_file(self, file_path: str, public_id: str, asset_folder: str = 'etechs') -> dict:
        """
        Faz o upload de um arquivo para o Cloudinary.

        Args:
            file_path (str): Caminho do arquivo ou URL.
            public_id (str): public ID is used to identify the image on cloudinary.
            asset_folder (str, default='etechs'): represents the folder where the image will be placed.

        Returns:
            dict: Retorna o URL seguro do arquivo ou mensagem de erro.
        """
        try:

            # Realiza o upload no Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                display_name=public_id,
                asset_folder=asset_folder
            )
            return {"success": True, "secure_url": upload_result.get("secure_url"), "id":  upload_result.get("public_id")}
        except Error as e:
            return {"success": False, "error": str(e)}

    def update_file(self, file_path: str, public_id: str, asset_folder: str = 'etechs') -> dict:

        if not public_id:
            return {"success": False, "error": str('Por favor adicione um public_id')}

        """
        Faz o upload de um arquivo para o Cloudinary.

        Args:
            file_path (str): Caminho do arquivo ou URL.
            public_id (str): Public ID é usado para identificar o arquivo no Cloudinary.
            asset_folder (str, default='etechs'): Pasta onde o arquivo será armazenado no Cloudinary.

        Returns:
            dict: Retorna o URL seguro do arquivo ou mensagem de erro.
        """
        try:
            upload_result = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                asset_folder=asset_folder
            )
            return {"success": True, "secure_url": upload_result.get("secure_url"), "id":  upload_result.get("public_id")}
        except Error as e:
            return {"success": False, "error": str(e)}
