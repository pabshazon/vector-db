from fastapi import FastAPI, HTTPException

from src.controller.chunk_controller     import ChunkController
from src.controller.document_controller  import DocumentController
from src.controller.library_controller   import LibraryController
from src.domain.stack_ai.entity.library  import Library
from src.domain.stack_ai.entity.document import Document
from src.domain.stack_ai.entity.chunk    import Chunk


app = FastAPI()

library_controller  = LibraryController()
document_controller = DocumentController()
chunk_controller    = ChunkController()

######### library

@app.post("/library/")
async def create_library_endpoint(payload: Library):
    return await library_controller.create_action(payload)

@app.get("/library/{id}")
async def get_library_endpoint(id: str):
    return library_controller.read_action(id)

@app.put("/library/{id}")
async def update_library_endpoint(id: str, payload: Library):
    return library_controller.update_action(id)

@app.delete("/library/{id}")
async def delete_library_endpoint(id: str):
    return library_controller.delete_action(id)

######### document

@app.post("/document/")
async def create_document_endpoint(payload: Document):
    return document_controller.create_action(id)

@app.get("/document/{id}")
async def get_document_endpoint(id: str):
    return document_controller.read_action(id)

@app.put("/document/{id}")
async def update_document_endpoint(id: str, payload: Document):
    return document_controller.update_action(id)

@app.delete("/document/{id}")
async def delete_document_endpoint(id: str):
    return document_controller.delete_action(id)

######### chunk

@app.post("/chunk/")
async def create_chunk_endpoint(payload: Chunk):
    return chunk_controller.create_action(id)

@app.get("/chunk/{id}")
async def get_chunk_endpoint(id: str):
    return chunk_controller.read_action(id)

@app.put("/chunk/{id}")
async def update_chunk_endpoint(id: str, payload: Chunk):
    return chunk_controller.update_action(id)

@app.delete("/chunk/{id}")
async def delete_chunk_endpoint(id: str):
    return chunk_controller.delete_action(id)

######### search

@app.post("/library/chunk_search_knn/{library_id}")
async def search_library_knn_endpoint(library_id: str, query_vector: list, k: int = 5):
    if not library_id.strip():
        raise HTTPException(status_code=400, detail="[Argument Error] library_id cannot be empty.")
    if not query_vector:
        raise HTTPException(status_code=400, detail="[Argument Error] query_vector cannot be empty.")
    if k <= 0:
        raise HTTPException(status_code=400, detail="[Argument Error] k must be a positive integer.")
    return library_controller.search_chunk_knn_action(library_id, query_vector, k)

@app.post("/document/chunk_search_knn/{document_id}")
async def search_library_knn_endpoint(document_id: str, query_vector: list, k: int = 5):
    if not document_id.strip():
        raise HTTPException(status_code=400, detail="[Argument Error] document_id cannot be empty.")
    if not query_vector:
        raise HTTPException(status_code=400, detail="[Argument Error] query_vector cannot be empty.")
    if k <= 0:
        raise HTTPException(status_code=400, detail="[Argument Error] k must be a positive integer.")

    return document_controller.search_chunk_knn_action(document_id, query_vector, k)

@app.post("/chunk/search_all_chunks_knn/{chunk_id}")
async def search_library_knn_endpoint(chunk_id: str, query_vector: list, k: int = 5):
    if not chunk_id.strip():
        raise HTTPException(status_code=400, detail="[Argument Error] chunk_id cannot be empty.")
    if not query_vector:
        raise HTTPException(status_code=400, detail="[Argument Error] query_vector cannot be empty.")
    if k <= 0:
        raise HTTPException(status_code=400, detail="[Argument Error] k must be a positive integer.")

    return chunk_controller.search_all_chunks_knn_action(chunk_id, query_vector, k)

