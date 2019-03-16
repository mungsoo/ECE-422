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
    
# import sys, urllib
# from pymd5 import md5, padding

# # Command: python sol_3.2.1.2.py 3.2.1.2_query.txt 3.2.1.2_command3.txt sol_3.2.1.2.txt

# if len(sys.argv) < 4:
    # print("Missing arguments: python your_script.py query_file command3_file output_file")

# with open(sys.argv[1]) as query, open(sys.argv[2]) as command, open(sys.argv[3], 'w') as out:
	# query_content = query.read().strip()
	# command_content = command.read().strip()
	# token_str = (query_content.split("&")[0]).split("=")[1]
	# user_str = "user=" + query_content.split("user=")[1]

	# new_token = md5(state=token_str.decode("hex"), count=512)
	# new_token.update(command_content)
	# out.write("token=" + new_token.hexdigest() + '&' + user_str + urllib.quote(padding(len(user_str*8) + 8*8)) + command_content)

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

