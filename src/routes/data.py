# Import necessary FastAPI modules and helpers
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import aiofiles
import logging

# Import application settings and controllers
from helpers.config import get_settings, Settings
# Import controllers for handling project and data operations
from controllers.ProjectController import ProjectController
from controllers.ProcessController import ProcessController
from controllers.DataController import DataController
# Import models and schemas
from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
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
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    
    # Validate the project ID
    project_model = ProjectModel(
        db_client=request.app.db_client
    )
    
    # Check if the project exists or create a new one
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    
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
            "Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value, # Indicate successful upload
            "File ID": file_id, # Unique identifier for the uploaded file
            "File Path": file_path, # Path where the file is saved
            
        }
    )
    
# ----------------------------------------------
# Endpoint: Process a previously uploaded file
# ----------------------------------------------

@data_router.post("/process/{project_id}")
async def process_data(request: Request, project_id: str, process_request: ProcessRequest):
    
    # Validate the project ID
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    
    # Check if the project exists or create a new one
    project_model = ProjectModel(
        db_client = request.app.db_client
    )
    
    # Get or create the project
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    
    process_controller = ProcessController(project_id=project_id)
    
    # Get the content of the file to be processed
    file_content = process_controller.get_file_content(file_id=file_id)
    
    # Process file into text chunks
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
        
     # Insert processed chunks into the database
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,  # Start order from 1
            chunk_project_id=project.id,
        )
        # Use enumerate to get both index and chunk
        for i, chunk in enumerate(file_chunks)
    ]
    
    # Create a ChunkModel instance to handle database operations
    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )
    
    # If do_reset is set, delete existing chunks for the project
    if do_reset == 1:
        deleted_count = await chunk_model.delete_chunks_by_project_id(project_id=project.id)
    else:
        deleted_count = 0
    
    
    #Insert the file chunks into the database
    no_records = await chunk_model.insert_many_chunks(
        chunks=file_chunks_records
    )
    
    # Return a JSON response indicating success
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "Signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,  # Indicate successful processing
            "File ID": file_id,  # ID of the processed file
            "Project ID": project_id,  # ID of the project being processed
            "Inserted Chunks": no_records,  # Number of records inserted
            "Deleted Chunks": deleted_count, # Number of chunks deleted if do_reset was set
        }
    )
    
    