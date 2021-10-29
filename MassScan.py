import random
import socket
import threading
import time
import re
import mcstatus
import termcolor
import waiting
scanType = int(input("1 - Spam, 2 - Scan an IP: "))
server = input("Enter Server IP: ")

port = 1
threads = []
tries = 3
WorkingServrs = []
outputFile = open("results.txt", "w")
def PingSpecificServer():
    global port

    try:
        TargetServer = mcstatus.MinecraftServer.lookup(server + ":" + str(port))
        # In case of an aternos server the port is not 25565 but something random
        # and we are finding the port that the server actually uses

        if TargetServer.status().description.find("aternos") != -1 and TargetServer.status().description.find("offline") == -1:
            print(TargetServer.status().description)
            result = re.search(':(.*)§7§',TargetServer.status().description)
            port = result.group(1)
            print(port)

        elif TargetServer.status().description.find("offline") != -1:
            print("Server offline")
            exit()

        print(TargetServer.status().latency)

    except socket.timeout:
        time.sleep(0.2)
        print("Timed out, continue")


def PingDomain(targetPort, retries):
    triesLeft = retries - 1

    try:
        TargetServer = mcstatus.MinecraftServer.lookup(server + ":" + str(targetPort))
        # In case of an aternos server the port is not 25565 but something random
        # and we are finding the port that the server actually uses

        if TargetServer.status().description.find("aternos") != -1 and TargetServer.status().description.find("offline") == -1:
            print(TargetServer.status().description)
            result = re.search(':(.*)§7§',TargetServer.status().description)
            port = result.group(1)
            print(port)


        termcolor.cprint("Server on " + server + ":"+ str(targetPort) + " replied! it is running on version " + TargetServer.status().version.name, color='green')
        outputFile.write(server + ":" + str(targetPort) + "\n")

    except socket.timeout:
        time.sleep(random.uniform(1, 10))
        if targetPort != 1:
            if triesLeft > 0:
                PingDomain(targetPort, triesLeft)

    except ConnectionRefusedError:
        time.sleep(random.uniform(1, 10))
        if targetPort != 1:
            if triesLeft > 0:
                PingDomain(targetPort, triesLeft)

    except ConnectionResetError:
        time.sleep(random.uniform(1, 10))
        if targetPort != 1:
            if triesLeft > 0:
                PingDomain(targetPort, triesLeft)

    except OSError:
        time.sleep(random.uniform(1, 10))
        if targetPort != 1:
            if triesLeft > 0:
                PingDomain(targetPort, triesLeft)



def createThread(times):
    global scanType
    global port
    global tries


    if scanType == 2:
        for i in range(times - 1):
            t = threading.Thread(target=PingDomain, args=(len(threads) + 1, tries))
            threads.append(t)
            t.start()

    elif scanType == 1:
        for _ in range(times - 1):
            t = threading.Thread(target=PingSpecificServer)
            threads.append(t)
            try:
                t.start()
            except:
                print("slep")
                time.sleep(3)


if scanType == 1:
    PingSpecificServer()
    createThread(2)
elif scanType == 2:
    PingDomain(1, 0)
    createThread(65535)
for thread in threads:
    thread.join()
outputFile.close()
