import hashlib


def sha256_hash(data):
    m = hashlib.sha256()
    m.update(data.encode())
    return m.hexdigest()
