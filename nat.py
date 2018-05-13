#!/usr/bin/python

import subprocess
import ConfigParser
import sys

def executeCmds(cmds):
    for i in cmds:
        subprocess.call(i,shell=True)

def setupNat():
    cmds = []
    cmds.append("/sbin/depmod -a >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_tables >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_conntrack >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_conntrack_ftp >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_conntrack_irc >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe iptable_nat >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_nat_ftp >> /dev/null 2>&1")
    cmds.append("/sbin/modprobe ip_nat_irc >> /dev/null 2>&1")

    cmds.append("echo '1' > /proc/sys/net/ipv4/ip_forward >> /dev/null 2>&1")
    cmds.append("echo '1' > /proc/sys/net/ipv4/ip_dynaddr >> /dev/null 2>&1")

    # Clearing any existing rules and setting default policy
    cmds.append("iptables -P INPUT ACCEPT")
    cmds.append("iptables -F INPUT ")
    cmds.append("iptables -P OUTPUT ACCEPT")
    cmds.append("iptables -F OUTPUT ")
    cmds.append("iptables -P FORWARD DROP")
    cmds.append("iptables -F FORWARD ")
    cmds.append("iptables -t nat -F")

    # FWD: Allow all connections OUT and only existing and related ones IN
    cmds.append("iptables -A FORWARD -i {} -o {} -m state --state ESTABLISHED,RELATED -j ACCEPT >> /dev/null 2>&1".format(EXTIF, INTIF))
    cmds.append("iptables -A FORWARD -i {} -o {} -j ACCEPT >> /dev/null 2>&1".format(INTIF, EXTIF))

    # Enabling SNAT (MASQUERADE) functionality on $EXTIF
    cmds.append("iptables -t nat -A POSTROUTING -o {} -j MASQUERADE >> /dev/null 2>&1".format(EXTIF))
    executeCmds(cmds)

if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read(sys.argv[1])
    INTIF = conf.get('natConfig', 'internalInterface')
    EXTIF = conf.get('natConfig', 'externalInterface')
    setupNat()
