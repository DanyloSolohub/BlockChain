from Crypto.PublicKey import RSA
from dataclasses import dataclass, field

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
