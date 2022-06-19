from datetime import datetime
from typing import List
from core.block import Block
from urllib.parse import urlparse
from core.transaction import Transaction


class BlockChain:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.chain = [self.get_genesis_block()]
        self.pending_transactions = []
        self.nodes = set()
        self.__difficult = 1
        self.__reward = 1000

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

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                elif transaction.recipient == address:
                    balance += transaction.amount
        return balance

    @staticmethod
    def get_genesis_block() -> Block:
        """
        :return: first "Genesis" block
        """
        return Block(0, '0', 1642346961.018641, 'Genesis block')

    def get_last_block(self) -> Block:
        """
        :return: last block of the core
        """
        return self.chain[-1]

    def generate_next_block(
            self,
            block_data: str
    ) -> Block:
        """
        Generates the next block
        :param block_data: some data which must contains in block
        :return: block
        """
        prev_block: Block = self.get_last_block()
        next_index: int = prev_block.index + 1
        next_timestamp = datetime.now().timestamp()
        return Block(
            index=next_index,
            previous_hash=prev_block.current_hash,
            timestamp=next_timestamp,
            block_data=block_data,
        )

    def mine_pending_transactions(self, miner_address):
        pass

    def create_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

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
        Verify new block, compare with previous
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
