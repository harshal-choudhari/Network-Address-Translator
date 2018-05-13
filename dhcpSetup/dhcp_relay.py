#! /usr/bin/python
#script to automate install and configure dhcp relay server.

import ConfigParser, sys, subprocess

def executeCmd(cmd):
 subprocess.call(cmd,shell=True)
 subprocess.call("sleep 1",shell=True)

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read(sys.argv[1])
	debFilePath = config.get('general','debFilePath')
	try:
		executeCmd("which dhcrelay >> /dev/null 2>&1")
	except:
		executeCmd("dpkg {}/isc-dhcp-relay*.deb".format(debFilePath)) 
	executeCmd("cp /etc/default/isc-dhcp-relay /etc/default/isc-dhcp-relay.backup >> /dev/null 2>&1")
	server = config.get('relay','server_ip')
	interface = config.get('relay','interfaces')
	executeCmd("sed -i 's/SERVERS.*/SERVERS="+ server +"/' /etc/default/isc-dhcp-relay >> /dev/null 2>&1")
	executeCmd("sed -i 's/INTERFACES.*/INTERFACES="+ interface +"/' /etc/default/isc-dhcp-relay >> /dev/null 2>&1")
