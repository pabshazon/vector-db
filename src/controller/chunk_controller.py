from fastapi import HTTPException

from src.domain.stack_ai.entity.chunk                import Chunk
from src.domain.stack_ai.database.in_memory_database import InMemoryDatabase
from src.domain.stack_ai.database.functions.search   import naive_knn_search


# @todo define a proper and unified response format across all app, a Response class.
class ChunkController:
    @staticmethod
    async def create_action(payload: dict) -> dict:
        chunk         = Chunk(**payload)
        insert_result = await chunk.create()
        return {
            "result": insert_result,
            "data": chunk.dict()
        }

    @staticmethod
    async def read_action(id: str) -> dict:
        chunk_data = await InMemoryDatabase().read(
            table_name = Chunk.table_name,
            conditions = {'id': id}
        )

        chunk = Chunk(**chunk_data)
        return {
            "result": True if chunk_data else None,
            "data":   chunk
        }

    @staticmethod
    async def update_action(id: str, chunk_data: dict) -> dict:
        chunk       = Chunk(**chunk_data)
        update_result = await InMemoryDatabase().update(
            table_name = chunk.table_name,
            values     = chunk,
            conditions = {"id": id},
        )

        return {
            "result": update_result,
            "data":   chunk
        }

    @staticmethod
    async def delete_action(id: str) -> dict:
        delete_result = await InMemoryDatabase().delete(
            table_name = Chunk.table_name,
            conditions = {"id": id},
        )

        return {
            "result": delete_result,
            "data":   {"id": id}
        }

    @staticmethod
    async def search_all_chunks_knn_action(id: str, query_vector: list, k: int):
        chunk_record = await InMemoryDatabase().read("chunk", {"id": id})
        if not chunk_record:
            raise HTTPException(status_code=404, detail=f"[Error] Chunk with id {id} not found.")

        all_chunks   = await InMemoryDatabase().read(Chunk.get_table_name(), {'id': '*'})
        chunks_found = naive_knn_search(all_chunks, query_vector, k)

        return {
            "result": True,
            "data":   chunks_found
        }
