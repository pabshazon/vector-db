from fastapi import HTTPException  # @todo handle all exceptions not just search

from src.domain.stack_ai.database.functions.search   import naive_knn_search
from src.domain.stack_ai.database.in_memory_database import InMemoryDatabase
from src.domain.stack_ai.entity.chunk                import Chunk
from src.domain.stack_ai.entity.library              import Library


# @todo define a proper and unified response format across all app, a Response class.
class LibraryController:
    @staticmethod
    async def create_action(payload: dict) -> dict:
        library       = Library(**payload)
        insert_result = await library.create()
        return {
            "result": insert_result,
            "data":   library
        }

    @staticmethod
    async def read_action(id: str) -> dict:
        library_data = await InMemoryDatabase().read(
            table_name = Library.get_table_name(),
            conditions = {'id': id}
        )

        library = Library(**library_data)
        return {
            "result": True if library_data else None,
            "data":   library
        }

    @staticmethod
    async def update_action(id: str, library_data: dict):
        library       = Library(**library_data)
        update_result = await InMemoryDatabase().update(
            table_name = library.get_table_name(),
            values     = library,
            conditions = {"id": id},
        )

        return {
            "result": update_result,
            "data":   library
        }

    @staticmethod
    async def delete_action(id: str):
        delete_result = await InMemoryDatabase().delete(
            table_name = Library.get_table_name(),
            conditions = {"id": id},
        )

        return {
            "result": delete_result,
            "data":   {"id": id}
        }

    @staticmethod
    async def search_chunk_knn_action(id: str, query_vector: list, k: int):
        library = await InMemoryDatabase().read("library", {"id": id})
        if not library:
            raise HTTPException(status_code=404, detail=f"[Error Search] Library with id {id} not found.")

        library_chunks = await InMemoryDatabase().search_by_index(
            table_name = Chunk.get_table_name(),
            conditions = {"library_id": id},
        )

        chunks_found = await naive_knn_search(library_chunks, query_vector, k)

        return {
            "result": True,
            "data":   chunks_found
        }
