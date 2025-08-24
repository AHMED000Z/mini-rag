from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import Settings, get_settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import os
import aiofiles
import logging
from .schemas import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemas import DataChunk
logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1", "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):

    project_model = ProjectModel(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(project_id=project_id)
    # Validate the file
    is_valid, result = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result
            }
        )

    file_path, file_id = DataController().generate_unique_filepath(
        original_file_name=file.filename,
        project_id=project_id
    )
    try:
        async with aiofiles.open(file_path, mode='wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f'Error while uploading file: {e}')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )
    return JSONResponse(
        content={
            "signal": result,
            "file_id": file_id
        }
    )


@data_router.post('/process/{project_id}')
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    try:
        file_id = process_request.file_id
        chunk_size = process_request.chunk_size
        overlap_size = process_request.overlap_size

        project_model = ProjectModel(
            db_client=request.app.db_client
        )
        project = await project_model.get_project_or_create_one(project_id=project_id)

        process_controller = ProcessController(project_id=project_id)

        file_content = process_controller.get_file_content(file_id=file_id)

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )

        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROCESSING_FAILED.value
                }
            )

        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id)
            for i, chunk in enumerate(file_chunks)
        ]

        chunk_model = ChunkModel(
            db_client=request.app.db_client
        )

        no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        return JSONResponse(
            content={
                "signal": ResponseSignal.PROCESSING_SUCCESS.value,
                "chunks_created": no_records
            }
        )
    except Exception as e:
        logger.error(f'Error during processing: {e}')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value,
                "error": str(e)
            }
        )
