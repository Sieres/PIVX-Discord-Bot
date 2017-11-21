import discord, json, requests, pymysql.cursors
from discord.ext import commands
from utils import rpc_module, mysql_module, parsing

rpc = rpc_module.Rpc()
Mysql = mysql_module.Mysql()


class Tip:
    def __init__(self, bot):
        self.bot = bot

    async def parse_part_bal(self,result_set,snowflake,name):
        # If user has a lasttxid value in the db, then stop parsing
        # trans-list at a specific ["txid"] and submit
        # changes to update_db
        count = 1000
        get_transactions = rpc.listtransactions(snowflake,count)
        i = len(get_transactions)-1

        new_balance = float(result_set["balance"])
        lasttxid = get_transactions[i]["txid"]
        if lasttxid == result_set["lasttxid"]:
            db_bal = float(result_set["balance"])
        else:
            for tx in reversed(get_transactions):
                if tx["txid"] == result_set["lasttxid"]:
                    break
                else:
                    new_balance += float(tx["amount"])
            db_bal = new_balance
            print ("about to update the DB from partial")
            Mysql.update_db(snowflake, db_bal, lasttxid)

    async def parse_whole_bal(self,snowflake,name):
        # If a user does not have a lasttxid in the db, the parse
        # the entire trans-list for that user. Submit changes to
        # update_db
        count = 1000
        get_transactions = rpc.listtransactions(snowflake,count)
        i = len(get_transactions)-1

        if len(get_transactions) == 0:
            db_bal = 0
        else:
            new_balance = 0
            lasttxid = get_transactions[i]["txid"]
            firsttxid = get_transactions[0]["txid"]
            while i <= len(get_transactions)-1:
                if get_transactions[i]["txid"] != firsttxid:
                    new_balance += float(get_transactions[i]["amount"])
                    i -= 1
                else:
                    new_balance += float(get_transactions[i]["amount"])
                    break
            db_bal = new_balance
            print ("about to update the DB from whole")
            Mysql.update_db(snowflake, db_bal, lasttxid)
            #Now update db with new balance

    @commands.command(pass_context=True)
    async def tip(self, ctx, user:discord.Member, amount:float):
        """Tip a user coins"""
        snowflake = ctx.message.author.id
        name = ctx.message.author

        tip_user = user.id
        if snowflake == tip_user:
            await self.bot.say("{} **:warning:You cannot tip yourself!:warning:**".format(name.mention))
            return

        if amount <= 0.0:
            await self.bot.say("{} **:warning:You cannot tip <= 0!:warning:**".format(name.mention))
            return

        Mysql.check_for_user(name, snowflake)

        result_set = Mysql.get_bal_lasttxid(snowflake)
        print ("before check last tx ID")
        if result_set["lasttxid"] in ["0",""]:
            await self.parse_whole_bal(snowflake, name)
            print ("after parse whole")
        else:
            await self.parse_part_bal(result_set, snowflake, name)
            print ("after parse partial")
        if float(result_set["balance"]) < amount:
            await self.bot.say("{} **:warning:You cannot tip more money than you have!:warning:**".format(name.mention))
            return
        else:
            tip_user_addy = rpc.getaccountaddress(tip_user)
			
            remaining_blance = float(result_set["balance"]) - amount
            #do the tip - update the wallet
            print("this is the tip clog")
            
            rpc.sendfrom(snowflake, tip_user_addy, amount)
            print ("after send from")
            # elif str(rpc_response['result']) ==  "<Response [500]>":
                # await self.bot.say("An error occured during the send of this tip \n Reach out to @Sieres with this error."
                # return

            print ("tipping {}".format(str(amount)))
			#parse and update the db
            await self.parse_part_bal(result_set, snowflake, name)
            #send the notifications
            await self.bot.say("{} **tipped {} {} PIV!** :money_with_wings:".format(name.mention, user.mention, str(amount)))
            await self.bot.send_message(name,"{}, you're a great tipper! This is your remaining balance: {} PIV :money_with_wings:".format(name.mention, str(remaining_blance)))
            await self.bot.send_message(user,"{}, Just tipped you {} PIV! Be sure to thank them! :money_with_wings:".format(name.mention, str(amount)))

def setup(bot):
    bot.add_cog(Tip(bot))
