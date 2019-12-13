import sys

fname = sys.argv[1]
cipher = open(fname).read()

rate = {
    'A': 0.082,
    'B': 0.015,
    'C': 0.028,
    'D': 0.043,
    'E': 0.127,
    'F': 0.022,
    'G': 0.020,
    'H': 0.061,
    'I': 0.070,
    'J': 0.002,
    'K': 0.008,
    'L': 0.040,
    'M': 0.024,
    'N': 0.067,
    'O': 0.075,
    'P': 0.019,
    'Q': 0.001,
    'R': 0.060,
    'S': 0.063,
    'T': 0.091,
    'U': 0.028,
    'V': 0.010,
    'W': 0.023,
    'X': 0.001,
    'Y': 0.020,
    'Z': 0.001,
}

def group(c, length):
    res = [[] for _ in range(length)]
    for i in range(len(c)):
        res[i % length].append(c[i].upper())

    return res


def calc_CI(c, length):
    res = []
    for cipher_t in group(c, length):
        tmp = 0.0
        for alpha in rate.keys():
            alpha_c = cipher_t.count(alpha)
            tmp += alpha_c * (alpha_c - 1)

        res.append(tmp / (len(cipher_t) * (len(cipher_t) - 1)))
    return sum(res) / len(res)


CIs = []
for i in range(1, 64):
    CIs.append((i, calc_CI(cipher, i)))

CIs.sort(key=lambda x: abs(x[1] - 0.065))
k_len = [x[0] for x in CIs]

for length in k_len:
    output = []
    for cipher_t in group(cipher, length):
        t = {ord(a): cipher_t.count(a) for a in rate.keys()}

        res = {}
        for offset in range(26):
            tmp = 0
            for a in t.keys():
                tmp += t[a] * rate[chr((
                    (a - 65 + offset) % 26) + 65)]
                res[offset] = tmp
                
        res = sorted(res.items(), key=lambda x: abs(x[1] - 0.065))
        output.append(chr((21 - res[0][0]) % 26 + ord('A')))
        key = ''.join(output)

    print(f'KEY_LENGTH={length} -> {key}')
