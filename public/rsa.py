import random


def extract_prime_power(a, p):
    s = 0
    if p > 2:
        while a and a % p == 0:
            s += 1
            a //= p
    elif p == 2:
        while a and a & 1 == 0:
            s += 1
            a >>= 1
    return s, a


def gcd(a, b):
    if a == 0: return b
    if b == 0: return a
    while b:
        a, b = b, a % b
    return abs(a)


def fast_pow(a, b, c):
    output = 1
    t = a % c
    while b != 0:
        if b & 1:
            output = (output * t) % c
        b >>= 1
        t = (t * t) % c
    return output


def prime_test_miller_rabin(p, k=25):
    if p < 2: return False
    if p == 3: return True
    if p & 1 == 0: return False

    # p - 1 = 2**s * m
    s, m = extract_prime_power(p - 1, 2)

    for j in range(k):
        a = random.randint(2, p - 2)
        if gcd(a, p) != 1:
            return False

        b = pow(a, m, p)
        if b in (1, p - 1):
            continue

        for i in range(s):
            b = pow(b, 2, p)

            if b == 1:
                return False

            if b == p - 1:
                if i < s - 1: break  # good
                else: return False  # bad
        else:
            # result is not 1
            return False
    return True


def randint_bits(size):
    low = 1 << (size - 1)
    hi = (1 << size) - 1
    return random.randint(low, hi)


def gen_prime(size):
    while True:
        n = randint_bits(size) | 1
        if gcd(1, n) != 1:
            continue
        if prime_test_miller_rabin(n, 25):
            return n


def mod_inverse(a, b):
    n = b
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u % n


def get_rsa_key():
    p = gen_prime(1024)
    q = gen_prime(1024)
    assert p != q
    n = p * q
    phi = (p - 1) * (q - 1)
    d = mod_inverse(65537, phi)
    return 65537, d, n


def encrypt(msg, e, n):
    return fast_pow(int(msg.encode('hex'), 16), e, n)


def decrypt(msg, d, n):
    tmp = fast_pow(msg, d, n)
    tmp = hex(tmp)[2:].rstrip('L')
    if len(tmp) % 2 != 0:
        tmp = '0' + tmp

    return tmp.decode('hex')


if __name__ == '__main__':
    import sys

    e, d, n = get_rsa_key()
    print('E: ', e)
    print('D: ', d)
    print('N: ', n)
    msg = sys.argv[1]

    cipher = encrypt(msg, e, n)
    print('CIPHER: ', cipher)
    print(decrypt(cipher, d, n))
