from fastapi import FastAPI, APIRouter,Depends,UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import Settings,get_settings
from controller import DataController, ProjectController
import os

data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
                    app_settings : Settings=Depends(get_settings)):
    
    is_valid, result=DataController().validat_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result
            }
            )
    
    project_file_path=ProjectController().get_project_path(project_id=project_id)
    file_path=os.path.join(
        project_file_path,
        file.filename
    )
