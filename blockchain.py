from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import List


@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: float  # 'datetime.now().timestamp()'
    block_data: str
    current_hash: str


class BlockChain:

    def __init__(self) -> None:
        self.block_chain = [self.get_genesis_block()]

    @staticmethod
    def get_genesis_block() -> Block:
        return Block(0, '0', 1642346961.018641, 'Genesis block',
                     '704242bb7fe5c275c19085eb8a139e7631ab444388dc9d01d5066f4cfa53a85b')

    @staticmethod
    def calculate_hash(index: int, previous_hash: str, timestamp: float, block_data: str) -> str:
        data = str(index) + previous_hash + str(timestamp) + block_data
        return sha256(data.encode('utf-8')).hexdigest()

    def get_last_block(self) -> Block:
        return self.block_chain[-1]

    def generate_next_block(self, block_data: str) -> Block:
        prev_block: Block = self.get_last_block()
        next_index = prev_block.index + 1
        next_timestamp = datetime.now().timestamp()
        next_hash = self.calculate_hash(index=next_index, previous_hash=prev_block.current_hash, block_data=block_data)
        return Block(index=next_index,
                     previous_hash=prev_block.current_hash,
                     timestamp=next_timestamp,
                     block_data=block_data,
                     current_hash=next_hash)

    def calculate_hash_for_block(self, block: Block) -> str:
        return self.calculate_hash(index=block.index,
                                   previous_hash=block.previous_hash,
                                   timestamp=block.timestamp,
                                   block_data=block.block_data)

    def is_new_block_valid(self, prev_block: Block, new_block: Block) -> bool:
        if prev_block.index + 1 != new_block.index:
            return False
        elif prev_block.current_hash != new_block.previous_hash:
            return False
        elif self.calculate_hash_for_block(new_block) != new_block.current_hash:
            return False
        return True

    def is_chain_valid(self, chain_to_validate: List[Block]) -> bool:
        if chain_to_validate[0] != self.block_chain[0]:
            return False
        temporary_blocks = [chain_to_validate[0]]
        for block in chain_to_validate:
            if self.is_new_block_valid(temporary_blocks[-1], block):
                temporary_blocks.append(block)
            else:
                return False
        return True

    def replace_chain(self, new_blocks: List[Block]):
        if len(new_blocks) > len(self.block_chain) and self.is_chain_valid(new_blocks):
            self.block_chain = new_blocks
