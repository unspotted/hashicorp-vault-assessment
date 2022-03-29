import base64
import argparse
from itertools import cycle
from operator import xor

parser = argparse.ArgumentParser(description="Decode Vault root token from base64 encoded token and OTP")
parser.add_argument("token", help="base64 encoded root token")
parser.add_argument("otp", help="OTP provided during the generation step")
args = parser.parse_args()

# Taken from https://stackoverflow.com/questions/55008149/xor-two-strings-of-different-length
def xor_two_str(a,b):
    short, long = sorted((a.encode("utf-8"), b.encode("utf-8")), key=len)
    xored = bytes(map(xor, long, cycle(short)))
    return xored.hex()

# padding needed for decoding
token = args.token + "=="
token = base64.b64decode(token)
str_token = token.decode("utf-8")
otp = args.otp

new_root = xor_two_str(str_token,otp)
byte_array = bytearray.fromhex(new_root)
print(byte_array.decode())