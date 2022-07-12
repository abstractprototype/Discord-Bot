import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio
import random
import json


class Spawn(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.scheduled_jobs.start()

    @tasks.loop(hours=3)
    async def scheduled_jobs(self):
        print("Running Scheduled Jobs")
        # SPAWN_CHANCE = 0.5
        # if SPAWN_CHANCE < random.uniform(0,1):
        await self.spawn_coins()

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="rain", help="SPECIAL ABILITY of a Dimensional Traveler. Make it rain Legend coins!")
    @commands.has_any_role('Moderator ⚔️', 'Dimensional Traveler')
    async def rain(self, ctx):
        await self.spawn_coins()

    async def spawn_coins(self):
        GUILD_NAME = "CSULB Legends"
        CHANNEL_NAMES = ["bot-commands", "office-hours", "wordle",
                         "pokemon-arceus", "epic-rpg", "waifu-gacha", "tatsu"]
        # SPAWN_CHANCE = .99
        MIN, MAX = 10, 1000  # coins amount
        TIME_LIMIT = 60
        guild = get(self.bot.guilds, name=GUILD_NAME)
        if not guild:
            return

        channels = [get(guild.text_channels, name=name)
                    for name in CHANNEL_NAMES]
        if not channels:
            return

        # if SPAWN_CHANCE < random.uniform(0,1): return

        channel = random.choice(channels)
        amount = random.randint(MIN, MAX)

        bankData = await self.get_bank_data()
        em = discord.Embed(
            color=(discord.Colour.random())
        )

        bankData["legends_bank"]["balance"] -= amount
        bank_amount = bankData["legends_bank"]["balance"]
        bank_amount_str = "{:,}".format(bank_amount)
        em.set_image(url='https://c.tenor.com/OaYYWO9efBIAAAAC/rich-money.gif')
        await channel.send(embed=em, delete_after=60)
        await channel.send(f"FREE Legend coins! First to type in {TIME_LIMIT} seconds will claim them!")
        await channel.send(f"Legends bank has remaining {bank_amount_str} coins.")

        def check(message):
            return channel.name == message.channel.name and guild.name == message.guild.name and message.author.id != self.bot.user.id

        # success = False
        # existing bug where a user with no bank account cannot collect the spawned coins
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=TIME_LIMIT)
            me = msg.author
            # await self.open_account(msg.author)
            em.set_image(
                url='https://c.tenor.com/mpogyegMpG4AAAAM/vampire-survivors-loot.gif')
            # em.set_image(url='https://c.tenor.com/R1w9qftRaP4AAAAC/your-win-prize-gift.gif')
            await channel.send(embed=em)
            await channel.send(f"{amount} coins claimed by {msg.author.name}!")
            bankData["users"][str(me.id)]["wallet"] += amount
            bankData["legends_bank"]["balance"] -= amount
            wallet_amount = bankData["users"][str(me.id)]["wallet"]
            #legends_bank = bankData["legends_bank"]["balance"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            # user_balance = self.bank_manager.deposit(str(msg.author.id), msg.author.name, float(amount))
            await channel.send(f"Success! Updated balance for {msg.author.name}: {wallet_amount} coins")
            # success = True
        except asyncio.TimeoutError:
            await channel.send(f"Too Late! The coins have ran away!")
        # except Exception as ex:
        #   await channel.send(str(ex))
        # finally:
        #   if success:
        #     self.bank_manager.commit_transaction()
        #   else:
        #     self.bank_manager.rollback_transaction()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (random.randint(0, 2000) == 42) and (message.author != self.bot.user):
            await message.channel.send("bruh")
        elif (random.randint(0, 2000) == 69) and (message.author != self.bot.user):
            await message.channel.send("ur mom")
        elif (random.randint(0, 2000) == 99) and (message.author != self.bot.user):
            await message.channel.send("awwww hellll nahhhhhhh")
        elif (random.randint(0, 2000) == 76) and (message.author != self.bot.user):
            await message.channel.send("No bitches?")
        elif (random.randint(0, 2000) == 25) and (message.author != self.bot.user):
            await message.channel.send("no.")
        elif (random.randint(0, 2000) == 56) and (message.author != self.bot.user):
            await message.channel.send("bad idea")
        else:
            return

#####################################################################################################################

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
            with open('bank.json', 'w') as outfile:
                json.dump(users, outfile, indent=2)
            return True
        print(users["users"])

    async def get_bank_data(self):
        with open('bank.json', 'r') as infile:
            users = json.load(infile)
        return users
