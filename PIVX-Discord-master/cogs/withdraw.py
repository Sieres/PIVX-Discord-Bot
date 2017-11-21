import discord, json, requests, pymysql.cursors, random
from discord.ext import commands
from utils import rpc_module, mysql_module, parsing
import decimal

rpc = rpc_module.Rpc()
Mysql = mysql_module.Mysql()
#scPhrases = tipbot_phrases.TBPhrases()

class Withdraw:

    def __init__(self, bot):
        self.bot = bot

    def phrases(self):
        phrase1 = "You must construct additional Pylons"
        phrase2 = "You require more vespene gas"
        phrase3 = "Not enough Minerals"
 
        all_phrases = [phrase1, phrase3, phrase2]
        return (random.choice(all_phrases))

    @commands.command(pass_context=True)
    async def withdraw(self, ctx, address:str , amount:float):

        phrase = self.phrases()
        """Withdraw coins from your account to any PIVX address"""
        snowflake = ctx.message.author.id
        user = ctx.message.author
        amount = abs(amount)
		#check if withdrawing to yourself
        user_addy = rpc.getaccountaddress(snowflake)
        if user_addy == address:
            await self.bot.send_message(user, "Why would you want to withdraw to yourself? It's only wasting PIV on TX fees so I won't let you do it.")
            return
		#getaddresses by account 
		#check is address is in that list
		#https://stackoverflow.com/questions/8214932/how-to-check-if-a-value-exists-in-a-dictionary-python
		
        if abs(decimal.Decimal(str(amount)).as_tuple().exponent) > 8:
            await self.bot.send_message(user, ":warning:**Invalid amount!**:warning:")
            return
        to_send_to_user = round(amount,8)
        print ("3")
        Mysql.check_for_user(user, snowflake)
        result_set = Mysql.get_bal_lasttxid(snowflake)
		#check if its a valid address
        conf = rpc.validateaddress(address)
        if not conf["isvalid"]:
            await self.bot.send_message(user, "{} **:warning:Invalid address!:warning:**".format(ctx.message.author.mention)) #await
            return
        print("OK address")
		
        db_bal = result_set
		#check if user has enough in balance
        if float(db_bal['balance']) < to_send_to_user:
            await self.bot.send_message(user, "{} **:warning:{}:warning: \n \t\t\t\t\t\t\t\t\t\t :warning:Not enough funds to withdraw!:warning:**".format(ctx.message.author.mention, phrase))
            return
        print("balance is ok")
		
		#check if user is withdrawing 0
        if to_send_to_user == 0.0:
            await self.bot.send_message(user, "{} **:interrobang::interrobang: Why would you try withdraw 0?:interrobang::interrobang:**".format(ctx.message.author.mention))
            return
        print("not withdrawing 0")

        #incorporate tx costs
        to_send_to_user = round(to_send_to_user, 8) - .001
		
        finalBalance = round(float(db_bal['balance']) - (to_send_to_user + .001),8)
        print(user, ": DB Balance: ", finalBalance, " Sending to user: ", to_send_to_user)
        rpc.sendtoaddress(address, to_send_to_user)
        
		#get last transaction ID for DB Update
        count = 1000
        get_transactions = rpc.listtransactions(snowflake,count)
        i = len(get_transactions)-1
        lasttxid = get_transactions[i]["txid"]
        Mysql.update_db(str(snowflake), str(finalBalance), str(lasttxid))
        await self.bot.send_message(user, "{} **withdrew {} PIV, Fee: 0.001 PIV! :money_with_wings:**\n {} PIV Remaining.".format(user.mention, str(to_send_to_user), str(finalBalance))) #await

def setup(bot):
    bot.add_cog(Withdraw(bot))
