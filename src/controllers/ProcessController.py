# src/controllers/ProcessController.py
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ProcessingEnum
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os


class ProcessController(BaseController):
    
    # Controller for processing files associated with a project
    def __init__(self, project_id: str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)
    
    # Method to process a file by its ID    
    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]    # -> “.txt”
    
    # Method to get a file loader based on the file type
    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )
        
        if not os.path.exists(file_path):
            return None
        
        print(f"Unsupported file type: {file_ext}")
        if file_ext == ProcessingEnum.TXT.value:
            # For text files, use TextLoader
            return TextLoader(file_path, encoding="utf-8")
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        print(f"Unsupported file type: {file_ext}")
        
        return None  # Unsupported file type
    
    # Method to get the content of a file by its ID
    def get_file_content(self, file_id: str):
        
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        
        return None
    
    def process_file_content(self, file_content: list, file_id: str,
                             chunk_size: int=100 , overlap_size: int=20):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        
        # Extract content and metadata from each document
        file_content_texts = [
            rec.page_content 
            for rec in file_content
        ]
        
        file_content_metadata = [
            rec.metadata 
            for rec in file_content
        ]
        
        # Create overlapping chunks of text, retaining metadata
        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )
        
        return chunks
    