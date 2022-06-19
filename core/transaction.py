from dataclasses import dataclass


@dataclass
class Transaction:
    random_bytes: bytes
    previous_block: str
    sender: str
    recipient: str
    amount: float
    to_storage: float
    current_hash: str
    signature: str
