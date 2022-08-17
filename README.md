# mc-tracker
This program scans all Minecraft servers from a text file and logs data from all online players. It saves UUIDs of players along with their usernames, addresses of the servers they have been detected on, and timestamps from when they were detected on the server. After it finishes going through the list of addresses, it repeats the process, updating any usernames that don't match their UUID (in case a player changes their username), and updating the timestamps of servers they have been on before, to keep data of when they were last online. The data is formatted as UUID|Username|Address;Timestamp,Address;Timestamp,etc. and stored in /mc-data/input.txt.

#### Installation:
- Clone the project
- Run `pip install -r requirements.txt`
