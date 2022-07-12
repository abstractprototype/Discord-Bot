import discord
from discord.ext import tasks, commands
from discord.utils import get
import json


class Reward(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Claim rewards command after winning wordle
    # @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="wordle_reward", help="Claim your legend coins reward for winning Wordle")
    @commands.has_role('WON WORDLE')
    async def wordle_reward(self, ctx):
        role = get(ctx.guild.roles, name="WON WORDLE")
        bankData = await self.get_bank_data()
        coins = 200
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] += coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            await ctx.send(f"Congrats on winning Wordle! You have received {coins} coins as a reward! Your new balance is {wallet_amount}")
            await ctx.author.remove_roles(role)

    # Claim rewards command after beating Radahn
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="radahn_reward", help="Claim your legend coins reward for beating Radahn")
    @commands.has_role("Radahn's Great Rune")
    async def radahn_reward(self, ctx):
        role = get(ctx.guild.roles, name="Radahn's Great Rune")
        bankData = await self.get_bank_data()
        coins = 1000
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] += coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            await ctx.send(f"You have felled the legendary Radahn! GOOD JOB! You have received {coins} coins as a reward! Your new balance is {wallet_amount}")
            await ctx.author.remove_roles(role)

    # Claim game night rewards
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="game_reward", help="Claim game night reward!")
    @commands.has_role("GAME NIGHT WINNER")
    async def game_reward(self, ctx):
        role = get(ctx.guild.roles, name="GAME NIGHT WINNER")
        bankData = await self.get_bank_data()
        coins = 6969
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] += coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            await ctx.send(f"CONGRATS ON WINNING GAME NIGHT! You have received {coins} coins as a reward! Your new balance is {wallet_amount}")
            await ctx.author.remove_roles(role)

    # Claim Pride Month Rewards
    @commands.cooldown(1, 2.628e+6, commands.BucketType.user)
    @commands.command(name="happy_pride_month", help="Claim Pride Month reward!")
    @commands.has_role("Happy Pride Month 2022")
    async def happy_pride_month(self, ctx):
        role = get(ctx.guild.roles, name="Happy Pride Month 2022")
        bankData = await self.get_bank_data()
        coins = 6969
        if str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] += coins
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            await ctx.send(f"Happy Pride Month for 2022! You have received {coins} coins as a reward! Your new balance is {wallet_amount}")
            # await ctx.author.remove_roles(role)

##################################################################################################################

    # @tasks.loop(seconds=5)
    @commands.command(name="reset", help="resets WON WORDLE role")
    @commands.has_any_role('Bot Developer', 'Game Master')
    async def reset(self, ctx, role: discord.Role):
        wordle = get(ctx.guild.roles, name="WON WORDLE")
        for person in role.members:  # for everyone in won wordle role, remove won wordle from them
            await person.remove_roles(wordle)
            await ctx.send(f"Resetted {person}'s role")

        # for member in ctx.guild.members:
        #   if role in member.roles:
        #     await member.remove_roles(role)
        #     print(member)

    @commands.command(name="resetr", help="resets Radahn's Great Rune role")
    @commands.has_any_role('Bot Developer', 'Game Master')
    async def resetr(self, ctx, role: discord.Role):
        radahn = get(ctx.guild.roles, name="Radahn's Great Rune")
        for person in role.members:
            await person.remove_roles(radahn)
            await ctx.send(f"Resetted {person}'s role")

    @commands.command(name="resetv", help="resets Visiting Hours role")
    @commands.has_any_role('Bot Developer', 'Game Master')
    async def resetv(self, ctx, role: discord.Role):
        visitinghours = get(ctx.guild.roles, name="Visiting Hours")
        for person in role.members:
            await person.remove_roles(visitinghours)
            await ctx.send(f"Resetted {person}'s role")


################################################################################################################################

    async def open_account(self, user):
        bankData = await self.get_bank_data()
        if str(user.id) in bankData["users"]:
            return False
        else:
            bankData["users"][str(user.id)] = {"name": user.name, "wallet": 0}
            # users["users"][str(user.id)]["name"] = user.name
            # users["users"][str(user.id)]["wallet"] = 0
            # users[str(user.id)]["bank"] = 0
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            return True
        print(bankData["users"])

    async def get_bank_data(self):
        with open('bank.json', 'r') as infile:
            users = json.load(infile)
        return users

#############################################################################################################################

    @wordle_reward.error
    async def wordle_reward_error(self, ctx, error):
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send('**:x: | You must win a Wordle game to receive a reward! | **:x:')

    @radahn_reward.error
    async def radahn_reward_error(self, ctx, error):
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send('**:x: | You must defeat General Radahn to use this spell! | **:x:')
