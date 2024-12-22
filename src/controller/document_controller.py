from fastapi import HTTPException

from src.domain.stack_ai.database.in_memory_database import InMemoryDatabase
from src.domain.stack_ai.entity.document             import Document
from src.domain.stack_ai.database.functions.search   import naive_knn_search


# @todo define a proper and unified response format across all app, a Response class.
class DocumentController:
    @staticmethod
    async def create_action(payload: dict) -> dict:
        document      = Document(**payload)
        insert_result = await document.create()
        return {
            "result": insert_result,
            "data": document.model_dump()
        }

    @staticmethod
    async def read_action(id: str) -> dict:
        document_data = await InMemoryDatabase().read(
            table_name = Document.table_name,
            conditions = {'id': id}
        )

        document = Document(**document_data)

        return {
            "result": True,
            "data":   document
        }

    @staticmethod
    async def update_action(id: str, document_data: dict) -> dict:
        document      = Document(**document_data)
        update_result = await InMemoryDatabase().update(
            table_name = document.table_name,
            values     = document,
            conditions = {"id": id},
        )

        return {
            "result": update_result,
            "data":   document
        }

    @staticmethod
    async def delete_action(id: str) -> dict:
        delete_result = await InMemoryDatabase().delete(
            table_name = Document.table_name,
            conditions = {"id": id},
        )

        return {
            "result": delete_result,
            "data":   {"id": id}
        }

    @staticmethod
    async def search_chunk_knn_action(id: str, query_vector: list, k: int):
        document = await InMemoryDatabase().read("document", {"id": id})
        if not document:
            raise HTTPException(status_code=404, detail=f"[Error Search] Document with id {id} not found.")

        document_chunks = await InMemoryDatabase().search_by_index(
            table_name = "chunk",
            conditions = {"document_id": id},
        )

        chunks_found = await naive_knn_search(document_chunks, query_vector, k)

        return {
            "result": True,
            "data":   chunks_found
        }