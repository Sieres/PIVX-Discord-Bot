import discord, json, requests
from discord.ext import commands
from utils import rpc_module as rpc


class Wallet:
    def __init__(self, bot):
        self.bot = bot
        self.rpc = rpc.Rpc()

    @commands.command()
    async def stats(self):
        """Shows wallet info"""
        get_info = self.rpc.getinfo()
        get_block_chain_info = self.rpc.getblockchaininfo()
        connection_count = self.rpc.getconnectioncount()
        block_height = get_info["blocks"]
        block_hash = get_block_chain_info["bestblockhash"]
        stake_difficulty = float(get_info["difficulty"])
        money_supply = float(get_info["moneysupply"])
        zerocoin_supply = get_info["zPIVsupply"]["total"]
        zc1 = get_info["zPIVsupply"]["1"]
        zc5 = get_info["zPIVsupply"]["5"]
        zc10 = get_info["zPIVsupply"]["10"]
        zc50 = get_info["zPIVsupply"]["50"]
        zc100 = get_info["zPIVsupply"]["100"]
        zc500 = get_info["zPIVsupply"]["500"]
        zc1000 = get_info["zPIVsupply"]["1000"]
        zc5000 = get_info["zPIVsupply"]["5000"]
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name="Last Block", value=block_height)
        embed.add_field(name="Last Block Hash", value=block_hash)
        embed.add_field(name="Network Difficulty", value=stake_difficulty)
        embed.add_field(name="Total Money Supply", value=money_supply)
        embed.add_field(name="Total Zerocoin Available", value=zerocoin_supply)
        embed.add_field(name="Total 1 Denomination", value=zc1)
        embed.add_field(name="Total 5 Denomination", value=zc5)
        embed.add_field(name="Total 10 Denomination", value=zc10)
        embed.add_field(name="Total 50 Denomination", value=zc50)
        embed.add_field(name="Total 100 Denomination", value=zc100)
        embed.add_field(name="Total 500 Denomination", value=zc500)
        embed.add_field(name="Total 1000 Denomination", value=zc1000)
        embed.add_field(name="Total 5000 Denomination", value=zc5000)
        embed.set_footer(text="PIVX Wallet Information")

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")
		
def setup(bot):
    bot.add_cog(Wallet(bot))

