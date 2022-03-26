#!/usr/bin/env python3
import binascii 
import threading
from time import *
import socketserver
from string import hexdigits
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

banner = """
Welcome to my supreme signing server!
Send me a signed command, I will verify and do it for you, I will also sign your commands, but don't tinker too much with them though!
I'm not Blind, I can see through your cunning ruse, sometimes!
"""

FLAG_FILE = "flag.txt"
class RSA:
    def __init__(self):
        self.e = 0x10001
        p = getPrime(1024)
        q = getPrime(1024)
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.d = inverse(self.e, phi)

    def get_public_key(self):
        return (self.e, self.n)

    def sign(self, msg):
        hex_str_of_peek = binascii.hexlify("peek".encode()).decode()
        if msg.startswith(hex_str_of_peek):
            return -1
        msg = bytes_to_long(binascii.unhexlify(msg.encode()))
        return pow(msg, self.d, self.n)

    def verify(self, msg):
        msg = bytes_to_long(binascii.unhexlify(msg.encode()))
        return pow(msg, self.e, self.n)
    
class Service(socketserver.BaseRequestHandler):
    #handle() will always run first
    def handle(self):
        self.get_flag()
        rsa = RSA()
        self.send(banner)

        while True:
            choice = self.receive("1. Sign\n2. Verify\nYour choice: ").decode()
            if choice == "1":
                cmd = self.receive("Command to sign: ").decode()

                if not self.assure_hex(cmd):
                    self.send("Please send a hex string!\n")
                    continue
                
                signed_msg = rsa.sign(cmd)

                if signed_msg != -1:
                    self.send("Message signed successfully!\n" + self.num_to_hex_str(signed_msg))
                else:
                    self.send("Ah ah, don't tinker with the commands!")

            elif choice == "2":
                cmd = self.receive("Command to verify: ").decode()

                if not self.assure_hex(cmd):
                    self.send("Please send a hex string!\n")
                    continue

                verified_cmd = rsa.verify(cmd)
                
                verified_cmd = long_to_bytes(verified_cmd)
                try:
                    #could be jibberish ¯\_(ツ)_/¯
                    verified_cmd = verified_cmd.decode()
                    
                    if verified_cmd == "peek flag":
                        self.send("Here is the flag!\n" + self.flag)
                        break
                    elif verified_cmd == "get pubkey":
                        self.send("Here is the public key!\n" + str(rsa.get_public_key()) + "\n")
                    else:
                        self.send("Command executed!")
                        break
                except:
                    self.send("There's something wrong with your command!")
                    break
            else:
                break
    
    def num_to_hex_str(self, num):
        return binascii.hexlify(long_to_bytes(num)).decode()

    def hex_str_to_num(self, string):
        return bytes_to_long(binascii.unhexlify(string.encode()))

    def assure_hex(self, string):
        return all(c in hexdigits for c in string)
    
    def get_flag(self):
        with open(FLAG_FILE, "r") as f:
            self.flag = f.read()

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")

        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt=": "):
        self.send(prompt, newline=False)
        return self.request.recv(1000).strip()

class ThreadedService(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
    socketserver.DatagramRequestHandler,
):
    pass

def main():
    port = 20314
    host = "103.245.249.107"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server started on " + str(server.server_address) + "!")
    # Now let the main thread just wait...
    while True:
        sleep(10)

if __name__ == "__main__":
    main()