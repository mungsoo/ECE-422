#!/usr/bin/python
# -*- coding: utf-8 -*-
blob = """          l"�����q��:M��1m�w�h���vm�5���|�mK�?3�dz'�)�Ԍ���g�X�<`j%�f�C�Z��)N�������,=��'��f纄��<����b�N�*H_OOy��"""
from hashlib import sha256
# print sha256(blob).hexdigest()
if sha256(blob).hexdigest() == "89a9f565079540c5618b4ecc3c04fc21bd3054656d4b16d44c659b34bfc408e8":
    print "I come in peace."
else:
    print "Prepare to be destroyed!"