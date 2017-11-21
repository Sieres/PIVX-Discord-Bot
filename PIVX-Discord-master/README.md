# Discord-PIVX-Bot
[<img src="https://pivx.org/wp-content/uploads/2017/01/PIVX_illustrated_white.png">](https://discord.gg/F8HByx2)

#This source code is free to use & distribute under the MIT Licence.
Attributions must be kept and paid to the authors of these source files.
Authors of this source code:

Aareon of the Netcoin Community: 2016
Sieres of the PIVX Community: 2017

These files are intended to function as a multi-functional tipbot for PIVX Currency.
Use of these source files are used at your own risk, PIVX takes no accountability to lost funds / incorrect balances or anything that may occur negatively as a result of this source code.
----------------------------------------------------------

# Requirements
* discord.py installed
* Python 3.5+
* A mySQL database
* The PIVX wallet w/ RPC enabled.
----------------------------------------------------------

# Functions
* Display general wallet information
* Display individual user balances
* Store user balance information in database
* Generate new deposit addresses for users
* Automatically add users to database
* Allow users to withdraw coins from the wallet with respect to how many coins they have in the DB
* Show network data through the wallet RPC functions
----------------------------------------------------------

# DB Tables
* CREATE DATABASE crypto_db;
* CREATE TABLE db (user VARCHAR(50), snowflake VARCHAR(50), balance VARCHAR(25), staked VARCHAR(50), lasttxid VARCHAR(50));
* CREATE TABLE server (server_id VARCHAR(50), enable_soak VARCHAR(1));
* CREATE TABLE channel (channel_id VARCHAR(50), server_id VARCHAR(50), enabled VARCHAR(1));
* CREATE TABLE person (userid_pk MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (userid_pk), username VARCHAR(50), balance VARCHAR(25));
* CREATE TABLE withdrawal (userid_pk MEDIUMINT, PRIMARY KEY (userid_pk), address_from VARCHAR(50), address_to VARCHAR(50), amount VARCHAR(25));
* CREATE TABLE deposit (userid_pk MEDIUMINT, PRIMARY KEY (userid_pk), address_from VARCHAR(50), address_to VARCHAR(50), amount VARCHAR(25));
* CREATE TABLE tip (userid_from_fk MEDIUMINT, userid_to_pk MEDIUMINT, amount VARCHAR(25));
----------------------------------------------------------


# TO DO
* ISSUE: When tipping, @invalid-user is used
* ISSUE: After being tipped, DB does not update the new receiver balance
* PISSUE: IF being tipped twice and then check balance, first tip may not apply?
* DM's for Withdrawal / Balance & Deposit address - DONE
* Validation to prevent withdraws into deposit account, doubling up on balance - DONE
* Add mySQL connection pools
* Setup forever node.js
* Refactor & make more robust / error handling
* Admin commands - view all balances / view user balances / view not 0 balances
* Print Proposals list - RPC ADDED
* Print budget projction list - RPC ADDED
* Current Prices USD / BTC Etc
* Address Search - not sure if this is possible
* Support help - am i forked? Where are my zPIV / Guides
* Bootstap / Snapshot links
* Superblock - RPC ADDED
* Shout me a coffee
* Masternode list search
* Support ticketing /queuing system ##MAYBE
* Gambling - Heads / Tails ##MAYBE
* Blackjack ##MAYBE
----------------------------------------------------------

# Coffee me! If you've found this source code useful, feel free to shout me a coffee!
* BTC Address: 1MQx7rPJGPGwQL1RnC7Q3UZCC6kRpp8KTF
* PIVX Address: DE6FCHWVcPPvE2XzCs7R6ZjT64LjXUAgDY
----------------------------------------------------------
