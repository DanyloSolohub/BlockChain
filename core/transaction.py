from dataclasses import dataclass


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
