# Import necessary FastAPI modules and helpers
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
import aiofiles
import logging

# Import application settings and controllers
from helpers.config import get_settings, Settings
from controllers.ProjectController import ProjectController
from controllers.ProcessController import ProcessController
from controllers.DataController import DataController
from models import ResponseSignal
from .schemes.data import ProcessRequest


logger = logging.getLogger('uvicorn.error')

# Define the router for data-related API endpoints
data_router = APIRouter(
    prefix="/api/v1/data",  # Base path for this router
    tags=["api_v1", "data"],    # Tags for grouping in Swagger docs
)

# ----------------------------------------------
# Endpoint: Upload a file to a specific project
# ----------------------------------------------

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    
    
    # Validate file properties
    
    data_controller = DataController()
    
    is_valid, result_signal = await data_controller.validate_upload_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": result_signal
            }
        )
        
    # Save the file to the project directory
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEfAULT_CHUNK_SIZE):
                await f.write(chunk)
    
    except Exception as e:
        
        logger.error(f"Error saving file {file.filename} for project {project_id}: {e}")
        
        # Handle any exceptions that occur during file writing
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "Signal": ResponseSignal.FILE_UPLOAD_FAILED.value,
            }
        )
            
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "File ID": file_id,
            "File Path": file_path
        }
    )
    
# ----------------------------------------------
# Endpoint: Process a previously uploaded file
# ----------------------------------------------

@data_router.post("/process/{project_id}")
async def process_data(project_id: str, process_request: ProcessRequest):
    
    # Validate the project ID
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    
    process_controller = ProcessController(project_id=project_id)
    
    file_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
    
    # Check if file chunks were created successfully
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "Signal": ResponseSignal.FILE_NOT_FOUND.value
            }
        )
    
    return file_chunks