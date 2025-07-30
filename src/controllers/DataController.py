# Import base controller and other dependencies
from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import re
import os

class DataController(BaseController):

    def __init__(self):
        
        super().__init__()
        self.size_scale = 1048576  # convert MB to bytes
                
    async def validate_upload_file(self, file: UploadFile):
        
        # Check file content type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_NOT_SUPPORTED.value
        
        # Check file size
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED .value
        
        # If all checks pass
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    # Generate a random string for file naming
    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        
        # Generate a random string for the file name
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        
        cleaned_file_name = self.get_clean_file_name(
            orig_file_name= orig_file_name
        )
        
        # Create the new file path with the random string and cleaned file name
        new_file_path = os.path.join(
            project_path,
            random_key + '_' + cleaned_file_name            
        )
        
        while os.path.exists(new_file_path):
            # If the file already exists, generate a new random string
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + '_' + cleaned_file_name
            )
        # Return the new file path
        return new_file_path, random_key + '_' + cleaned_file_name
        
    def get_clean_file_name(self, orig_file_name: str):
        
        # Remove special characters and spaces, replace with underscores
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())
        
        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(' ', '_')
        
        return cleaned_file_name
    