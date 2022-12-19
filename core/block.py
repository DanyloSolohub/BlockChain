from dataclasses import dataclass, field
from hashlib import sha256
from typing import List, Dict

from core.transaction import Transaction


@dataclass
class Block:
    height: int
    nonce: int = field(init=False, default=0)
    difficulty: int
    current_hash: str = field(init=False)
    previous_hash: str
    transactions: List[Transaction]
    mapping: Dict[str, str]
    miner: str
    signature: str
    timestamp: float  # 'datetime.now().timestamp()'

    def __post_init__(self):
        self.current_hash = self.calculate_hash(
            height=self.height,
            nonce=self.nonce,
            previous_hash=self.previous_hash,
            timestamp=self.timestamp,
        )

    def mine_block(self):
        while self.current_hash[:self.difficulty] != ''.zfill(self.difficulty):
            self.nonce += 1
            self.current_hash = self.calculate_hash(
                height=self.height,
                nonce=self.nonce,
                previous_hash=self.previous_hash,
                timestamp=self.timestamp,
            )

    @staticmethod
    def calculate_hash(
            nonce: int,
            height: int,
            previous_hash: str,
            timestamp: float,
    ) -> str:
        """
        calculates a hash
        :param nonce: number needed to calculate hash
        :param height: block height
        :param previous_hash: hash of previous block
        :param timestamp: timestamp
        :return: hash
        """

        data = str(nonce) + str(height) + previous_hash + str(timestamp)
        return sha256(data.encode('utf-8')).hexdigest()
