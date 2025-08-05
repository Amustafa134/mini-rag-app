from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne



class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_CHUNK_NAME.value
        ]
     
    # Create a new chunk in the database   
    async def create_chunk(self, chunk: DataChunk):
        
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        
        return chunk
    
    # Get a chunk by its ID
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })
        
        # If no chunk is found, return None
        if result is None:
            return None
        # Convert the result to a DataChunk object
        return DataChunk(**result)
    
    # Insert multiple chunks into the database in batches
    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        
        # Insert chunks into the database in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            
            # Prepare the operations for bulk insertion
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]
            # Execute the bulk write operation
            await self.collection.bulk_write(operations)
            
        # Return the number of chunks inserted
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        
        # Delete all chunks associated with a specific project ID
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        
        return result.deleted_count
    