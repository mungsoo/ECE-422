import urllib2
from bottle import request, route, response, run
from Crypto.Cipher import AES
from Crypto import Random
from binascii import hexlify

def get_status(u):
    req = urllib2.Request(u)
    try:
        f = urllib2.urlopen(req)
        return f.code
    except urllib2.HTTPError, e:
        return e.code


# Pad the message to a multiple of 16 bytes
def pad(msg):
    n = len(msg)%16
    return msg + ''.join(chr(i) for i in range(16,n,-1))


def strip_padding(msg):
    padlen = 17 - ord(msg[-1])
    if padlen > 16 or padlen < 1:
        return True, None
    if msg[-padlen:] != ''.join(chr(i) for i in range(16,16-padlen,-1)):
        return True, None
    return False, msg[:-padlen]


with open("3.2.3_ciphertext.hex") as f:
    ciphertext = bytearray(f.read().strip().decode("hex"))

base_url = "http://cs461-mp3.sprai.org:8081/mp3/haoyuan9/?"
result = []

for pos in range(len(ciphertext) // 16 - 1, 0, -1):
    prev_ciphertext = ciphertext[16 * (pos - 1):16 * pos]
    current_block = ciphertext[16 * pos:16 * (pos + 1)]
    for offset in range(1, 17):
        target_byte = prev_ciphertext[-offset]
        # print(offset)
        for guess in range(256):
            prev_ciphertext[-offset] = target_byte ^ guess ^ 16
            fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
            # print(fake_cipher)
            url = base_url + fake_cipher
            # print url
            status = get_status(url)
            # print(status)
            if status == 404:
                result.append(chr(guess))
                print(chr(guess))
                for i in range(offset):
                    prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (15 - i)
                break

result.reverse()
_, msg = strip_padding("".join(result))
print(msg)

with open("sol_3.2.3.txt", "w") as f:
    f.write(msg)

# A local example
#
#
# # Encrypt the messages using CBC mode
# def enc(key,msg):
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     return iv + cipher.encrypt(pad(msg))
#
# # Decrypt the message using CBC mode
# def dec(msg):
#     cipher = AES.new(key, AES.MODE_CBC, msg[:16])
#     text = cipher.decrypt(msg[16:])
#     return text
#
# key = 'MYSUPERSECRETKEY'
# plaintext = 'This is a pretty long message that requires some padding.'
# ciphertext = bytearray(enc(key, plaintext))
#
# first_block_idx = 16
# prev_ciphertext = ciphertext[:first_block_idx]
# current_block = ciphertext[first_block_idx:first_block_idx + 16]
#
# #print(hexlify(prev_ciphertext))
# #print(hexlify(current_block))
#
# last_byte_of_first_block = prev_ciphertext[-1]
# result = []
# #print(hex(last_byte_of_first_block))
# for pos in range(len(ciphertext) // 16 - 1, 0, -1):
#     prev_ciphertext = ciphertext[16 * (pos - 1):16 * pos]
#     current_block = ciphertext[16 * pos:16 * (pos + 1)]
#     for offset in range(1, 17):
#         target_byte = prev_ciphertext[-offset]
#         # print(offset)
#         for guess in range(256):
#             prev_ciphertext[-offset] = target_byte ^ guess ^ 16
#             fake_cipher = hexlify(prev_ciphertext) + hexlify(current_block)
#             msg = dec(fake_cipher.decode('hex'))
#             err, msg = strip_padding(msg)
#             if not err:
#                 #print('incorrect ciphertext!', guess)
#                 print(chr(guess))
#                 result.append(chr(guess))
#                 for i in range(offset):
#                     prev_ciphertext[-offset + i] = prev_ciphertext[-offset + i] ^ (16 - i) ^ (15 - i)
#                 break
# result.reverse()
# _, msg = strip_padding("".join(result))
# print(msg)