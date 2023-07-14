from paillier import *
import time

if __name__=='__main__':

    # Measure keygen time
    start = time.time()
    pk, sk = Paillier.keygen(1024)
    end = time.time()
    print(f"Keygen time: {end - start}")

    # Measure encryption time
    start = time.time()
    messages = [(1 if i==14 else 0) for i in range(256)]
    ciphertexts = [pk.encrypt([messages[i]]) for i in range(256)]
    end = time.time()
    print(f"Encryption time: {end - start}")
    
    database = [i for i in range(256)]

    # Measure decryption time
    start = time.time()
    ciphertext_sum = pk.encrypt([0])
    for i in range(256):
        ciphertext_sum = ciphertext_sum + (ciphertexts[i] * database[i])
    end = time.time()
    print(f"Computation time: {end - start}")

    decrypted_sum = sk.decrypt(ciphertext_sum)
    # plaintext_sum = [message1[i] + message2[i] for i in range(len(message1))]
    print(f"Decrypted sum: {decrypted_sum}")
