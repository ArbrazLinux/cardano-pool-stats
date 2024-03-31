# INSTALLATION

+ clone this repository to whatever folder on your cardano-node running machine
+ create database into MySQL using file createDB.sql

# Configuration

+ open config.sh and edit it with your credentials "POOL TICKER", "POOL ID" (bech32 format), "REGISTRATION EPOCH"
+ get a BlockFrost.io ID and source it in $HOME/.bashrc
+ open initDB.py and edit it with your credentials "HOST", "PORT", "USER", "PASSWORD"
+ do as well with file updateDB.py

# Initialization

+ in a terminal, run ./initData.sh
+ initialization process comes through 4 steps :
  1. get list of delegators from start for each epoch
  2. check incoming, outgoing and comingback delegators -- organize a useable index
  3. retrieve pool data history and data history for each delegators -- write data into a readable JSON file
  4. load data into MySQL database
 
