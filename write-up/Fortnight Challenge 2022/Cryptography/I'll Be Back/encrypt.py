#!/usr/bin/env python3
import binascii
import threading
from time import *
import socketserver
from random import choice
from string import ascii_uppercase, digits, hexdigits

banner = """
Hey! You there! Are you a perceptive one? Let's see.
I will give you an encrypted flag, and will even encrypt anything you send me!
But in the future where I came from, we can only read hexadecimal strings, so catch up!
Can you find the flag hidden in plain sight? 
"""

KEY_LENGTH = 6900
FLAG_FILE = "flag.txt"
class Service(socketserver.BaseRequestHandler):
    #handle() will always run first
    def handle(self):
        self.get_flag()
        self.key = ""
        self.key_position = 0

        self.send(banner)
        encrypted_flag = self.encrypt_flag().decode()
        if not encrypted_flag:
            return
        self.send("Here is the ecrypted flag:" + encrypted_flag + "\n")
        
        while True:
            self.send("Send me anything, I will encrypt it for you.")
            user_input = self.receive("Your message: ").strip().decode("utf-8")
            if (self.assure_hex(user_input)):
                user_input = bytes.fromhex(user_input)
                encrypted_user_input = self.encrypt_user_input(user_input).decode() 
                self.send("Encrypted message: " + encrypted_user_input + "\n") 
            else:
                self.send("Hey! That's not a hexadecimal string!\n")
                return
    
    def encrypt_flag(self):
        return self.strxor(self.flag, self.get_key(len(self.flag)))
    
    def encrypt_user_input(self, ui):
        return self.strxor(ui, self.get_key(len(ui)))

    def get_flag(self):
        with open(FLAG_FILE) as f:
            self.flag = f.readline()

    def get_key(self, length):
        if self.key == "":
            self.key = ''.join(choice(ascii_uppercase + digits) for _ in range(KEY_LENGTH))
        key_part = ''
        for i in range(length):
            key_part += self.key[(self.key_position + i) % KEY_LENGTH]
        self.key_position = (self.key_position + length) % KEY_LENGTH
        return key_part

    def assure_hex(self, ui):
        return all(c in hexdigits for c in ui)

    def strxor(self, a, b):
        if type(a) is str:
            a = bytes(a, encoding="utf-8")
        if type(b) is str:
            b = bytes(b, encoding="utf-8")
        return binascii.hexlify(bytes(i^j for i, j in zip(a, b)))

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
    port = 20302
    host = "103.245.249.207"

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