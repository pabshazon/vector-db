class HashTableIndexer:
    def __init__(self, size = 100):
        self.size       = size
        self.hash_slots = []
        for slot_index in range(size):
            empty_collision_chain = []
            self.hash_slots.append(empty_collision_chain)

    def insert(self, key, value):
        if self._key_already_exists(key):
            self._update_existing_key(key, value)
        else:
            self._add_new_key(key, value)

    def read(self, key):
        index = self._calculate_slot_index(key)

        for existing_key, value in self.hash_slots[index]:
            if existing_key == key:
                return value
        return None

    def update(self, key, new_value):  # @todo TBD if we need this public one, or if we use always insert which handles updates. looks redundant
        if self._key_already_exists(key):
            self._update_existing_key(key, new_value)

    def _calculate_slot_index(self, key) -> int:
        return hash(key) % self.size

    def _key_already_exists(self, key) -> bool:
        index           = self._calculate_slot_index(key)
        collision_chain = self.hash_slots[index]

        for entry in collision_chain:
            key_from_entry = entry[0]
            if key_from_entry == key:
                return True
        return False

    def _update_existing_key(self, key, new_value):
        index = self._calculate_slot_index(key)

        for entry_position, (existing_key, _) in enumerate(self.hash_slots[index]):
            if existing_key == key:
                self.hash_slots[index][entry_position] = (key, new_value)
                break

    def _add_new_key(self, key, value):
        index = self._calculate_slot_index(key)
        self.hash_slots[index].append((key, value))
