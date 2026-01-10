from .BaseController import BaseController
from models import ResponseSignal
from fastapi import UploadFile
import os


class ProjectController(BaseController):

    def __init__(self):
        super().__init__()
        
    # Construct the project path based on the project ID
    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.files_dir,
            project_id
        )
    # Ensure the project directory exists    
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
    # Return the project directory path            
        return project_dir
     