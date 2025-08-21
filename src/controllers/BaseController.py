from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    
    def __init__(self):
        
        # Load application settings from config
        self.app_settings = get_settings()
        
        # Set the base directory for file operations
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )
        
    # Generate a random string of specified length    
    def generate_random_string(self, length: int = 10):
        return ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=length
        ))
        