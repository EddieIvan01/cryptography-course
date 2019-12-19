# Block Cipher

## AES128-ECB

```
$ main enc 010101 text.txt text-self.enc

$ openssl enc -aes-128-ecb -K 010101 -in text.txt -out text-openssl.enc

$ md5sum text-openssl.enc text-self.enc
c2d266451e4dae52e438a335c5914779 *text-openssl.enc
c2d266451e4dae52e438a335c5914779 *text-self.enc

$ openssl enc -aes-128-ecb -K 010101 -in text-self.enc -out 1 && cat 1
Hello, world! This is an AES128 cipher encrypt/decrypt in ECB mode.

```

