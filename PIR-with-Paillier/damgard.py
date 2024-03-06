import math
from typing import List

from Crypto.Random.random import randint
from Crypto.Util.number import getPrime, GCD, inverse


def lcm(x, y):
    return x * (y // GCD(x, y))


def crt(a_list: List[int], n_list: List[int]) -> int:
    """Applies the Chinese Remainder Theorem to find the unique x such that x = a_i (mod n_i) for all i.

    :param a_list: A list of integers a_i in the above equation.
    :param n_list: A list of integers b_i in the above equation.
    :return: The unique integer x such that x = a_i (mod n_i) for all i.
    """

    N = math.prod(n_list)
    y_list = [N // n_i for n_i in n_list]
    z_list = [inverse(y_i, n_i) for y_i, n_i in zip(y_list, n_list)]
    x = sum(a_i * y_i * z_i for a_i, y_i, z_i in zip(a_list, y_list, z_list))

    return x


class DamgardCiphertext:
    def __init__(self, n, g, s, values, ns=None):
        self.n = n
        self.g = g
        self.s = s
        self.ns = n ** s if ns is None else ns
        self.values = values

    def __getitem__(self, key):
        return DamgardCiphertext(self.n, self.g, self.s, [self.values[key]])

    def __add__(self, other):
        if isinstance(other, DamgardCiphertext):
            return self.add_ct(other)
        else:
            return self.add_pt(other)

    def add_pt(self, m):
        pk = DamgardPublicKey(self.n, self.g)
        ct = pk.encrypt([m], self.s)
        return self.add_ct(ct)

    def add_ct(self, ct2):
        """Perform homomorphic addition of two ciphertexts."""
        assert self.s == ct2.s
        nsp1 = self.ns * self.n
        assert isinstance(ct2.values, list), "can't add vector, scalar ciphers"
        assert len(self.values) == len(ct2.values), "can't add ciphers of unequal length"
        values = [Damgard.add_single(self.values[i], ct2.values[i], nsp1) for i in range(len(self.values))]
        return DamgardCiphertext(self.n, self.g, self.s, values, ns=self.ns)

    def __mul__(self, m):
        """Perform homomorphic addition of two ciphertexts."""
        nsp1 = self.ns * self.n
        values = [Damgard.mul_single(self.values[i], m, nsp1) for i in range(len(self.values))]
        return DamgardCiphertext(self.n, self.g, self.s, values, ns=self.ns)


class DamgardSecretKey:
    def __init__(self, n, s, phi):
        self.s = s
        self.n = n
        self.phi = phi
        self.ns = None
        self.d = None
        self.set_s(s)

    def set_s(self, s):
        self.s = s
        self.ns = self.n ** s
        self.d = crt(a_list=[0, 1], n_list=[self.phi, self.ns])

    def decrypt(self, ct):
        """Decrypt ciphertext ct with secret key sk."""
        if ct.s != self.s:
            self.set_s(ct.s)
        return [Damgard.decrypt_single(self, c) for c in ct.values]


class DamgardPublicKey:
    def __init__(self, n, g):
        self.n = n
        self.g = g

    def encrypt(self, m, s=10):
        """Encrypt message m with public key pk."""
        ns = self.n ** s
        nsp1 = ns * self.n
        values = [Damgard.encrypt_single(self.g, x, ns, nsp1) for x in m]
        return DamgardCiphertext(self.n, self.g, s, values, ns=ns)


class Damgard:
    @staticmethod
    def keygen(bits, s=2):
        """Generate Damgard-Jurik key pair."""
        p = getPrime(bits)
        q = getPrime(bits)
        n = p * q
        g = n + 1
        phi = lcm((p - 1), (q - 1))
        return DamgardPublicKey(n, g), DamgardSecretKey(n, s, phi)

    @staticmethod
    def encrypt_single(g, m, ns, nsp1):
        r = randint(1, nsp1)
        while GCD(r, nsp1) != 1:
            r = randint(1, nsp1)
        return (pow(g, m, nsp1) * pow(r, ns, nsp1)) % nsp1

    @staticmethod
    def decrypt_single(sk, ct):
        u = pow(ct, sk.d, sk.ns * sk.n)
        l = Damgard.reduce(u, sk.n, sk.s)
        return l % sk.ns

    @staticmethod
    def reduce(a: int, n: int, s: int) -> int:
        def L(b: int) -> int:
            return (b - 1) // n

        i = 0
        for j in range(1, s + 1):

            t_1 = L(a % (n ** (j + 1)))
            t_2 = i

            for k in range(2, j + 1):
                i = i - 1
                t_2 = t_2 * i % (n ** j)
                t_1 = t_1 - (t_2 * n ** (k - 1) * inverse(math.factorial(k), n ** j)) % n ** j
            i = t_1
        return i

    @staticmethod
    def add_single(c1, c2, nsp1):
        return (c1 * c2) % nsp1

    @staticmethod
    def mul_single(c1, m, nsp1):
        return pow(c1, m, nsp1)


if __name__ == "__main__":
    s = 4
    pk, sk = Damgard.keygen(8, s)
    message1 = [123456789101112, 123]
    message2 = [211101987654321, 321]
    scale = 5
    ciphertext1 = pk.encrypt(message1, s)
    ciphertext2 = pk.encrypt(message2, s)
    ciphertext_sum = ciphertext2 + ciphertext1
    ciphertext_scaling = ciphertext1 * scale
    decrypted_sum = sk.decrypt(ciphertext_sum)
    decrypted_scaling = sk.decrypt(ciphertext_scaling)
    plaintext_sum = [message1[i] + message2[i] for i in range(len(message1))]
    plaintext_scaling = [message1[i] * 5 for i in range(len(message1))]
    print(f"Sum of original messages: {plaintext_sum}, Decrypted sum: {decrypted_sum}")
    print(f"message1 x {scale}: {plaintext_scaling}, Decrypted scaling: {decrypted_scaling}")
