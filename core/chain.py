from datetime import datetime
from typing import List
from urllib.parse import urlparse

from core.block import Block
from core.transaction import Transaction


class BlockChain:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.chain = [self.genesis_block]
        self.transactions = []
        self.nodes = set()
        self.__difficult = 1
        self.__reward = 1000

    @property
    def genesis_block(self) -> Block:
        """
        :return: first "Genesis" block
        """
        return Block(
            height=0,
            difficulty=self.difficult,
            previous_hash=None,
            transactions=[],
            mapping=None,
            miner=None,
            timestamp=1642346961.018641,
        )

    @property
    def difficult(self):
        chain_len = len(self.chain)
        sum_part = (chain_len // 10000)
        return self.__difficult + sum_part

    @property
    def reward(self):
        chain_len = len(self.chain)
        division_part = (chain_len // 10000) + 1
        return self.__reward // division_part

    @property
    def last_block(self) -> Block:
        """
        :return: last block of the core
        """
        return self.chain[-1]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                elif transaction.recipient == address:
                    balance += transaction.amount
        return balance

    def generate_next_block(
            self,
    ) -> Block:
        """
        Generates the next block
        :return: block
        """
        prev_block: Block = self.last_block
        next_height: int = prev_block.height + 1
        next_timestamp = datetime.now().timestamp()
        return Block(
            height=next_height,
            previous_hash=prev_block.current_hash,
            timestamp=next_timestamp,
        )

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    @staticmethod
    def calculate_hash_for_block(
            block: Block
    ) -> str:
        """
        Calculates a hash for the block
        :param block: Block
        :return: calculated hash
        """
        return Block.calculate_hash(
            nonce=block.nonce,
            height=block.height,
            previous_hash=block.previous_hash,
            timestamp=block.timestamp,
        )

    def is_new_block_valid(
            self,
            prev_block: Block,
            new_block: Block
    ) -> bool:
        """
        Verify new block, compare with previous
        :param prev_block: previous Block
        :param new_block: new Block
        :return: True if new block is valid, False if not
        """
        if prev_block.height + 1 != new_block.height:
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
        if chain_to_validate[0] != self.chain[0]:
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
        if len(new_blocks) > len(self.chain) and self.is_chain_valid(new_blocks):
            self.chain = new_blocks
            return True
        return False

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
