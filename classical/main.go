package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

type VigenereCipher struct {
	table [26][26]byte
	key   []byte
}

func NewVigenereCipher(key []byte) *VigenereCipher {
	v := &VigenereCipher{
		key: key,
	}
	v.init()
	return v
}

func (v *VigenereCipher) init() {
	for i := 0; i < 26; i++ {
		for j := 0; j < 26; j++ {
			v.table[i][j] = 'A' + (byte(i)+byte(j))%26
		}
	}
}

func (v VigenereCipher) displayTable() {
	for i := 0; i < 26; i++ {
		for j := 0; j < 26; j++ {
			fmt.Printf("%c ", v.table[i][j])
		}
		fmt.Println()
	}
}

func (v VigenereCipher) lookup(msg byte, key byte) byte {
	return v.table[msg-'A'][key-'A']
}

func (v VigenereCipher) lookupRev(cipher byte, key byte) byte {
	offset := int(cipher) - int(v.table[key-'A'][0])

	if offset < 0 {
		offset = 26 + offset
	}

	return 'A' + uint8(offset)
}

func (v VigenereCipher) extendKey(length int) []byte {
	var padding []byte
	keyLen := len(v.key)

	for i := 0; i < length; i++ {
		padding = append(padding, v.key[i%keyLen])
	}
	return padding
}

func (v VigenereCipher) encrypt(msg []byte) []byte {
	var output []byte
	key := v.extendKey(len(msg))

	for i, _ := range msg {
		if !isA2Z(msg[i]) {
			if isAlpha(msg[i]) {
				msg[i] = msg[i] - ('a' - 'A')
			} else {
				// output = append(output, msg[i])
				continue
			}
		}
		output = append(output, v.lookup(msg[i], key[i]))
	}
	return output
}

func (v VigenereCipher) decrypt(cipher []byte) []byte {
	var output []byte
	key := v.extendKey(len(cipher))

	for i, _ := range cipher {
		output = append(output, v.lookupRev(cipher[i], key[i]))
	}
	return output
}

func isA2Z(c byte) bool {
	return c >= 'A' && c <= 'Z'
}

func isAlpha(c byte) bool {
	return isA2Z(c) || (c >= 'a' && c <= 'z')
}

func banner() {
	fmt.Printf(
		"Usage:\n\t%s [enc | dec] key text [-f]\n\te.g. vigenere enc \"KEY\" \"helloworld\"",
		os.Args[0])
}

func main() {
	if len(os.Args) < 4 {
		banner()
		return
	}

	mode := os.Args[1]
	key := os.Args[2]
	text := os.Args[3]

	var isFile string
	if len(os.Args) > 4 {
		isFile = os.Args[4]
	}

	v := NewVigenereCipher([]byte(key))

	switch mode {
	case "enc":
		var bytes []byte
		if isFile == "-f" {
			bytes, _ = ioutil.ReadFile(text)
		} else {
			bytes = []byte(text)
		}
		cipher := v.encrypt(bytes)
		fmt.Println(string(cipher))

	case "dec":
		var bytes []byte
		if isFile == "-f" {
			bytes, _ = ioutil.ReadFile(text)
		} else {
			bytes = []byte(text)
		}
		msg := v.decrypt([]byte(bytes))
		fmt.Println(string(msg))

	default:
		banner()
	}
}
