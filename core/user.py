from Crypto.PublicKey import RSA
from dataclasses import dataclass, field
from hashlib import sha512
from Crypto.PublicKey.RSA import RsaKey

from main import KEY_SIZE
import base64


@dataclass
class User:
    private_key: RsaKey = field(init=False)

    def __post_init__(self):
        self.private_key = RSA.generate(KEY_SIZE)

    @property
    def address(self) -> str:
        public_key = self.private_key.publickey()
        encoded_key = base64.b64encode(public_key.export_key())
        return encoded_key.decode('utf-8')

    def sign(self, message_to_sign: str) -> str:
        hash_ = int.from_bytes(sha512(message_to_sign.encode('utf-8')).digest(), byteorder='big')
        signature = pow(hash_, self.private_key.d, self.private_key.n)
        return hex(signature)

    def verify_signature(self, message_to_verify: str, signature: str) -> bool:
        hash_ = int.from_bytes(sha512(message_to_verify.encode('utf-8')).digest(), byteorder='big')
        hash_from_signature = pow(int(signature, 16), self.private_key.e, self.private_key.n)
        return hash_ == hash_from_signature
