from enum import Enum


class ResponseSignal(Enum):
    
    # General response messages
    FILE_VALIDATED_SUCCESS = "File is validated successfully"
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit"
    FILE_NOT_FOUND = "File not found"
    FILE_ALREADY_EXISTS = "File already exists"
    FILE_NOT_SUPPORTED = "File type not supported"
    
    # File processing status messages
    FILE_PROCESSING_SUCCESS = "File processed successfully"
    FILE_PROCESSING_FAILED = "File processing failed"
    FILE_PROCESSING_ERROR = "Error processing the file"
    
    # File upload status messages
    FILE_UPLOAD_ERROR = "Error uploading the file"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_IN_PROGRESS = "File upload in progress"
    