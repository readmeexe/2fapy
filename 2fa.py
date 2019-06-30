import yaml
import hmac
import time
import base64
import struct
import hashlib
from os import system, name 

"""
mostly stolen from https://gist.github.com/acoster/4121786
"""

def clear(): 
    print(name)
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

def load_secrets(filepath):
    with open(filepath,"r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def get_hotp(secret, counter):
    secret  = base64.b32decode(secret)
    counter = struct.pack('>Q', counter)
    hash   = hmac.new(secret, counter, hashlib.sha1).digest()
    offset = hash[19] & 0xF
    return (struct.unpack(">I", hash[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000

def get_totp(secret):
    return get_hotp(secret, int(time.time()) // 30)

if __name__ == "__main__":
    filepath = "secrets.yml"
    data = load_secrets(filepath)

    while True:
        clear()
        print("Countdown:", 30 - (int(time.time()) % 30))
        for account,secret in data.items():
            code = get_totp(secret.replace(" ", "").upper())
            print("{:<10} {:<06d}".format(account,code))
        time.sleep(1)
