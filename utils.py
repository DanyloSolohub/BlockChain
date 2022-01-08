from hashlib import sha256


def calculate_hash(self):
    data = f'{self.block_index} {self.previous_hash} {self.timestamp} {self.block_data}'
    return sha256(data.encode('utf-8')).hexdigest()
