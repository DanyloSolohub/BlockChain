from dataclasses import dataclass, field
from hashlib import sha256
from typing import List

from core.transaction import Transaction


@dataclass
class Block:
    nonce: int = field(init=False, default=0)
    difficulty: int
    current_hash: str = field(init=False)
    previous_hash: str
    transactions: List[Transaction]
    mapping: dict
    miner: str
    signature: str
    timestamp: float  # 'datetime.now().timestamp()'

    def __post_init__(self):
        self.current_hash = self.calculate_hash(
            nonce=self.nonce,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
        )

    def mine_block(self, difficult):
        while self.current_hash[:difficult] != ''.zfill(difficult):
            self.nonce += 1
            self.current_hash = self.calculate_hash(
                nonce=self.nonce,
                previous_hash=self.previous_hash,
                timestamp=self.timestamp,
            )

    @staticmethod
    def calculate_hash(
            nonce: int,
            index: int,
            previous_hash: str,
            timestamp: float,
    ) -> str:
        """
        calculates a hash
        :param nonce: number needed to calculate hash
        :param index: block index
        :param previous_hash: hash of previous block
        :param timestamp: timestamp
        :return: hash
        """
        data = str(nonce) + str(index) + previous_hash + str(timestamp)
        return sha256(data.encode('utf-8')).hexdigest()
