import asyncio
from fastapi.encoders import jsonable_encoder


class InMemoryDatabase:
    _instance          = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized   = True
            self.data          = {}
            self.indexed_data  = {}
            self.table_config  = {}
            self.table_indexer = {}
            self._lock         = asyncio.Lock()

    def register_table(self, table_name: str, table_config: dict):
        self.table_config[table_name]  = table_config
        self.table_indexer[table_name] = table_config["indexer"]

    async def insert(self, table_name: str, values):  # @todo data type the values.
        async with self._lock:
            if table_name not in self.data:
                self.data[table_name] = {}

            key                        = str(values['id'])
            self.data[table_name][key] = jsonable_encoder(values)

            indexer = self.table_indexer.get(table_name, False)
            if indexer:
                config              = self.table_config[table_name]
                index_keys          = config["index_keys"]
                attributes_to_index = {}
                for index_key in index_keys:
                    if index_key in values:
                        attributes_to_index[index_key] = values[index_key]
                indexer.insert(key, attributes_to_index)  # @todo rethink if this level of polymorphism is adecuate or we are breaking too much the compile time typing - we could add an intermediate method to ensure the type returned

            return True

    async def read(self, table_name: str, conditions):
        async with self._lock:
            if table_name not in self.data or 'id' not in conditions:
                return None  # @todo TBD raising error/warning fail-first approach?
            key  = str(conditions['id'])
            if key == '*':
                return self.data[table_name]
            data = self.data[table_name].get(key)
            return data

    async def update(self, table_name: str, values: dict, conditions: dict):
        async with self._lock:
            if table_name not in self.data or 'id' not in conditions:
                return None  # @todo think if raise error/warning

            key = str(conditions['id'])
            if key in self.data[table_name]:
                updated_values             = {**self.data[table_name][key], **values}
                self.data[table_name][key] = jsonable_encoder(updated_values)

            indexer = self.table_indexer.get(table_name, False)
            if indexer:
                config     = self.table_config[table_name]
                index_keys = config["index_keys"]
                attributes_to_index = {}
                for index_key in index_keys:
                    if index_key in values:
                        attributes_to_index[index_key] = values[index_key]
                indexer.update(key, attributes_to_index)  # @todo rethink if this level of polymorphism is adecuate or we are breaking too much the strong typing we want - we could add an intermediate method to ensure the type returned
            return True

    async def delete(self, table_name: str, conditions):  # @todo data type the conditions.
        async with self._lock:
            if table_name not in self.data or 'id' not in conditions:
                return None  # @todo think if raise error/warning

            key = str(conditions['id'])
            if key in self.data[table_name]:
                del self.data[table_name][key]
                indexer = self.table_indexer.get(table_name, False)
                if indexer:
                    indexer.update(key, None)  # @todo rethink if this level of polymorphism is adecuate or we are breaking too much the strong typing we want - we could add an intermediate method to ensure the type returned
                return True
            return None

    async def _id_already_exists(self, table_name, row):
        if await self.read(table_name=table_name, conditions={"id": row.id}):
            return True
        return False

    async def search_by_index(self, table_name: str, conditions: dict):
        async with self._lock:
            if table_name not in self.table_indexer:
                return None

            indexer      = self.table_indexer[table_name]
            matched_keys = await indexer.read(conditions)
            matched_rows = {}

            for key in matched_keys:
                row_data = self.data[table_name].get(key)
                if row_data:
                    matched_rows[key] = row_data
            return matched_rows
