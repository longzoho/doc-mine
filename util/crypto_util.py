import os
import hashlib


def hash_content(data: bytes):
    secret_str = os.getenv('HASH_SECRET') or '2d816e36ff0797739370b5192a00084d'
    # convert hex string to bytes
    secret = bytes.fromhex(secret_str)
    # hash data
    _hash = hashlib.sha256()
    _hash.update(secret)
    _hash.update(data)
    _hash.digest()
    return _hash.hexdigest()
