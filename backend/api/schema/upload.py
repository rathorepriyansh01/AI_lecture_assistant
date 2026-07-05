"""
=========================================================
AI Lecture Assistant
Upload API
=========================================================
"""

import os
import shutil
import tempfile

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException

from backend.api.responses import APIResponse
from backend.services.videoupload_service import VideoService

router = APIRouter(

    prefix="/upload",

    tags=["Upload"]

)

upload_service = VideoService()


@router.post("/")
async def upload_lecture(

    file: UploadFile = File(...)

):

    try:

        suffix = os.path.splitext(

            file.filename

        )[1]

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=suffix

        ) as temp_file:

            shutil.copyfileobj(
                
                file.file,

                temp_file

            )

            temp_path = temp_file.name

        result = upload_service.create_lecture(

            temp_path

        )

        return APIResponse.success(

            "Lecture processed successfully.",

            result

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

    finally:

        try:

            if os.path.exists(temp_path):

                os.remove(temp_path)

        except:

            pass