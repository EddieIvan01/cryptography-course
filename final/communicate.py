import rsa
import os
import socket
import sys

END = '||||\n'


def recv_until(s, token=END):
    buffer = []
    while True:
        tmp = s.recv(1)
        buffer.append(tmp)
        if ''.join(buffer).endswith(token):
            break
    return ''.join(buffer[:-5])


def client():
    s = socket.socket()
    s.connect(('127.0.0.1', 9999))
    print('connect to 127.0.0.1 9999')
    s.send('START' + END)

    e = int(recv_until(s))
    n = int(recv_until(s))

    print('recv E: %d' % e)
    print('recv N: %d' % n)

    aes_key = os.urandom(16).encode('hex')
    print('generate random AES key: %s' % aes_key)

    os.system('aes enc %s secret.txt secret.enc' % aes_key)
    print('encrypt secret.enc with AES128...')

    enc_content = open('secret.enc', 'rb').read()

    print('sending encrypted file')
    s.send(enc_content + END)

    print('sending encrypted AES key...')
    enc_key = str(rsa.encrypt(aes_key, e, n))
    s.send(enc_key + END)

    print('secret file transfering ok')


def server():
    s = socket.socket()
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print('listent at 127.0.0.1 9999')
    conn, addr = s.accept()
    print('recv connect from %s %d' % (addr[0], addr[1]))
    recv_until(conn)

    print('generate RSA key')
    e, d, n = rsa.get_rsa_key()
    print('E: %d' % e)
    print('D: %d' % d)
    print('N: %d' % n)

    print('sending E and N...')
    conn.send(str(e).strip('L') + END)
    conn.send(str(n).strip('L') + END)

    print('recv encrypted file and AES key')
    enc_content = recv_until(conn)
    enc_key = recv_until(conn)

    with open('server_secret.enc', 'wb') as fp:
        fp.write(enc_content)

    print('decrypt AES key...')
    key = int(enc_key)
    key = rsa.decrypt(key, d, n)
    print('AES key is %s' % key)

    print('decrypt encrypted file with AES key')
    os.system('aes dec %s server_secret.enc server_secret.txt' % key)

    print('the file\'s content is: ')
    print(open('server_secret.txt').read())


mode = sys.argv[1]
if mode == 'client':
    client()
elif mode == 'server':
    server()
