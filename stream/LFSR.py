def lfsr(key, mask):
    while 1:
        output = (key << 1) & 0xFFFFFFFF
        tmp = (key & mask) & 0xFFFFFFFF
        lastbit = 0
        while tmp != 0:
            lastbit ^= tmp & 1
            tmp >>= 1
        output ^= lastbit
        key = output
        yield output


mask = 0b10100100000010000000100010010100
k = 0x876FDA
gen = lfsr(k, mask)

for i in gen:
    init = i
    break

c = 1
for i in gen:
    if i == init:
        break
    c += 1

print(c)
