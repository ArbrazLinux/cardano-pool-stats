# Prerequesites
+ python3.8 or above
+ pycurl
+ jq
+ bash
+ MySQL

# Installation
+ clone this repository to whatever folder on your cardano-node running machine
+ create database into MySQL using file createDB.sql

# Configuration
+ open config.py and edit it with your credentials "POOL TICKER", "POOL ID" (bech32 format), "REGISTRATION EPOCH", "OWNER ADDRESS"
+ get a BlockFrost.io ID and source it in $HOME/.bashrc
+ open initDB.py and edit it with your credentials "HOST", "PORT", "USER", "PASSWORD"
+ do as well with file updateDB.py

# Initialization
+ in a terminal, run ./init.sh
+ initialization process comes through 4 steps :
  1. get list of delegators from start for each epoch
  2. check incoming, outgoing and comingback delegators -- organize a useable index
  3. retrieve pool data history and data history for each delegators -- write data into a readable JSON file
  4. load data into MySQL database
 
+ initialization process can take few minutes to hours to complete, depending of your processor and amount of data to retrieve
+ BlockFrost queries are limited to 50000/day in free version .. there is ((Ndelegators + 1)*(N+1)blocks)*Nepoch queries .. in case you have a great number of delegators (>50), we advise to either upgrade to a paid plan, either proceed initialization in multiple steps
