from fractions import gcd
from math import floor
from pbp import encrypt, decrypt
from Crypto.PublicKey import RSA

def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x, y = gcdExtended(b % a, a)

    return gcd, y - b // a * x, x


def modInv(a, b):

    # Get x where ax = 1 (mod b)
    gcd, x, y = gcdExtended(a, b)

    # Modular multiplicative inverse only exists when a b are coprime
    if gcd != 1:
        raise Exception("Modular multiplicative inverse doesn't exist")
    else:
        return x % b


def prod(iterable):
    return reduce(lambda x, y: x*y, iterable, 1)


def productTree(X):
    result = [X]
    while len(X) > 1:
        X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
        result.append(X)
    return result


def batchgcd_faster(X):
    prods = productTree(X)
    R = prods.pop()
    while prods:
        X = prods.pop()
        R = [R[int(floor(i/2))] % X[i]**2 for i in range(len(X))]
    return [gcd(r/n,n) for r,n in zip(R,X)]


with open("3.2.4_ciphertext.enc.asc") as f:
    ciphtertext = f.read().replace("\r\n", "\n")

with open("moduli.hex") as f:
    modulis = map(str.strip, f.readlines())
    modulis = [int(i, 16) for i in modulis]


# Compute gcds of every modulis and save them to gcds.txt
# gcds = batchgcd_faster(modulis)
# gcds = map(str, gcds)
#
# with open("gcds.txt", "w") as f:
#     f.write("\n".join(gcds))

with open("gcds.txt") as f:
    gcds = map(str.strip, f.readlines())
    gcds = map(int, gcds)

e = 65537
private_keys = []

for i, p in enumerate(gcds):
    if p > 1:
        q = modulis[i] / p
        # Compute private key d, which is the modular multiplicative inverse
        try:
            d = modInv(e, (p - 1) * (q - 1))
            private_keys.append(RSA.construct((long(modulis[i]), long(e), long(d))))
        except "Modular multiplicative inverse doesn't exist":
            print("Error: Can not compute private key of modulis[%d]" % i)

# Try to decrypt using each private key
for key in private_keys:
    try:
        plaintext = decrypt(key, ciphtertext)
        print(plaintext)
        break
    except:
        pass

with open("sol_3.2.4.txt", "w") as f:
    f.write(plaintext)





