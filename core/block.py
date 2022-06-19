from typing import List
from dataclasses import dataclass, field
from hashlib import sha256

from core.transaction import Transaction


@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: float  # 'datetime.now().timestamp()'
    block_data: str
    transactions: List[Transaction] = None
    nonce: int = field(init=False, default=0)
    current_hash: str = field(init=False)

    def __post_init__(self):
        self.current_hash = self.calculate_hash(
            nonce=self.nonce,
            index=self.index,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
            block_data=self.block_data
        )

    def mine_block(self, difficult):
        while self.current_hash[:difficult] != ''.zfill(difficult):
            self.nonce += 1
            self.current_hash = self.calculate_hash(
                nonce=self.nonce,
                index=self.index,
                previous_hash=self.previous_hash,
                timestamp=self.timestamp,
                block_data=self.block_data
            )

    @staticmethod
    def calculate_hash(
            nonce: int,
            index: int,
            previous_hash: str,
            timestamp: float,
            block_data: str
    ) -> str:
        """
        calculates a hash
        :param nonce: number needed to calculate hash
        :param index: block index
        :param previous_hash: hash of previous block
        :param timestamp: timestamp
        :param block_data: some data which must contains in block
        :return: hash
        """
        data = str(nonce) + str(index) + previous_hash + str(timestamp) + block_data
        return sha256(data.encode('utf-8')).hexdigest()
