import sys
import numpy as np
from matplotlib import pyplot as plt
import math

def bpail(x,pay): # BasicPIR w Paillier in KB
    log2m = 2048
    req_size = (x * 2 * log2m) / 8192
    resp_size = (2 * log2m * math.ceil(float(pay) * float(8/log2m))) / 8192
    return req_size + resp_size

def blwe(x,pay): # BasicPIR w LWE in KB
    n = 750
    log2q = 64
    lmbda = 128
    log2p = 16
    req_size = (x * (lmbda + log2q)) / 8192
    resp_size = (n * log2q * math.ceil(float(pay) * float(8/log2p))) / 8192
    return req_size + resp_size

def sealpir(x,pay): #SealPIR (d = 2) in KB
    N = 4096
    log2q = 109
    log2p = 20
    lmbda = 128
    crypto_setup = (math.log2(N) * (lmbda + N * log2q)) / 8192
    req_size = (np.ceil(2 * np.sqrt(x)/N)*(lmbda + N * log2q)) / 8192
    resp_size = (2 * N * log2q * np.ceil(log2q/log2p) * np.ceil(pay/(N*log2p))) / 8192
    return crypto_setup + req_size + resp_size

def fastpir(x,pay): #FastPIR (d = 1) in KB
    N = 4096
    log2q = 109
    log2p = 20
    lmbda = 128
    crypto_setup = (math.log2(N) * (lmbda + N * log2q)) / 8192
    req_size = (np.ceil(2 * x / N)*(lmbda + N * log2q)) / 8192
    resp_size = (2 * N * log2q * np.ceil(pay/(N*log2p))) / 8192
    return crypto_setup + req_size + resp_size

def mulpir(x,pay): #MulPIR in KB
    N = 8192
    log2q = 218
    log2p = 20
    lmbda = 128
    crypto_setup = (np.ceil(math.log2(N)) + 1)*(lmbda + N * log2q) / 8192 
    req_size = (np.ceil(2 * np.sqrt(x) / N)*(lmbda + N * log2q)) / 8192
    resp_size = (2 * N * log2q * np.ceil(pay/(N*log2p))) / 8192
    return crypto_setup + req_size + resp_size

def cwpir(x,pay): #Constant-weight PIR (h = 2) in KB
    N = 8192
    log2q = 218
    log2p = 20
    lmbda = 128
    crypto_setup = (np.ceil(math.log2(N)) + 1)*(lmbda + N * log2q) / 8192 
    req_size = (np.ceil(np.sqrt(x) / N)*(lmbda + N * log2q)) / 8192
    resp_size = (2 * N * log2q * np.ceil(pay/(N*log2p))) / 8192
    return crypto_setup + req_size + resp_size

def onionpir(x,pay): #OnionPIR (d = 2) in KB
    N = 4096
    log2q = 128
    log2p = 60
    lmbda = 128
    logB = 31
    ell = np.ceil(log2q / logB)
    crypto_setup = ((math.log2(N) * (lmbda + N * log2q)) + (ell * (lmbda + N * log2q))) / 8192 # to fix ?
    req_size = (np.ceil(2 * np.sqrt(x)/N) * (lmbda + N * log2q)) / 8192
    resp_size = (2 * N * log2q * np.ceil(pay/(N*log2p))) / 8192
    return crypto_setup + req_size + resp_size

def frodopir(x,pay): #FrodoPIR in KB
    n = 1774
    log2q = 32
    log2ro = 10
    lmbda = 128
    w = pay * 8
    omega = np.ceil(w/log2ro)
    setup = (lmbda + n * omega * log2q) / 8192
    req_size = (x * log2q) / 8192
    resp_size = (omega * log2q) / 8192
    return setup + req_size + resp_size


if __name__ == "__main__":
    payload_size = int(sys.argv[1])
    #num_rows = sys.argv[2]
    num_rows = np.linspace(0,100000, 10)
   
    # print(" --- computing communication cost for PIR protocols ----")
    # print(bpail(4096,payload_size)/1024)
    # print(blwe(4096,payload_size)/1024)
    # print(sealpir(4096,payload_size)/1024)
    # print(fastpir(4096,payload_size)/1024)
    # print(mulpir(4096,payload_size)/1024)
    # print(cwpir(4096,payload_size)/1024)
    # print(onionpir(4096,payload_size)/1024)
    # print(frodopir(4096,payload_size)/1024)

    plt.plot(num_rows, bpail(num_rows, payload_size)/1024, color='red', label='BasicPIR w Paillier')
    plt.plot(num_rows, blwe(num_rows, payload_size)/1024, color='orange', label='BasicPIR w LWE')
    plt.plot(num_rows, sealpir(num_rows, payload_size)/1024, color='yellow', label='SealPIR')
    plt.plot(num_rows, fastpir(num_rows, payload_size)/1024, color='green', label='FastPIR')
    plt.plot(num_rows, mulpir(num_rows, payload_size)/1024, color='blue', label='MulPIR')
    plt.plot(num_rows, cwpir(num_rows, payload_size)/1024, color='indigo', label='Constant weight PIR')
    plt.plot(num_rows, onionpir(num_rows, payload_size)/1024, color='violet', label='OnionPIR')
    plt.plot(num_rows, frodopir(num_rows, payload_size)/1024, color='black', label='FrodoPIR')
    plt.legend()
    plt.xlabel("Number of Rows")
    plt.ylabel("Communication Cost (MB)")
    plt.show()