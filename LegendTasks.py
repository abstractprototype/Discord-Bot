import discord
from discord.ext import commands
from discord.utils import get
import random
import json
import math

descendgifs = [
    'https://c.tenor.com/NZGPXGO1_bQAAAAC/straight-to-jail-crime.gif',
    'https://c.tenor.com/T5FwpeRjmFgAAAAC/falling.gif',
    'https://c.tenor.com/X1UBzspDL3kAAAAC/burn-in-hell-elmo.gif'
]


class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

       # number guessing game
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name="plunder", help="plunder an amount of legend coins from user")
    async def plunder(self, ctx, user: discord.Member, amount):
        role = get(user.guild.roles, name="JAIL")
        banish = get(user.guild.roles, name="TARNISHED")
        channel = self.bot.get_channel(
            803383587176972358)  # Shadow Realm's channel id
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        await self.open_account(ctx.author)
        me = ctx.author
        users = await self.get_bank_data()
        loot = random.randrange(1, 10)
        bankloot = random.randrange(1, 100)
        ROB_BANK_CHANCE = random.randint(1, 3)

        # if author already has the jail or tarnished role and tries to steal
        if role in me.roles:
            embedVar.set_image(
                url='https://c.tenor.com/lJGud7tZVj8AAAAM/episode37-saikou.gif')
            await ctx.send(embed=embedVar)
            await ctx.send("You have been banished to evergaol for commiting crimes in hell.")
            await ctx.author.add_roles(banish)
            return

        # if user attempts to rob the bank
        if user.bot and (ROB_BANK_CHANCE == 1 or ROB_BANK_CHANCE == 2):
            embedVar.set_image(
                url='https://c.tenor.com/eaAbCBZy0PoAAAAC/reverse-nozumi.gif')
            await ctx.send(embed=embedVar)
            await ctx.send(f"Nice try bozo {ctx.author.mention}, you failed to rob Legends Bank")
            await ctx.author.add_roles(role)
            await ctx.author.edit(voice_channel=channel)
            return
        elif user.bot and ROB_BANK_CHANCE == 3:
            embedVar.set_image(
                url='https://c.tenor.com/khLn9wuWeOkAAAAC/spongebob-meme.gif')
            await ctx.send(embed=embedVar)
            users["users"][str(me.id)]["wallet"] += bankloot
            users["users"][str(me.id)]["coins_stolen"] += bankloot
            users["legends_bank"]["balance"] -= bankloot
            await ctx.send(f"You have stolen {bankloot} coins from Legends Bank!")
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)
            return

        # if the target user has no money then return
        if users["users"][str(user.id)]["wallet"] < loot:
            await ctx.send("This person is poor and homeless. Please do not bother them. Instead of robbing them, you walk away peacefully.")
            return

        # start the normal game
        await ctx.send("```Guess the number 1 or 2!```")
        numbers = ["1", "2"]
        choice = random.choice(numbers)

        def check(author):
            def inner_check(message):
                return message.author == ctx.author
            return inner_check

        answer = await self.bot.wait_for("message", check=check(ctx.author))

        if answer.content == choice:
            embedVar = discord.Embed(color=0x0000FF)
            embedVar.set_image(
                url='https://c.tenor.com/nPgdqRftJ9kAAAAC/scary-meme.gif')
            await ctx.send(embed=embedVar)
            users["users"][str(me.id)]["wallet"] += loot
            users["users"][str(me.id)]["coins_stolen"] += loot
            users["users"][str(user.id)]["wallet"] -= loot
            await ctx.send(f"You have stolen {loot} coins from {user.mention}!")
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)
        else:
            embedVar = discord.Embed(color=0xFF0000)
            embedVar.set_image(
                url='https://c.tenor.com/_YqdfwYLiQ4AAAAd/traffic-fbi-open-up.gif')
            await ctx.send(embed=embedVar)
            await ctx.send(f"{ctx.author.mention} got caught stealing and was sent to Jail!")
            await ctx.author.add_roles(role)
            await ctx.author.edit(voice_channel=channel)

    # Pay legend coins to steal a random role from someone
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="swipe", help="Pay 500k legend coins to ?")
    async def swipe(self, ctx, user: discord.Member):
        role = random.choice(user.roles)  # grabs all the roles of a user
        bankData = await self.get_bank_data()
        coins = 500000
        embed = discord.Embed(
            color=(discord.Colour.random()),
        )
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] -= coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            embed.set_image(
                url='https://c.tenor.com/ufH8TS7dO_cAAAAC/dat-yoink.gif')
            await ctx.send(embed=embed)
            await ctx.send(f"Swiped {role} from {user.mention}! Your new balance is {wallet_amount}")
            await user.remove_roles(role)
            await ctx.author.add_roles(role)
        # for role in user.roles:
        #   if role.name != "@everyone":
        #     embed.set_image(url='https://c.tenor.com/ufH8TS7dO_cAAAAC/dat-yoink.gif')
        #     await ctx.send(embed = embed)
        #     await ctx.send(f"Yoinked {role} from {user.mention}!")
        #     await user.remove_roles(role)
        #     await ctx.author.add_roles(role)

        # if role not in user.roles:
        #   await ctx.send("This person does not have the role!")
        #   return

    # Pay legend coins to send user to jail

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="execute", help="Pay 1 million legend coins to send someone to jail")
    async def execute(self, ctx, user: discord.Member):
        role = get(ctx.guild.roles, name="JAIL")
        bankData = await self.get_bank_data()
        coins = 1000000
        embed = discord.Embed(
            color=(discord.Colour.random()),
        )
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] -= coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            embed.set_image(
                url='https://c.tenor.com/KOBtQnT0H0cAAAAd/get-rekt-boi-elmo.gif')
            await ctx.send(embed=embed)
            await ctx.send(f"You have sent {user.mention} to Jail! Your new balance is {wallet_amount}")
            await user.add_roles(role)

    @commands.command(name="show", help="shows the top 10 richest people in CSULB Legends")
    async def show(self, ctx):
        info = await self.get_bank_data()
        # sorted_items = sorted(info.items(), key=lambda x: x["wallet"])
        # sorted_list = ["Username: {} Money: {}".format(info[k]["name"], info[k]["wallet"]) for k, v in sorted_items]
        # print(sorted_list)

        # for accounts in info['users']:
        #   print(accounts)
        em = discord.Embed(
            title="Top 10 Richest people in Legends", color=(discord.Colour.random()))

        # print("wallets: ", info["users"])
        # richest = sorted(info, key=lambda k: k["users"]["wallet"])
        richest = sorted(info["users"].items(),
                         key=lambda k: k[1]["wallet"], reverse=True)

        for k, v in richest[:10]:  # <-- change to 10 if you want top 10
            ranking = ("Username: {}, \nMoney: {:,}".format(
                v["name"], v["wallet"]))
            em.add_field(name=":trophy:", value=ranking)
            # print(list(info["users"].items())[:10])
        await ctx.send(embed=em)

    @commands.command(name="donate", help="donates money to the Central Legends Bank")
    async def donate(self, ctx, amount):
        jail = get(ctx.guild.roles, name="JAIL")
        bankData = await self.get_bank_data()
        await self.open_account(ctx.author)
        me = ctx.author
        coins = float(amount)

        temp = str(amount)
        amountT = float(temp)
        if math.isinf(amountT) or math.isnan(amountT):
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return
        elif coins < 0:
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return

        if bankData["users"][str(me.id)]["wallet"] < coins:
            await ctx.send("You do not have enough money to give away!")
            return
        elif str(me.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(me.id)]["wallet"] -= coins
            legendsbank = bankData["legends_bank"]["balance"]
            bankData["legends_bank"]["balance"] += coins
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            await ctx.send(f"You donated {coins} coins to Legends Bank! The total coins inside the Legends Bank is {legendsbank}. Thank you for your donation! {me}!")

    @commands.command(name="bank", help="open bank account or check current balance")
    async def bank(self, ctx):
        # initializes an account for a user
        await self.open_account(ctx.author)
        bankData = await self.get_bank_data()
        me = ctx.author

        wallet_amount = bankData["users"][str(me.id)]["wallet"]
        coins_lost = bankData["users"][str(me.id)]["coins_lost"]
        coins_flipped = bankData["users"][str(me.id)]["coins_flipped"]
        coins_stolen = bankData["users"][str(me.id)]["coins_stolen"]
        legends_bank = bankData["legends_bank"]["balance"]
        wallet_str = "{:,}".format(wallet_amount)
        lost_str = "{:,}".format(coins_lost)
        flip_str = "{:,}".format(coins_flipped)
        coin_str = "{:,}".format(coins_stolen)
        legends_str = "{:,}".format(legends_bank)
        em = discord.Embed(
            title=f"{ctx.author.name}'s Wallet", color=(discord.Colour.random()))
        em.add_field(name="Available Legend Coins:", value=wallet_str)
        em.add_field(name="Lost coins:", value=lost_str)
        em.add_field(name="Coins flipped:", value=flip_str)
        em.add_field(name="Looted coins:", value=coin_str)
        em.add_field(name="Total Legend Coins in Legends Bank:",
                     value=legends_str)
        await ctx.send(embed=em)

    @commands.command(name="give", help="choose an amount of coins to give to someone")
    async def give(self, ctx, user: discord.Member, amount):
        jail = get(user.guild.roles, name="JAIL")
        coins = float(amount)
        me = ctx.author
        users = await self.get_bank_data()

        temp = str(amount)
        amountT = float(temp)
        if math.isinf(amountT) or math.isnan(amountT):
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return
        elif coins < 0:
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return

        if users["users"][str(me.id)]["wallet"] < coins:
            await ctx.send("You do not have enough money to give away!")
            return
        elif str(user.id) not in users["users"]:
            await ctx.send("This person does not have a bank account!")
            return
        else:
            users["users"][str(me.id)]["wallet"] -= coins
            users["users"][str(user.id)]["wallet"] += coins
            await ctx.send(f"{user.mention} has received {coins} coins!")
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)

    @commands.command(name="beg", help="receive random coins")
    async def beg(self, ctx):
        await self.open_account(ctx.author)
        me = ctx.author
        users = await self.get_bank_data()
        earnings = random.randrange(3)

        await ctx.send(f"Someone gave you {earnings} coins!")
        users["users"][str(me.id)]["wallet"] += earnings

        with open('bank.json', 'w') as outfile:
            json.dump(users, outfile, indent=2)

    # @commands.command(name="drop", help="spawns random coins in random channels")
    # async def drop(self, ctx):
    #   channels = [channel for guild in ctx.bot.guilds for channel in guild.text_channels]
    #   picked = random.choice(channels)
    #   await picked.send("Dropped some coins!")

    # number guessing game
    # @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name="steal", help="guess a number to steal someones coins")
    async def steal(self, ctx, user: discord.Member = None):
        role = get(user.guild.roles, name="JAIL")
        banish = get(user.guild.roles, name="TARNISHED")
        channel = self.bot.get_channel(
            803383587176972358)  # Shadow Realm's channel id
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        await self.open_account(ctx.author)
        me = ctx.author
        users = await self.get_bank_data()
        loot = random.randrange(1, 10)
        bankloot = random.randrange(1, 100)
        ROB_BANK_CHANCE = random.randint(1, 3)

        # if author already has the jail or tarnished role and tries to steal
        if role in me.roles:
            embedVar.set_image(
                url='https://c.tenor.com/lJGud7tZVj8AAAAM/episode37-saikou.gif')
            await ctx.send(embed=embedVar)
            await ctx.send("You have been banished to evergaol for commiting crimes in hell.")
            await ctx.author.add_roles(banish)
            return

        # if user attempts to rob the bank
        if user.bot and (ROB_BANK_CHANCE == 1 or ROB_BANK_CHANCE == 2):
            embedVar.set_image(
                url='https://c.tenor.com/eaAbCBZy0PoAAAAC/reverse-nozumi.gif')
            await ctx.send(embed=embedVar)
            await ctx.send(f"Nice try bozo {ctx.author.mention}, you failed to rob Legends Bank")
            await ctx.author.add_roles(role)
            await ctx.author.edit(voice_channel=channel)
            return
        elif user.bot and ROB_BANK_CHANCE == 3:
            embedVar.set_image(
                url='https://c.tenor.com/khLn9wuWeOkAAAAC/spongebob-meme.gif')
            await ctx.send(embed=embedVar)
            users["users"][str(me.id)]["wallet"] += bankloot
            users["users"][str(me.id)]["coins_stolen"] += bankloot
            users["legends_bank"]["balance"] -= bankloot
            await ctx.send(f"You have stolen {bankloot} coins from Legends Bank!")
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)
            return

        # if the target user has no money then return
        if users["users"][str(user.id)]["wallet"] < loot:
            await ctx.send("This person is poor and homeless. Please do not bother them. Instead of robbing them, you walk away peacefully.")
            return

        # start the normal game
        await ctx.send("```Guess the number 1 or 2!```")
        numbers = ["1", "2"]
        choice = random.choice(numbers)

        def check(author):
            def inner_check(message):
                return message.author == ctx.author
            return inner_check

        answer = await self.bot.wait_for("message", check=check(ctx.author))

        if answer.content == choice:
            embedVar = discord.Embed(color=0x0000FF)
            embedVar.set_image(
                url='https://c.tenor.com/nPgdqRftJ9kAAAAC/scary-meme.gif')
            await ctx.send(embed=embedVar)
            users["users"][str(me.id)]["wallet"] += loot
            users["users"][str(me.id)]["coins_stolen"] += loot
            users["users"][str(user.id)]["wallet"] -= loot
            await ctx.send(f"You have stolen {loot} coins from {user.mention}!")
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)
        else:
            embedVar = discord.Embed(color=0xFF0000)
            embedVar.set_image(
                url='https://c.tenor.com/_YqdfwYLiQ4AAAAd/traffic-fbi-open-up.gif')
            await ctx.send(embed=embedVar)
            await ctx.send(f"{ctx.author.mention} got caught stealing and was sent to Jail!")
            await ctx.author.add_roles(role)
            await ctx.author.edit(voice_channel=channel)

########################################################################################################################################################################

    #  # @commands.cooldown(1, 86400, commands.BucketType.user)
    # @commands.command(name="jail", help="pay 1 million coins to send someone to jail")
    # async def jail(self, ctx, user: discord.Member):
    #   role = get(user.guild.roles, name ="JAIL")
    #   channel = self.bot.get_channel(803383587176972358) #Shadow Realm's channel id
    #   embed = discord.Embed(
    #     color = (discord.Colour.random()),
    #   )
    #   await self.open_account(ctx.author)
    #   me = ctx.author
    #   users = await self.get_bank_data()
    #   fee = 1000000

    #   if users["users"][str(me.id)]["wallet"] < fee:
    #     await ctx.send("You do not have enough money!")
    #     return
    #   elif str(ctx.author.id) not in users["users"]:
    #     await ctx.send("You do not have a bank account!")
    #     return
    #   else:
    #     users["users"][str(me.id)]["wallet"] -= fee

    #   with open('bank.json', 'w') as outfile:
    #     json.dump(users, outfile, indent=2)

    #   if user.bot:
    #     embed.set_image(url='https://c.tenor.com/eaAbCBZy0PoAAAAC/reverse-nozumi.gif')
    #     await ctx.send(embed = embed)
    #     await ctx.send(f"Nice try bozo {ctx.author.mention}")
    #     await ctx.author.add_roles(role)
    #     await ctx.author.edit(voice_channel=channel)
    #     return
    #   else:
    #     embed.set_image(url=(random.choice(descendgifs)))
    #     await ctx.send(embed = embed, delete_after=10)
    #     await ctx.send(f"You sent {user.mention} to Jail!")
    #     await user.add_roles(role)
    #     await user.edit(voice_channel=channel)

    # @commands.command(name="game", help="bet an amount of coins with someone else")
    # async def game(self, ctx, user: discord.Member, amount):
    #   await ctx.send(f"{ctx.author.mention}```Coin Battle: Guess Heads or Tails!```")
    #   await ctx.send(f"{user.mention}```Coin Battle: Guess Heads or Tails!```")

    #   numbers = ["Heads", "Tails"]
    #   choice = random.choice(numbers)

    #   authorAnswer, userAnswer = await asyncio.wait([
    #     self.bot.loop.create_task(self.bot.wait_for('message')),
    #     self.bot.loop.create_task(self.bot.wait_for('message'))
    #   ], return_when=asyncio.ALL_COMPLETED)

    #   try:
    #      #AUTHOR WINS
    #     if authorAnswer.content == choice and userAnswer != choice:
    #       await ctx.send(f"{ctx.author} has beat {user.mention}")
    #     #USER WINS
    #     elif authorAnswer.content != choice and userAnswer == choice:
    #       await ctx.send(f"{user.mention} has beat {user.mention} and won coins!")

    #     #IF BOTH ANSWERS NOT CORRECT OR BOTH THE SAME
    #     else:
    #       await ctx.send(f"It is a tie! Thank you for playing!")
    #       return


################################################################################################################

    # initializes bank account for a user

    async def open_account(self, user):
        users = await self.get_bank_data()
        if str(user.id) in users["users"]:
            return False
        else:
            users["users"][str(user.id)] = {
                "name": user.name, "wallet": 0, "coins_lost": 0, "coins_flipped": 0, "coins_stolen": 0}
            # users["users"][str(user.id)]["name"] = user.name
            # users["users"][str(user.id)]["wallet"] = 0
            # users[str(user.id)]["bank"] = 0
            with open("bank.json", "w") as outfile:
                json.dump(users, outfile, indent=2)
            return True
            print(users["users"])

    # async def open_squid_bank(self):
    #   mainbank = await self.get_bank_data()
    #   mainbank["main_bank"] = {"balance": 0}
    #   with open('bank.json', 'w') as outfile:
    #     json.dump(mainbank, outfile, indent=2)
    #   return True

    # fetches the bank json
    async def get_bank_data(self):
        with open("bank.json", "r") as infile:
            users = json.load(infile)
        return users
