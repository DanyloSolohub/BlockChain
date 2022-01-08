class Block:
    def __init__(self, block_index, previous_hash, timestamp, block_data, current_hash):
        self.block_index = block_index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.block_data = block_data
        self.current_hash = current_hash
