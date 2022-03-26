## Fortnight challenge 2022: I'll Be Back

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-16-lightgrey.svg)

### Description
Arnold Schwarzenegger left me a message and said Only The Perceptives can understand what it said. Are you a perceptive one?
Use nc 103.245.249.107 20302 to connect and solve the challenge.

### Hints
- None

### Attached files
- 

### Summary
It's a classic one time pad (OTP) challenge.

### Detailed solution
Reading the code, particularly the `get_key` function, is a good way to get an idea of how to solve the challenge.  
```
def get_key(self, length):
    if self.key == "":
        self.key = ''.join(choice(ascii_uppercase + digits) for _ in range(KEY_LENGTH))
    key_part = ''
    for i in range(length):
        key_part += self.key[(self.key_position + i) % KEY_LENGTH]
    self.key_position = (self.key_position + length) % KEY_LENGTH
    return key_part
```
Here we can spot a potential weakness in the key generation function. Everytime we call `get_key`, we are just getting a new part of a 6900-character long key. If the part itself is longer than the 6900th character, the key will loop back to the beginning.  
This is a weakness that we can exploit, because the problem encrypts its flag by xor-ing it with the flag-length part at the beginning of the key. Therefore, to get the flag, we only need to xor the encrypted flag with that particular key part.  
However, one bottleneck is that the server only accept 1000 characters at a time, but since we're communicating in hex, that's only 500 characters each time, so this require some rudimentary maths to get around.  

With the solution in mind, let's connect to the server and get the encrypted flag, and set the KEY_LENGTH accordingly.  
```
from pwn import *
conn = remote("103.245.249.107", 20302)

KEY_LENGTH = 6900

print(conn.recvuntil("Here is the ecrypted flag:".encode()).decode())
encrypted_flag = conn.recvline().decode().strip()
print(encrypted_flag)
flag_length = len(encrypted_flag) // 2

KEY_LENGTH -= flag_length
```

Now we can iteratively send trash data to the server to expend the key until we can loop it back around to the beginning.  
```
while True:
    print(conn.recvuntil("Your message: ".encode()).decode())
    
    msg_to_send = "a"*min(500, KEY_LENGTH)*2
    print(msg_to_send)
    conn.send(msg_to_send.encode())

    print(conn.recvuntil("Encrypted message: ".encode()).decode())
    print(conn.recvuntil("\n".encode()).strip().decode())

    KEY_LENGTH -= len(msg_to_send) // 2
    print("Key length left: ",KEY_LENGTH)
    if KEY_LENGTH == 0:
        break
```

Finally, we send out the encrypted flag to get the flag back.  
```
print(conn.recvuntil("Your message: ".encode()).decode())
print(encrypted_flag)
conn.send((encrypted_flag + "\n").encode())
print(conn.recvuntil("Encrypted message: ".encode()).decode())
flag = conn.recvline().decode().strip()
print(flag)
conn.close()

print("The flag is: " + bytearray.fromhex(flag).decode())
```

Full script:  
```
from pwn import *
conn = remote("103.245.249.107", 20302)

KEY_LENGTH = 6900

print(conn.recvuntil("Here is the ecrypted flag:".encode()).decode())
encrypted_flag = conn.recvline().decode().strip()
print(encrypted_flag)
flag_length = len(encrypted_flag) // 2

KEY_LENGTH -= flag_length

while True:
    print(conn.recvuntil("Your message: ".encode()).decode())
    
    msg_to_send = "a"*min(500, KEY_LENGTH)*2
    print(msg_to_send)
    conn.send(msg_to_send.encode())

    print(conn.recvuntil("Encrypted message: ".encode()).decode())
    print(conn.recvuntil("\n".encode()).strip().decode())

    KEY_LENGTH -= len(msg_to_send) // 2
    print("Key length left: ",KEY_LENGTH)
    if KEY_LENGTH == 0:
        break

print(conn.recvuntil("Your message: ".encode()).decode())
print(encrypted_flag)
conn.send((encrypted_flag + "\n").encode())
print(conn.recvuntil("Encrypted message: ".encode()).decode())
flag = conn.recvline().decode().strip()
print(flag)
conn.close()

print("The flag is: " + bytearray.fromhex(flag).decode())
```


Running the script in the console gives us the flag.  
```
[+] Opening connection to 103.245.249.107 on port 20302: Done  

Hey! You there! Are you a perceptive one? Let's see.  
I will give you an encrypted flag, and will even encrypt anything you send me!  
But in the future where I came from, we can only read hexadecimal strings, so catch up!  
Can you find the flag hidden in plain sight?  
  
Here is the ecrypted flag:  
53053e45366b21213b282e7a3e0f383355133b1720344324563b3965252c66783f5c33  
  
Send me anything, I will encrypt it for you.  
Your message:  
  
...  
  
Key length left:  0  
  
Send me anything, I will encrypt it for you.  
Your message:  
53053e45366b21213b282e7a3e0f383355133b1720344324563b3965252c66783f5c33  
Encrypted message:  
663072746e316768747b7930755f6172655f615f706572636570743176655f306e657d  
[*] Closed connection to 103.245.249.107 port 20302  
The flag is: f0rtn1ght{y0u_are_a_percept1ve_0ne}  
```

### Flag
```
f0rtn1ght{y0u_are_a_percept1ve_0ne}
```