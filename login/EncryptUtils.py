import hashlib

class EncryptUtils:
    @staticmethod
    def md5_encrypt(string):
        if not string:
            raise Exception("null value")
        md5_hash = hashlib.md5()
        md5_hash.update(string.encode('utf-8'))
        return md5_hash.hexdigest()
