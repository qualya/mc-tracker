from mcstatus import JavaServer #https://github.com/py-mine/mcstatus
from time import sleep, time, strftime, localtime
import threading
from tqdm import tqdm
import os
currentDir = os.getcwd()

startingThreads = threading.active_count()+1

path = currentDir + "/mc-data"
if os.path.isdir(path) == False:
    os.mkdir(path)
filePath = path + "/players.txt"
if os.path.exists(filePath) == False:
    open(filePath, "w").close()


filteredStrings = ["§"]
def getMC(address):
    try:
        server = JavaServer.lookup(address)
        status = server.status()
        timestamp = str(time())
        try:
            for player in status.players.sample:
                uuid = str(player.id).replace("|", "!").replace(";", ":").replace(",", ".").replace("\n", " ").replace("-", "")
                username = str(player.name).replace("|", "!").replace(";", ":").replace(",", ".").replace("\n", " ")
                
                add = True
                for string in filteredStrings:
                    if string in username:
                        add = False
                if add == True:
                    playerData.append([uuid, username, [[address, timestamp]]])
        
        except Exception as error:
            pass
    
    except Exception as error:
        pass



print("\n\nDo you want to scan servers for players [1], or read player data [2]?")
mode = input()
while mode not in ["1", "2"]:
    print("\nInput must be '1', or '2'.")
    mode = input()



if mode == "1":
    print("\n\nHow many threads do you want to use? (64 seems to work well)")
    properInput = False
    while properInput == False:
        max_threads = input() #64
        if max_threads.isdigit():
            max_threads = int(max_threads)
            if max_threads > 0:
                properInput = True
            else:
                print("\nThe number of threads must be greater than 0.")
        else:
            print("\nThis is not a valid number.")
    


    print("\n\nWhat is the search interval you want (in seconds) for scanning all the addresses?")
    properInput = False
    while properInput == False:
        searchInterval = input()
        if searchInterval.isdigit():
            searchInterval = int(searchInterval)
            if searchInterval > 0:
                properInput = True
            else:
                print("\nThe search interval must be greater than 0.")
        else:
            print("\nThis is not a valid number.")



    print("\n\nWhat is the name of the file containing the server addresses you want to be scanned?")
    filename = input("Filename: ")
    while os.path.exists(filename) == False:
        print("\nFile not found.")
        filename = input("Filename: ")
    addressList = list()
    with open(filename, "r", encoding="utf8") as txt:
        for line in txt:
            addressList.append(line.replace("\n", ""))
    print("\n")



    while True:
        start_time = time()


        playerData = list()
        with open(currentDir + "/mc-data/players.txt", "r", encoding="utf8") as txt:
            for line in txt: #uuid|username|address:timestamp,address:timestamp --> [uuid, username, [[address, timestamp], [address, timestamp]]]
                data = line.replace("\n", "").split("|")
                data[2] = data[2].split(",")
                for i in range(len(data[2])):
                    data[2][i] = data[2][i].split(";")
                playerData.append(data)


        for address in tqdm(addressList):
            threading.Thread(target=getMC, args=[address]).start()
            while threading.active_count() > max_threads: # limit the number of threads.
                sleep(1)
        while threading.active_count() > startingThreads:
            sleep(1)


        newPlayerData = [[], [], []] #format of two players, each having been on two servers: [[uuid, uuid], [username, username], [[[address, timestamp], [address, timestamp]], [[address, timestamp], [address, timestamp]]]]
        for data in playerData:
            if data[0] in newPlayerData[0]:
                position = newPlayerData[0].index(data[0])
                newPlayerData[1][position] = data[1]
                for address, timestamp in data[2]:
                    found = False
                    for i in range(len(newPlayerData[2][position])): #newPlayerData[2][position] will contain a list of addresses and timestamps
                        if address == newPlayerData[2][position][i][0]:
                            newPlayerData[2][position][i][1] = timestamp
                            found = True
                    if found == False:
                        newPlayerData[2][position].append([address, timestamp])
            else:
                newPlayerData[0].append(data[0])
                newPlayerData[1].append(data[1])
                newPlayerData[2].append(data[2])


        with open(currentDir + "/mc-data/players.txt", "w", encoding="utf8") as txt:
            for i in range(len(newPlayerData[0])):
                uuid, username = newPlayerData[0][i], newPlayerData[1][i]
                line = uuid + "|" + username + "|"
                for address, timestamp in newPlayerData[2][i]:
                    line = line + address + ";" + timestamp + ","
                line = line[:-1] + "\n"
                txt.write(line)


        end_time = time()
        elapsed = end_time-start_time
        print("Elapsed time: " + str(elapsed) + " seconds")
        timeLeft = searchInterval - elapsed
        if timeLeft >= 0:
            print("Time until next search: " + str(searchInterval - (end_time-start_time)) + " seconds")
            sleep(searchInterval - (end_time-start_time))
        else:
            print("Falling " + str(abs(timeLeft)) + " seconds behind schedule.")
        print()




if mode == "2":
    playerData = [[], [], []]
    with open(currentDir + "/mc-data/players.txt", "r", encoding="utf8") as txt:
        for line in txt: #uuid|username|address:timestamp,address:timestamp --> [uuid, username, [[address, timestamp], [address, timestamp]]]
            data = line.replace("\n", "").split("|")
            data[2] = data[2].split(",")
            for i in range(len(data[2])):
                data[2][i] = data[2][i].split(";")
            playerData[0].append(data[0])
            playerData[1].append(data[1])
            playerData[2].append(data[2])
    
    while True:
        username = input("\n\n\nUsername: ")
        if username in playerData[1]:
            position = playerData[1].index(username)
            print("UUID: " + str(playerData[0][position]))
            print("\nServers seen on:")
            for address, timestamp in playerData[2][position]:
                date = strftime('%Y-%m-%d %H:%M:%S', localtime(float(timestamp)))
                print(address + ": " + date)
        else:
            print("Player not found in database.")
