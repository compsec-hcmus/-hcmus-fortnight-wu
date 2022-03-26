## Fortnight challenge 2022: Deco de Crypto

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-34-lightgrey.svg)

### Description
My friend Deco de Crypto sent me this and challenged me to find his message. But how am I supposed to crack this code?

### Hints
- None

### Attached files
- [encoded](https://github.com/compsec-hcmus/hcmus-wu/raw/main/write-up/Fortnight%20Challenge%202022/Cryptography/Deco%20de%20Crypto/encoded)

### Summary
I used base 32 decode and base 64 decode

### Detailed solution
The challenge looks like it's the type of challenge that would repeatedly encode the message using various types of encodings. Since we don't know how many encodings are used, or how many times they are used. Based on the relatively short length of the message, we can guess it may have been encoded with hex, base32, and base64, the three most common encodings.  
With that in mind, I wrote a script to solve it automatically.  
```
from binascii import unhexlify  
from string import ascii_lowercase,  ascii_uppercase, digits  
from base64 import b64decode, b32decode  
a = open("encoded").readline()  
  
hex1 = ascii_uppercase+digits  
hex2 = ascii_lowercase+digits  
b32 = ascii_uppercase+"234567="  
b64 = ascii_uppercase+ascii_lowercase+digits+"+/="  
  
def isHex(a):  
    return all(i in hex1 for i in a) or all(i in hex2 for i in a)  
  
def isBase32(a):  
    return all(i in b32 for i in a)  
  
def isBase64(a):  
    return all(i in b64 for i in a)  
  
while not a.startswith("f0rtn1ght"):  
    if isBase32(a):  
        a = b32decode(a).decode()  
        continue  
    if isBase64(a):  
        a = b64decode(a).decode()  
        continue  
    if isHex(a):  
        a = unhexlify(a).decode()  
        continue  
  
print(a)  
```
Running it in the console returns the flag:  
```
f0rtn1ght{n01ce_ba5e5}  
```
### Flag
```
f0rtn1ght{n01ce_ba5e5}
```
