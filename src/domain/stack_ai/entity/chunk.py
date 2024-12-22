from datetime import datetime
from uuid     import UUID, uuid4
from typing   import List
from pydantic import BaseModel, Field, field_validator

from src.domain.stack_ai.database.in_memory_database      import InMemoryDatabase
from src.domain.stack_ai.database.indexer.indexer_factory import IndexerFactory

table_name: str  = "chunk"


class Chunk(BaseModel):
    id:          UUID = Field(default_factory=uuid4)
    document_id: UUID
    library_id:  UUID
    text:        str
    embedding:   List[float]
    created_at:  datetime = Field(default_factory=datetime.utcnow)

    @field_validator("text")
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("[Argument Error] Chunk - text cannot be empty.")
        return value

    @field_validator("document_id")
    def validate_document_id(cls, value):
        if not value.strip():
            raise ValueError("[Argument Error] Chunk - document_id cannot be empty.")
        return value

    @field_validator("library_id")
    def validate_document_id(cls, value):
        if not value.strip():
            raise ValueError("[Argument Error] Chunk - library_id cannot be empty.")
        return value

    # @todo think if we should extract a class with all methods below for all Entities that are stored, as they seem to be the same for all 3 entities
    async def create(self):
        if table_name not in InMemoryDatabase().table_config:
            self.register_index_config()  # @todo add mechanism to check updates in the config too, to update it
        return await InMemoryDatabase().insert(table_name, self.model_dump())

    @staticmethod
    async def get_by_id(id: str):
        return await InMemoryDatabase().read(table_name, {"id": id})

    async def update_by_id(self, id: str):
        return await InMemoryDatabase().update(table_name, self.model_dump(), {"id": id})

    @staticmethod
    async def delete_by_id(id: str):
        return await InMemoryDatabase().delete(table_name, {"id": id})

    @staticmethod
    def register_index_config():  # @todo rethink this plugin approach: it will break if we change the config since it is only registered on table creation time.
        index_config = {
            "indexer": IndexerFactory.make(
                index_type ="binary_search_tree"
            ),
            "index_keys": ["library_id", "document_id", "created_at"]
        }
        InMemoryDatabase().register_table(table_name, index_config)

    @staticmethod
    def get_table_name():
        return table_name
