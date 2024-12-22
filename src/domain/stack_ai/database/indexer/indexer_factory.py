from .hash_table_indexer import HashTableIndexer
from .binary_search_tree import BinarySearchTree

allowed_indexes = ["hash", "binary_search_tree"]


class IndexerFactory:
    @staticmethod
    def make(index_type: str, options: dict = None):
        if index_type not in allowed_indexes:
            raise Exception(f"Unknown index type '{index_type}'. Use allowed values '{allowed_indexes}'.")

        if index_type == "binary_search_tree":
            return BinarySearchTree()

        elif index_type == "hash":
            if not options or not options.get("size"):
                options["size"] = None
            return HashTableIndexer(options["size"])

        else:
            raise Exception(f"Unknown index type '{index_type}'. Use allowed values '{allowed_indexes}'.")
