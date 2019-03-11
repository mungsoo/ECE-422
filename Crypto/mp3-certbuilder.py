from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.Util import number
import datetime
import hashlib

# Utility to make a cryptography.x509 RSA key object from p and q
def make_privkey(p, q, e=65537):
    n = p*q
    d = number.inverse(e, (p-1)*(q-1))
    iqmp = rsa.rsa_crt_iqmp(p, q)
    dmp1 = rsa.rsa_crt_dmp1(e, p)
    dmq1 = rsa.rsa_crt_dmq1(e, q)
    pub = rsa.RSAPublicNumbers(e, n)
    priv = rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, pub)
    pubkey = pub.public_key(default_backend())
    privkey = priv.private_key(default_backend())
    return privkey, pubkey

# The ECE422 CA Key! Your cert must be signed with this.
ECE422_CA_KEY, _ = make_privkey(10079837932680313890725674772329055312250162830693868271013434682662268814922750963675856567706681171296108872827833356591812054395386958035290562247234129L,13163651464911583997026492881858274788486668578223035498305816909362511746924643587136062739021191348507041268931762911905682994080218247441199975205717651L)

# Skeleton for building a certificate. We will require the following:
# - COMMON_NAME matches your netid.
# - COUNTRY_NAME must be US
# - STATE_OR_PROVINCE_NAME must be Illinois
# - issuer COMMON_NAME must be ece422
# - 'not_valid_before' date must must be March 1
# - 'not_valid_after'  date must must be March 27
# Other fields (such as pseudonym) can be whatever you want, we won't check them
def make_cert(netid, pubkey, ca_key = ECE422_CA_KEY, serial=4772483458719937903370594016975L):
    builder = x509.CertificateBuilder()
    builder = builder.not_valid_before(datetime.datetime(2017, 3, 1))
    builder = builder.not_valid_after (datetime.datetime(2017, 3,27))
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, unicode(netid)),
        x509.NameAttribute(NameOID.PSEUDONYM, u'unused'),
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Illinois'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'ece422'),
]))
    builder = builder.serial_number(serial)
    builder = builder.public_key(pubkey)
    cert = builder.sign(private_key=ECE422_CA_KEY, algorithm=hashes.MD5(), backend=default_backend())
    return cert

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print 'usage: python mp3-certbuilder <netid> <outfile.cer>'
        sys.exit(1)
    netid = sys.argv[1]
    outfile = sys.argv[2]
    p = number.getPrime(1024)
    q = number.getPrime(1024)
    privkey, pubkey = make_privkey(int("f4930d9a0e13105411d3aabd8d26679898b25900e203624b053fb22041dc51afc19009d097402c60523ceb52a012bab9ea7c38959801e48b17e5907bcf001", 16), \
    int("2a853dde31bc8585f82b9e0ddecfdc4baacc54b7ec62d2b6f9c0279ba62337df1540ad947c70fc2161f115296f7eac016a2740096c492157e55ea7dc6302cc06b66aeab1bdd17c6f897470c639a95195940258b9be1fa55cf35ed5c824e92b4101b2c1b2dd21c1815440e0b4c06ef673224203cb22ff264cb057547361219f07b56fc09ef123d754ea8c655fb7e129226ff2128a2754f1ff3b8a61c299a1bfee7c03bf2b0de1370081a83da1a74448bbe9bc319829d300abc3f401bad7f82b3ed7b", 16))
    # privkey, pubkey = make_privkey(int("a106717ccde380feb772cb623824a4c5a24da164e4b82ec412346e091062ae6ede7ac612d67af85135cba4656e9fe2b83be372861fc6c63690f77daad61ad", 16), \
    # int("409523f412d97e5d3b635a2fe287147a7f00c3e1d1bee1a61912558e34c92d2967a81fc13c23d421c14977d5acbeb9bbdfdbeb1079d094c120d8fabb0c00410fc89e3cf13a64b8f934110a045164c185965ba32baee0b074f49266f3abd37d7f6b6c8632544a46ddf745410347138eed1a78c879833933ef0000276ec35bd96a0d04924bdfa6c34496a6695280e1cdb313c45136e0851410659ed884f91da51d7619c2e795805b17c68db59567988a1c499deb38d8a713399346d26e698b11f90c7", 16))
    cert = make_cert(netid, pubkey)
    print 'md5 of cert.tbs_certificate_bytes:', hashlib.md5(cert.tbs_certificate_bytes).hexdigest()

    # We will check that your certificate is DER encoded
    # We will validate it with the following command:
    #    openssl x509 -in {yourcertificate.cer} -inform der -text -noout
    with open(outfile, 'wb') as f:
        f.write(cert.public_bytes(Encoding.DER))
    print 'try the following command: openssl x509 -in %s -inform der -text -noout' % outfile
