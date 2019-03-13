# coding: utf-8

# In[62]:

# Length Extension and Hashing Demo

# Basic hashing with pymd5
from pymd5 import md5, padding
import sys
m = "Hello There!"
h = md5()
h.update(m)
#print(h.hexdigest())

# Get number of bits in m
m_bits = len(m) * 8
# Get padding for message m
padding(m_bits)
# Padding size
padding_bits = len(padding(m_bits)) * 8

#print((m_bits + padding_bits) % 512 == 0)

m2 = "a" * 64
m2_bits = len(m2) * 8
# What do you think the padding will be for m2?

#print(len(padding(m2_bits)))

# Why is this the padding?

# Length extension attack (from spec)
m = "Use HMAC, not hashes"
h = md5()
h.update(m)
h.hexdigest()

# Assume we don't know m, but we know its hash is 3ecc68efa1871751ea9b0b1a5b25004d

# Keep state by "adding" one compression function block
h = md5(state="3ecc68efa1871751ea9b0b1a5b25004d".decode("hex"), count=512)
x = "Good advice"
h.update(x)
#print(h.hexdigest())

padded_message = m + padding(len(m) * 8) + x
h2 = md5()
h2.update(padded_message)
#print(h2.hexdigest())


# In[202]:

# Padding Oracle Attack Demo

from bottle import request, route, response, run
from Crypto.Cipher import AES
from Crypto import Random
from binascii import hexlify
import urllib2

# Pad the message to a multiple of 16 bytes
def pad(msg):
    n = len(msg)%16
    return msg + ''.join(chr(i) for i in range(16,n,-1))

# Remove the padding, returning an error if bad padding
def strip_padding(msg):
    padlen = 17 - ord(msg[-1])
    if padlen > 16 or padlen < 1:
        return True, None
    if msg[-padlen:] != ''.join(chr(i) for i in range(16,16-padlen,-1)):
        return True, None
    return False, msg[:-padlen]

# Encrypt the messages using CBC mode
def enc(key,msg):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(msg))

# Decrypt the message using CBC mode
def dec(msg):
    cipher = AES.new(key, AES.MODE_CBC, msg[:16])
    text = cipher.decrypt(msg[16:])
    return text

key = 'MYSUPERSECRETKEY'
plaintext = 'This is a pretty long message that requires some padding.'
ciphertext = bytearray(enc(key, plaintext))

first_block_idx = 16
prev_ciphertext = ciphertext[:first_block_idx]
current_block = ciphertext[first_block_idx:first_block_idx + 16]

#print(hexlify(prev_ciphertext))
#print(hexlify(current_block))

last_byte_of_first_block = prev_ciphertext[-1]
#print(hex(last_byte_of_first_block))

for guess in range(256):
    prev_ciphertext[-1] = last_byte_of_first_block ^ guess ^ 16
    fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
    msg = dec(fake_cipher.decode('hex'))
    err, msg = strip_padding(msg)
    if not err:
        #print('incorrect ciphertext!', guess)
        #print(guess)
        #print(chr(guess))
        pass


# In[201]:

# Weak RSA Key Generation Product Tree Demo
# From https://facthacks.cr.yp.to/batchgcd.html
from fractions import gcd
from math import floor

def prod(iterable):
    return reduce(lambda x, y: x*y, iterable, 1)

def productTree(X):
    result = [X]
    while len(X) > 1:
        X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
        result.append(X)
    return result

def batchgcd_faster(X):
    prods = producttree(X)
    R = prods.pop()
    while prods:
        X = prods.pop()
        R = [R[int(floor(i/2))] % X[i]**2 for i in range(len(X))]
    return [gcd(r/n,n) for r,n in zip(R,X)]

modulus = "49b8c9b4810e25cc5fef52ec4dfc01f62fa3df97671e12b9d7b1e339f610bb458bd0713f4fb0165ffb426cabb6d38526a8cf6564571f548ea2bd078e99bbb50f30351a234f1d91fc4338a0ca94e3e01788e2e9375e1c60a64ee0255d588f949898ef5e18726453a6e40e61758fe83b993a70b28b23126531dcb51bac34f377b1"
modulus2 = "49f87c01689b545d5a99a9e9c71411db25c3971a5bf7dac1bdc83a65d7ab96f5b3b6df3cf44b8ed02eee817a1eab514f6b9a1094c13fea125e473e754798428358914b50489d45c9ce49c1a13254af76d513cacc2eb52dd04da68f02610aabe818e323357487d5ccc0216f0175b56020ee3044dbe1648845759374dddd636141"
e = 65537

modulus_int = int(modulus, 16)
modulus2_int = int(modulus2, 16)

moduli = [modulus_int, modulus2_int]
batchgcd_faster(moduli)


# In[ ]: