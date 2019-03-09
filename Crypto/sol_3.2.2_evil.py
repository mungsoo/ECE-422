#!/usr/bin/python
# -*- coding: utf-8 -*-
blob = """            Ó‹ž		;òÊM„^Jp—˜h²FOC‚!ÄíÑõ¾h39ÆÇ
âü§qÛ×Òç#_ÿ7™•c_ÂKY)Ý2*<m¢wÅ€ìfcÉ¨Ä“¨Ûh!ƒÈ©µ*`ˆæÏëè¯rVºŽ’ékíZ©FZç¶$hº@±R
"""
from hashlib import sha256

if sha256(blob).hexdigest() == "46f1fbcb1d6f045ff2989d01200cbc23a8d68a5f00414ce2d9137bb05f247f7f":
    print "I come in peace."
else:
    print "Prepare to be destroyed!"
