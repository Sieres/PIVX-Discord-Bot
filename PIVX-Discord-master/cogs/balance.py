import discord
from discord.ext import commands
from utils import rpc_module, mysql_module

#result_set = database response with parameters from query
#db_bal = nomenclature for result_set["balance"]
#snowflake = snowflake from message context, identical to user in database
#wallet_bal = nomenclature for wallet reponse

rpc = rpc_module.Rpc()
Mysql = mysql_module.Mysql()


class Balance:

    def __init__(self, bot):
        self.bot = bot
		
    # @bot.event
    # async def on_channel_create(channel):
        # channelString = str(channel)
        # if channelString.startswith("Direct Message"):
            # privateChannel = "y"

    async def do_embed(self, user, db_bal):
        # Simple embed function for displaying useruser and balance
        embed = discord.Embed()#(colour=user.top_role.colour)
        embed.add_field(name="User", value=user.mention)
        if float(db_bal) is not None:
            embed.add_field(name="Balance", value="%.8f PIV" % round(float(db_bal),8))
        else:
            embed.add_field(name="Balance", value="0 PIV")
        embed.set_footer(text="Sieres waz 'ere '17")

        try:
            #await self.bot.say(embed=embed)
            # if pirvateChannel == "y":
                # 
            # else:
            await self.bot.send_message(user, embed=embed)
         #   await self.bot.send_message(user, "Your balance is: {} PIV".format(db_bal))
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")

    async def parse_part_bal(self,result_set,snowflake,user):
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
            await self.do_embed(user, db_bal)
        else:
            for tx in reversed(get_transactions):
                if tx["txid"] == result_set["lasttxid"]:
                    break
                else:
                    new_balance += float(tx["amount"])
            db_bal = new_balance
            Mysql.update_db(snowflake, db_bal, lasttxid)
            await self.do_embed(user, db_bal)

    async def parse_whole_bal(self,snowflake,user):
        # # If a user does not have a lasttxid in the db, the parse
        # # the entire trans-list for that user. Submit changes to
        # # update_db
        count = 1000
        get_transactions = rpc.listtransactions(snowflake,count)
        i = len(get_transactions)-1
        if len(get_transactions) == 0:
            db_bal = 0
            await self.do_embed(user, db_bal)
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
            #Now update db with new balance
            Mysql.update_db(snowflake, db_bal, lasttxid)
            await self.do_embed(user, db_bal)


    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """Display your balance"""
        # Set important variables
        snowflake = ctx.message.author.id
        user = ctx.message.author

        # Check if user exists in db
        result_set = Mysql.check_for_user(user, snowflake)

        # Execute and return SQL Query
        result_set = Mysql.get_user(snowflake)
		
		#get balance
    #    db_bal = Mysql.get_bal_lasttxid(snowflake)

        if result_set["lasttxid"] in ["0",""]:
            await self.parse_whole_bal(snowflake, user)
        else:
            await self.parse_part_bal(result_set, snowflake, user)

    #    await self.do_embed(user, float(db_bal['balance']))


def setup(bot):
    bot.add_cog(Balance(bot))
