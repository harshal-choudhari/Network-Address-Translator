#! /usr/bin/python
#Script to automate task of installing and configuring dhcp server 

import ConfigParser, sys, subprocess

def executeCmd(cmd):
 subprocess.call(cmd,shell=True)
 subprocess.call("sleep 1",shell=True)

def setupDhcp():
  config = ConfigParser.ConfigParser()
  config.read(sys.argv[1])
  #CODE TO GET RETURN VALUE#
  retCode = subprocess.Popen("which dhcpd", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
  theInfo = retCode.communicate()[0].strip()
  retVal = retCode.returncode
  ##########################
  debFilePath = config.get('lan1','debFilePath')
  if(retVal != 0):
    executeCmd("dpkg -i {}/* >> /dev/null 2>&1".format(debFilePath))
  
  executeCmd("cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.backup >> /dev/null 2>&1")
  sec = list(config.sections())
  for x in sec:
    network = config.get(x,'network_ip')
    lease = config.get(x,'default_lease_time')
    max_lease = config.get(x,'max_lease_time')
    starting_ip = config.get(x,'starting_range')
    ending_ip = config.get(x,'ending_range')
    netmask = config.get(x,'network_mask')
    gateway = config.get(x,'default_gateway')
    executeCmd("echo 'subnet "+ network +" netmask "+ netmask +" {' >> /etc/dhcp/dhcpd.conf")
    executeCmd("echo 'range "+ starting_ip +" "+ ending_ip +";' >> /etc/dhcp/dhcpd.conf")
    executeCmd("echo 'option routers "+ gateway +";' >> /etc/dhcp/dhcpd.conf")
    executeCmd("echo 'default-lease-time "+ lease +";' >> /etc/dhcp/dhcpd.conf")
    executeCmd("echo 'max-lease-time "+ max_lease +";\n}' >> /etc/dhcp/dhcpd.conf")
    #executeCmd("/etc/init.d/isc-dhcp-server restart")

if __name__ == '__main__':
  setupDhcp()
