from datetime import datetime
from uuid     import UUID, uuid4
from typing   import List
from pydantic import Field, BaseModel, field_validator

from src.domain.stack_ai.database.in_memory_database      import InMemoryDatabase
from .document                                            import Document
from src.domain.stack_ai.database.indexer.indexer_factory import IndexerFactory

table_name = "library"


class Library(BaseModel):
    id:         UUID = Field(default_factory=uuid4)
    name:       str
    documents:  List[Document]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("[Argument Error] Library name cannot be empty.")
        return value

    @field_validator("document_id")
    def validate_document_id(cls, value):
        if not value.strip():
            raise ValueError("[Argument Error] Chunk - document_id cannot be empty.")
        return value


    # @todo think if we should extract a class with all methods below for all Entities that are stored, as they seem to be the same for all 3 entities
    async def create(self):
        if table_name not in InMemoryDatabase().table_config:
            self.register_index_config()  # @todo add mechanism to check updates in the config too, to update it
        return InMemoryDatabase().insert(table_name, self.model_dump())

    @staticmethod
    async def get_by_id(id: str):
        return InMemoryDatabase().read(table_name, {"id": id})

    async def update_by_id(self, id: str):
        return InMemoryDatabase().update(table_name, self.model_dump(), {"id": id})

    @staticmethod
    async def delete_by_id(id: str):
        return InMemoryDatabase().delete(table_name, {"id": id})

    @staticmethod
    def register_index_config():
        index_config = {
            "indexer": IndexerFactory.make(
                index_type ="binary_search_tree"
            ),
            "index_keys": ["created_at"]
        }
        InMemoryDatabase().register_table(table_name, index_config)

    @staticmethod
    def get_table_name():
        return table_name
