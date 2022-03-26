## Fortnight challenge 2022: Really Silly Algorithm

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-9-lightgrey.svg)

### Description
I'm making a signing server project to apply for an internship at a bank. I implemented a Really Silly Algorithm, see if you can hack it.
Use nc 103.245.249.107 20314 to connect and solve the challenge.

### Hints
- None

### Attached files
- [server.py](https://raw.githubusercontent.com/compsec-hcmus/hcmus-wu/main/write-up/Fortnight%20Challenge%202022/Cryptography/Really%20Silly%20Algorithm/server.py)

### Summary
It's an RSA challenge that can be solved using the Blinding attack.

### Detailed solution
[Provide the detailed solution of the ctf here.]
Some rules:
Name of tool, name of file, name of functions, etc: put in 1 set of backtick:  `name of something`
Code snippet, console output, other long multilines of text: put in 3 sets of backticks on a new line: 
```code snippet```
Key ideas, name of person who invented the method, etc: put in bold **name of someone** 

The challenge itself is quite straight forward, it's a signing server that can sign our commands, verify our signed commands and execute those commands.  
Tracing back from the commands that we can execute, we see that we can get the flag using "peek flag"  
```
if verified_cmd == "peek flag":
    self.send("Here is the flag!\n" + self.flag)
    break
```

So the problem is simple, send "peek flag", get signed, send back the signed command, get flag, get some pizza, enjoy the afternoon.  
But here's a catch, the `sign` function won't let us sign commands starting with "peek"  
```
def sign(self, msg):
    hex_str_of_peek = binascii.hexlify("peek".encode()).decode()
    if msg.startswith(hex_str_of_peek):
        return -1
    msg = bytes_to_long(binascii.unhexlify(msg.encode()))
    return pow(msg, self.d, self.n)
```

This elevates the difficulty a bit, but nothing a lil' math can't solve.  
  
Let m = the numerical representation of "peek flag".  
Essentially, `sign` will give us C = m^d mod n.  
And `verify` will revert it back to C^e mod n = m^(de) mod n = m mod n.  
  
But since the server will not sign m, we can sneakily send some m1 such that we can later convert m1 back to m and get it verified.  
This is where the **Blinding attack** comes in.  
By this attack, instead of sending m, we can send m1 = m*k^e mod n for some arbitrary k.  
Then when we get back C1 = m1^d mod n = m^d*k^(ed) mod n = m^d*k mod n, we can just divide C1 by k and get C = m^d mod n. We can then send this C value to verify and get the flag.  
One key thing that we will need is ofcourse the public key, since we need to calculate m1 = m*k^e mod n. Luckily, the server also send us the public key with the "get_pubkey" command.  
```
elif verified_cmd == "get pubkey":
    self.send("Here is the public key!\n" + str(rsa.get_public_key()) + "\n")
```

With that idea in mind, let's write some helper functions.  
```
from pwn import *
from binascii import hexlify, unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
conn = remote("103.245.249.107", 20314)
e = 0x10001
n = 0

def num_to_hex_str(num):
    return binascii.hexlify(long_to_bytes(num)).decode()

def hex_str_to_num(string):
    return bytes_to_long(binascii.unhexlify(string.encode()))

def to_sign(conn, msg, hex=False):
    print(conn.recvuntil("Your choice: ".encode()).decode())
    print("1")
    conn.sendline("1\n".encode())
    print(conn.recvuntil("Command to sign: ".encode()).decode())
    if hex == False:
        msg = hexlify(msg.encode()).decode()
    print(msg)
    conn.sendline((msg + "\n").encode())
    print(conn.recvline().decode())
    signed_cmd = conn.recvline().decode()
    print(signed_cmd)
    return signed_cmd

def to_verify(conn, cmd, get_output=False):
    print(conn.recvuntil("Your choice: ".encode()).decode())
    print("2")
    conn.sendline("2\n".encode())
    print(conn.recvuntil("Command to verify: ".encode()).decode())
    print(cmd)
    conn.sendline((cmd + "\n").encode())
    print(conn.recvline().decode())
    if get_output == True:
        pubkey = conn.recvline().decode()
        print(pubkey)
        return pubkey
```

And of course, the main action, here I choose k = 5.  
```
signed_cmd = to_sign(conn, "get pubkey")
pubkey = to_verify(conn, signed_cmd, True)

n = int(pubkey.split(", ")[1][:-2])

cmd = bytes_to_long("peek flag".encode())
blinded_cmd = cmd * pow(5, e, n)
blinded_cmd = num_to_hex_str(blinded_cmd)

blinded_signed_cmd = to_sign(conn, blinded_cmd, True).strip()

blinded_signed_cmd = hex_str_to_num(blinded_signed_cmd)
blinded_signed_cmd = blinded_signed_cmd * inverse(5, n) % n
blinded_signed_cmd = num_to_hex_str(blinded_signed_cmd)

to_verify(conn, blinded_signed_cmd, True)
conn.close()
```

The full script:  
```
from pwn import *
from binascii import hexlify, unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
conn = remote("103.245.249.107", 20314)
e = 0x10001
n = 0

def num_to_hex_str(num):
    return binascii.hexlify(long_to_bytes(num)).decode()

def hex_str_to_num(string):
    return bytes_to_long(binascii.unhexlify(string.encode()))

def to_sign(conn, msg, hex=False):
    print(conn.recvuntil("Your choice: ".encode()).decode())
    print("1")
    conn.sendline("1\n".encode())
    print(conn.recvuntil("Command to sign: ".encode()).decode())
    if hex == False:
        msg = hexlify(msg.encode()).decode()
    print(msg)
    conn.sendline((msg + "\n").encode())
    print(conn.recvline().decode())
    signed_cmd = conn.recvline().decode()
    print(signed_cmd)
    return signed_cmd

def to_verify(conn, cmd, get_output=False):
    print(conn.recvuntil("Your choice: ".encode()).decode())
    print("2")
    conn.sendline("2\n".encode())
    print(conn.recvuntil("Command to verify: ".encode()).decode())
    print(cmd)
    conn.sendline((cmd + "\n").encode())
    print(conn.recvline().decode())
    if get_output == True:
        pubkey = conn.recvline().decode()
        print(pubkey)
        return pubkey

signed_cmd = to_sign(conn, "get pubkey")
pubkey = to_verify(conn, signed_cmd, True)

n = int(pubkey.split(", ")[1][:-2])

cmd = bytes_to_long("peek flag".encode())
blinded_cmd = cmd * pow(5, e, n)
blinded_cmd = num_to_hex_str(blinded_cmd)

blinded_signed_cmd = to_sign(conn, blinded_cmd, True).strip()

blinded_signed_cmd = hex_str_to_num(blinded_signed_cmd)
blinded_signed_cmd = blinded_signed_cmd * inverse(5, n) % n
blinded_signed_cmd = num_to_hex_str(blinded_signed_cmd)

to_verify(conn, blinded_signed_cmd, True)
conn.close()
```

Console output:  
```
[x] Opening connection to 103.245.249.107 on port 20314  
[x] Opening connection to 103.245.249.107 on port 20314: Trying 103.245.249.107  
[+] Opening connection to 103.245.249.107 on port 20314: Done  
  
Welcome to my supreme signing server!  
Send me a signed command, I will verify and do it for you, I will also sign your commands, but don't tinker too much with them though!  
I'm not Blind, I can see through your cunning ruse, sometimes!  
  
...  
  
Command to verify:  
47b6e1c8a9196c1fc77a09ab0a851a62299305ab20122cecb261df5404b5b4bc479ff40be381b98082d2af4ebd3e6e30c32585a37eb50d2211c05ed17379666491fc6b3c56c762e04559ce2854a9cf7b9296614b1ca75c1a58c3cc00b80588fb895f8d32b397356d411dab2c09b4c8376a62952e054f6a1d7c3ac0fb65fb6a939dce86298525eb9aed5d5da11489b108fbce2074f917f0bafd2cb0311f79271409e7bf842f6a0bd9b4cced5c9c736b7a6115317fa2cfc89d2e1255027d8b1c0899b3f0d158ab2ff328db1ac54ba5e706730e67bf1e4b31be4c1600ec9a0a02d5e23190bc74c9f09cffc6338f6df199c46bcf422ce4c777dafcef1e480d11b447  
Here is the flag!  
  
f0rtn1ght{0uch_such_bl1nd1ng_l1ght}  
```

### Flag
```
f0rtn1ght{0uch_such_bl1nd1ng_l1ght}
```
