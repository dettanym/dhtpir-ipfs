from damgard import *


class PaillierCiphertext(DamgardCiphertext):
    def __init__(self, n, g, values):
        super().__init__(n, g, 1, values)


class PaillierSecretKey(DamgardSecretKey):
    def __init__(self, n, phi):
        super().__init__(n, 1, phi)


class PaillierPublicKey(DamgardPublicKey):
    def __init__(self, n, g):
        super().__init__(n, g)

    def encrypt(self, m, s=1):
        # encryption enforced with s=1
        return super().encrypt(m, s=1)


class Paillier:
    @staticmethod
    def keygen(bits):
        """Generate Damgard-Jurik key pair."""
        p = getPrime(bits)
        q = getPrime(bits)
        n = p * q
        g = n + 1
        phi = (p - 1) * (q - 1)
        return PaillierPublicKey(n, g), PaillierSecretKey(n, phi)


if __name__ == "__main__":
    pk, sk = Paillier.keygen(128)
    messages = [123456789101112, 123]
    message2 = [211101987654321, 321]
    ciphertext1 = pk.encrypt(messages)
    ciphertext2 = pk.encrypt(message2)
    ciphertext_sum = ciphertext2 + ciphertext1
    decrypted_sum = sk.decrypt(ciphertext_sum)
    plaintext_sum = [messages[i] + message2[i] for i in range(len(messages))]
    print(f"Sum of original messages: {plaintext_sum}, Decrypted sum: {decrypted_sum}")
