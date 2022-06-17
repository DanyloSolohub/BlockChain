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
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.block_chain = [self.get_genesis_block()]

    @staticmethod
    def get_genesis_block() -> Block:
        return Block(0, '0', 1642346961.018641, 'Genesis block',
                     '704242bb7fe5c275c19085eb8a139e7631ab444388dc9d01d5066f4cfa53a85b')

    @staticmethod
    def calculate_hash(
            index: int,
            previous_hash: str,
            timestamp: float,
            block_data: str
    ) -> str:
        data = str(index) + previous_hash + str(timestamp) + block_data
        return sha256(data.encode('utf-8')).hexdigest()

    def get_last_block(self) -> Block:
        return self.block_chain[-1]

    def generate_next_block(
            self,
            block_data: str
    ) -> Block:
        """

        :param block_data:
        :return:
        """
        prev_block: Block = self.get_last_block()
        next_index: int = prev_block.index + 1
        next_timestamp = datetime.now().timestamp()
        next_hash = self.calculate_hash(
            index=next_index,
            previous_hash=prev_block.current_hash,
            block_data=block_data
        )
        return Block(
            index=next_index,
            previous_hash=prev_block.current_hash,
            timestamp=next_timestamp,
            block_data=block_data,
            current_hash=next_hash
        )

    def calculate_hash_for_block(
            self,
            block: Block
    ) -> str:
        """
        Calculates a hash for the block
        :param block: Block
        :return: calculated hash
        """
        return self.calculate_hash(
            index=block.index,
            previous_hash=block.previous_hash,
            timestamp=block.timestamp,
            block_data=block.block_data
        )

    def is_new_block_valid(
            self,
            prev_block: Block,
            new_block: Block
    ) -> bool:
        """
        Verify new block compared with previous
        :param prev_block: previous Block
        :param new_block: new Block
        :return: True if new block is valid, False if not
        """
        if prev_block.index + 1 != new_block.index:
            return False
        elif prev_block.current_hash != new_block.previous_hash:
            return False
        elif self.calculate_hash_for_block(new_block) != new_block.current_hash:
            return False
        return True

    def is_chain_valid(
            self,
            chain_to_validate: List[Block]
    ) -> bool:
        """
        Verify chain of blocks
        :param chain_to_validate: chain which should be verified
        :return: True if chain is valid, False if not
        """
        if chain_to_validate[0] != self.block_chain[0]:
            return False
        temporary_blocks = [chain_to_validate[0]]
        for block in chain_to_validate:
            if self.is_new_block_valid(temporary_blocks[-1], block):
                temporary_blocks.append(block)
            else:
                return False
        return True

    def replace_chain(
            self,
            new_blocks: List[Block]
    ) -> bool:
        """
        Replace chain if new chain is valid and they not same
        :param new_blocks: chain which could become new chain
        :return: True if chain has been replaced
        """
        if len(new_blocks) > len(self.block_chain) and self.is_chain_valid(new_blocks):
            self.block_chain = new_blocks
            return True
        return False
# https://dev.to/freakcdev297/creating-a-blockchain-in-60-lines-of-javascript-5fka