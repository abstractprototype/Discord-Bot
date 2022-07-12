import discord
from discord.ext import commands
from discord.utils import get
import json
import math
import random
import time
import asyncio


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # gambling
    # @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name="coinflip", aliases=['cf', 'flip'], help="coin flip to gamble an amount of coins")
    async def coinflip(self, ctx, amount, answer):
        jail = get(ctx.guild.roles, name="JAIL")
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        await self.open_account(ctx.author)
        me = ctx.author
        users = await self.get_bank_data()
        users["users"][str(me.id)]["coins_flipped"] += 1
        earnings = float(amount)

        temp = str(amount)
        amountT = float(temp)
        if math.isinf(amountT) or math.isnan(amountT):
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return
        elif earnings <= 0:
            await ctx.send("You are poor and homeless. Go get a job!")
            # await ctx.author.add_roles(jail)
            return

        if users["users"][str(me.id)]["wallet"] < float(amount):
            await ctx.send(f"You do not have enough money to gamble! {ctx.author.mention}")
            return
        elif str(me.id) not in users["users"]:
            await ctx.send(f"You do not have a bank account! {ctx.author.mention}")
            return

        # await ctx.send(f"```{ctx.author} Guess Heads or Tails!```")

        coins = ["Heads", "Tails"]
        choice = random.choice(coins)

        # def check(author):
        #   def inner_check(message):
        #     return message.author == ctx.author
        #   return inner_check

        # answer = await self.bot.wait_for("message",check=check(ctx.author))

        # (result,) = random.choices(["Heads","Tails"], k=1, weights=([.2,.8]
        # if users["users"][str(me.id)]["wallet"] >= 500000

        # else [.5,.5]))

        # result = answer.content if won else ("tails" if user_choice=="heads" else "heads")

        # FTW
        # if answer == "Heads":
        #   choice = "Heads"
        #   embedVar = discord.Embed(title=f'Your choice was {answer}', color=0x0000FF)
        #   embedVar.add_field(name='You picked the correct coin! You WON!', value = 'POGGERS')
        #   await ctx.send(embed=embedVar)
        #   # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
        #   # await ctx.send(embed=embedVar, delete_after=10)
        #   earnings = earnings * 2
        #   users["users"][str(me.id)]["wallet"] += earnings
        #   wallet_amount = users["users"][str(me.id)]["wallet"]
        #   await ctx.send(f"{ctx.author.mention} You have won {earnings} coins. Your new balance is: {wallet_amount} coins.")
        #   with open('bank.json', 'w') as outfile:
        #     json.dump(users, outfile, indent=2)
        #   return
        # elif answer == "Tails":
        #   choice = "Tails"
        #   embedVar = discord.Embed(title=f'Your choice was {answer}', color=0x0000FF)
        #   embedVar.add_field(name='You picked the correct coin! You WON!', value = 'POGGERS')
        #   await ctx.send(embed=embedVar)
        #   # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
        #   # await ctx.send(embed=embedVar, delete_after=10)
        #   earnings = earnings * 2
        #   users["users"][str(me.id)]["wallet"] += earnings
        #   wallet_amount = users["users"][str(me.id)]["wallet"]
        #   await ctx.send(f"{ctx.author.mention} You have won {earnings} coins. Your new balance is: {wallet_amount} coins.")
        #   with open('bank.json', 'w') as outfile:
        #     json.dump(users, outfile, indent=2)
        #   return

        try:
            R_CHANCE = .70  # 70%
            if users["users"][str(me.id)]["wallet"] >= 535586 and R_CHANCE > random.uniform(0, 1) and earnings >= 42999:
                print("GG")
                if answer == "Heads":
                    choice = "Tails"
                    embedVar = discord.Embed(
                        title=f'Your choice was {answer}', color=0xFF0000)
                    embedVar.add_field(
                        name=f"Sorry, you picked the wrong coin, the coin was {choice}.", value='RIP')
                    embedVar.add_field(
                        name=f"Your losses have been donated to Legends Bank.", value='Thank you for your charity!')
                    await ctx.send(embed=embedVar)
                    users["users"][str(me.id)]["wallet"] -= earnings
                    users["users"][str(me.id)]["coins_lost"] += earnings
                    users["legends_bank"]["balance"] += earnings
                    # embedVar.set_image(url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
                    # await ctx.send(embed=embedVar, delete_after=10)
                    wallet_amount = users["users"][str(me.id)]["wallet"]
                    await ctx.send(f"{ctx.author.mention} You have lost {amount} coins. Your new balance is: {wallet_amount} coins.")
                    with open('bank.json', 'w') as outfile:
                        json.dump(users, outfile, indent=2)
                    return
                elif answer == "Tails":
                    choice = "Heads"
                    embedVar = discord.Embed(
                        title=f'Your choice was {answer}', color=0xFF0000)
                    embedVar.add_field(
                        name=f"Sorry, you picked the wrong coin, the coin was {choice}.", value='RIP')
                    embedVar.add_field(
                        name=f"Your losses have been donated to Legends Bank.", value='Thank you for your charity!')
                    await ctx.send(embed=embedVar)
                    users["users"][str(me.id)]["wallet"] -= earnings
                    users["users"][str(me.id)]["coins_lost"] += earnings
                    users["legends_bank"]["balance"] += earnings
                    # embedVar.set_image(url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
                    # await ctx.send(embed=embedVar, delete_after=10)
                    wallet_amount = users["users"][str(me.id)]["wallet"]
                    await ctx.send(f"{ctx.author.mention} You have lost {amount} coins. Your new balance is: {wallet_amount} coins.")
                    with open('bank.json', 'w') as outfile:
                        json.dump(users, outfile, indent=2)
                    return
            else:  # play the original game + chance of daily double
                dailydouble = random.randint(1, 500)
                if answer == choice and dailydouble == 69:
                    # dailydouble = random.randint(1,50)
                    # if answer == choice and dailydouble == 25:
                    earnings = 1000000
                    embedVar = discord.Embed(
                        title='YOU HAVE WON THE DAILY DOUBLE!!!', color=(discord.Colour.random()))
                    embedVar.set_image(
                        url='https://c.tenor.com/koDbvldZ670AAAAC/cat-shocked.gif')
                    await ctx.send(embed=embedVar)
                    embedVar = discord.Embed(
                        title='YOU HAVE WON THE DAILY DOUBLE!!!', color=(discord.Colour.random()))
                    embedVar.add_field(
                        name=f'Your choice was {answer}', value='DAILY DOUBLE!!!')
                    embedVar.add_field(
                        name=f'You HAVE CHOSEN THE CORRECT COIN! AND RECEIVED {earnings} COINS!!!', value='DAILY DOUBLE!!!')
                    embedVar.set_image(
                        url='https://c.tenor.com/t5gydXmjItoAAAAC/daffy-duck-money.gif')
                    await ctx.send(embed=embedVar)
                    users["users"][str(me.id)]["wallet"] += earnings
                    wallet_amount = users["users"][str(me.id)]["wallet"]
                    await ctx.send(f"{ctx.author.mention} YOUR NEW BALANCE IS: {wallet_amount} coins!!!")
                    with open('bank.json', 'w') as outfile:
                        json.dump(users, outfile, indent=2)
                    return
                if answer == choice:
                    embedVar = discord.Embed(
                        title=f'Your choice was {answer}', color=0x0000FF)
                    embedVar.add_field(
                        name='You picked the correct coin! You WON!', value='POGGERS')
                    await ctx.send(embed=embedVar)
                    # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
                    # await ctx.send(embed=embedVar, delete_after=10)
                    earnings = earnings * 2
                    users["users"][str(me.id)]["wallet"] += earnings
                    wallet_amount = users["users"][str(me.id)]["wallet"]
                    await ctx.send(f"{ctx.author.mention} You have won {earnings} coins. Your new balance is: {wallet_amount} coins.")
                    with open('bank.json', 'w') as outfile:
                        json.dump(users, outfile, indent=2)
                    return
                else:
                    embedVar = discord.Embed(
                        title=f'Your choice was {answer}', color=0xFF0000)
                    embedVar.add_field(
                        name=f"Sorry, you picked the wrong coin, the coin was {choice}.", value='RIP')
                    embedVar.add_field(
                        name=f"Your losses have been donated to Legends Bank.", value='Thank you for your charity!')
                    await ctx.send(embed=embedVar)
                    users["users"][str(me.id)]["wallet"] -= earnings
                    users["users"][str(me.id)]["coins_lost"] += earnings
                    users["legends_bank"]["balance"] += earnings
                    # embedVar.set_image(url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
                    # await ctx.send(embed=embedVar, delete_after=10)
                    wallet_amount = users["users"][str(me.id)]["wallet"]
                    await ctx.send(f"{ctx.author.mention} You have lost {amount} coins. Your new balance is: {wallet_amount} coins.")
                    with open('bank.json', 'w') as outfile:
                        json.dump(users, outfile, indent=2)
                    return
        except:
            await ctx.send("An error has occured! Please try again.")

    # gambling with someone else
    # @commands.cooldown(1, 3600, commands.BucketType.user)
    # @commands.has_any_role("Moderator ⚔️")
    @commands.command(name="bet", help="bet an amount of coins with someone else")
    async def bet(self, ctx, user: discord.Member, amount):
        jail = get(ctx.guild.roles, name="JAIL")
        channel = self.bot.get_channel(
            803383587176972358)  # Shadow Realm's channel id
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        await self.open_account(ctx.author)
        me = ctx.author
        bankData = await self.get_bank_data()
        authorCoins = float(amount)
        userCoins = float(amount)

        temp = str(amount)
        amountT = float(temp)
        if math.isinf(amountT) or math.isnan(amountT):
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            await ctx.author.edit(voice_channel=channel)
            return
        elif float(amount) < 0:
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            await ctx.author.edit(voice_channel=channel)
            return
        elif user == ctx.author:
            await ctx.send("You can't play with yourself you fucking dumb bitch!")
            await ctx.author.add_roles(jail)
            await ctx.author.edit(voice_channel=channel)
            return

        if bankData["users"][str(me.id)]["wallet"] < float(amount):
            await ctx.send("You do not have enough money to gamble!")
            return
        elif bankData["users"][str(user.id)]["wallet"] < float(amount):
            await ctx.send(f"{user.mention} does not have enough money to gamble!")
            return
        elif str(me.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        elif str(user.id) not in bankData["users"]:
            await ctx.send(f"{user.mention} does not have a bank account!")
            return

        await ctx.send(f"{ctx.author.mention}```Coin Battle: Guess Heads or Tails! Type No to cancel game.```")
        await ctx.send(f"{user.mention}```Coin Battle: Guess Heads or Tails! Type No to cancel game.```")

        numbers = ["Heads", "Tails"]
        choice = random.choice(numbers)

        def check(author):
            def inner_check(message):
                return message.author == ctx.author
            return inner_check

        try:
            # check author answer if heads or tails
            authorAnswer = await self.bot.wait_for("message", check=check(ctx.author), timeout=60)
            # check user answer if heads or tails
            userAnswer = await self.bot.wait_for("message", check=lambda message: message.author == user and message.channel == ctx.channel, timeout=60)

            # Type No or no to cancel the game
            if authorAnswer.content == 'No' or authorAnswer.content == 'no':
                await ctx.send(f"{ctx.author.mention} has cancelled the game!")
                return
            elif userAnswer.content == 'No' or userAnswer.content == 'no':
                await ctx.send(f"{user.mention} has cancelled the game!")
                return

            # AUTHOR WINS
            if authorAnswer.content == choice and userAnswer.content != choice:
                # embedVar = discord.Embed(title=f'Your choice was {answer.content}', color=0x0000FF)
                # embedVar.add_field(name='You picked the correct number! You WON!', value = 'Poggers')
                # await ctx.send(embed=embedVar)
                # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
                # await ctx.send(embed=embedVar, delete_after=10)
                totalCoins = authorCoins + userCoins
                bankData["users"][str(me.id)]["wallet"] += authorCoins
                bankData["users"][str(user.id)]["wallet"] -= authorCoins
                bankData["users"][str(user.id)]["coins_lost"] += authorCoins
                await ctx.send(f"The coin was {choice}! {ctx.author.mention} has beat {user.mention} and won {totalCoins} coins!")
                with open('bank.json', 'w') as outfile:
                    json.dump(bankData, outfile, indent=2)
                return
            # USER WINS
            elif authorAnswer.content != choice and userAnswer.content == choice:
                # embedVar = discord.Embed(title=f'Your choice was {answer.content}', color=0x0000FF)
                # embedVar.add_field(name='You picked the correct number! You WON!', value = 'Poggers')
                # await ctx.send(embed=embedVar)
                # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
                # await ctx.send(embed=embedVar, delete_after=10)
                totalCoins = authorCoins + userCoins
                bankData["users"][str(me.id)]["wallet"] -= authorCoins
                bankData["users"][str(user.id)]["wallet"] += authorCoins
                bankData["users"][str(me.id)]["coins_lost"] += authorCoins
                await ctx.send(f"The coin was {choice}! {user.mention} has beat {ctx.author.mention} and won {totalCoins} coins!")
                with open('bank.json', 'w') as outfile:
                    json.dump(bankData, outfile, indent=2)
                return
            # IF BOTH ANSWERS NOT CORRECT OR BOTH THE SAME
            else:
                # embedVar = discord.Embed(title=f'Your choice was {answer.content}', color=0xFF0000)
                # embedVar.add_field(name=f"Sorry, you picked the wrong coin, the coin was {choice}", value = 'RIP')
                # await ctx.send(embed=embedVar)
                await ctx.send(f"The choice was {choice} It is a tie! Thank you for playing!")
                return
                # embedVar.set_image(url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
                # await ctx.send(embed=embedVar, delete_after=10)
                # with open('bank.json', 'w') as outfile:
                #   json.dump(users, outfile, indent=2)

        except asyncio.TimeoutError:
            await ctx.send(f"Game has timed out! Please try again next time.")
            return

#####################################################################################################################

    # Slots machine
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="slots", aliases=['s', 'slot'], help="Play SLOT MACHINE with legend coins!")
    async def slots(self, ctx):
        jail = get(ctx.guild.roles, name="JAIL")
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        amount = 100
        earnings = float(amount)
        me = ctx.author
        MIN, MAX = 10, 500
        randomAmount = random.randint(MIN, MAX)

        temp = str(amount)
        amountT = float(temp)
        if math.isinf(amountT) or math.isnan(amountT):
            await ctx.send("Fuck off Bitch.")
            await ctx.author.add_roles(jail)
            return
        elif earnings < 100:
            await ctx.send("This game requires 100 Legend coins!")
            # await ctx.author.add_roles(jail)
            return

        if users["users"][str(me.id)]["wallet"] < earnings:
            await ctx.send(f"You do not have enough money to gamble! {ctx.author.mention}")
            return
        elif str(me.id) not in users["users"]:
            await ctx.send(f"You do not have a bank account! {ctx.author.mention}")
            return

        users["users"][str(me.id)]["wallet"] -= earnings
        users["legends_bank"]["balance"] += earnings
        await ctx.send(f"You paid {earnings} LC \nGood Luck!")
        numbers = ["Dragon", "Tiger", "Rat", "Ox", "Rabbit", "Snake", "Horse", "Goat",
                   "Monkey", "Rooster", "Dog", "Pig", "X", "Chiyu", "Quan", "Defective", "Krezna"]
        choice1 = random.choice(numbers)
        choice2 = random.choice(numbers)
        choice3 = random.choice(numbers)
        # choice4 = random.choice(numbers)
        # choice5 = random.choice(numbers)
        # choice6 = random.choice(numbers)
        # choice7 = random.choice(numbers)
        # choice8 = random.choice(numbers)
        # choice9 = random.choice(numbers)

        # A B C
        await ctx.send(f"```Welcome to Legendary Slots!```")
        time.sleep(0.3)
        await ctx.send(f"```{choice1}```")
        time.sleep(0.5)
        await ctx.send(f"```{choice2}```")
        time.sleep(0.8)
        await ctx.send(f"```{choice3}```")
        await ctx.send(f"Thank you for playing! {ctx.author}")

        dailydouble = random.randint(1, 100)
        if dailydouble == 50:
            dailydouble = random.randint(1, 100)
            if dailydouble == 25:
                earnings = 1000000
                embedVar = discord.Embed(
                    title='YOU HAVE WON THE DAILY DOUBLE!!!', color=(discord.Colour.random()))
                embedVar.set_image(
                    url='https://c.tenor.com/koDbvldZ670AAAAC/cat-shocked.gif')
                await ctx.send(embed=embedVar)
                embedVar = discord.Embed(
                    title='YOU HAVE WON THE DAILY DOUBLE!!!', color=(discord.Colour.random()))
                embedVar.add_field(
                    name=f'CONGRATULATIONS! YOU RECEIVED {earnings} COINS!!!', value='DAILY DOUBLE!!!')
                embedVar.set_image(
                    url='https://c.tenor.com/t5gydXmjItoAAAAC/daffy-duck-money.gif')
                await ctx.send(embed=embedVar)
                users["users"][str(me.id)]["wallet"] += earnings
                wallet_amount = users["users"][str(me.id)]["wallet"]
                await ctx.send(f"{ctx.author.mention} YOUR NEW BALANCE IS: {wallet_amount} coins!!!")
                with open('bank.json', 'w') as outfile:
                    json.dump(users, outfile, indent=2)
                return

        if choice1 == choice2 == choice3:
            # embedVar = discord.Embed(title=f'Your choice was {answer.content}', color=0x0000FF)
            # embedVar.add_field(name='You picked the correct coin! You WON!', value = 'POGGERS')
            # await ctx.send(embed=embedVar)
            # embedVar.set_image(url='https://c.tenor.com/TY_AmszVhJIAAAAC/oh-yeah-high-kick.gif')
            # await ctx.send(embed=embedVar, delete_after=10)
            earnings += 777
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} YOU HIT THE 3 COMBO JACKPOT! You have won {earnings} coins! Your new balance is: {wallet_amount}.")
            return
        elif choice1 == choice2:
            earnings += 200
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} You rolled a COMBO! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice2 == choice3:
            earnings += 200
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} Amazing you got a COMBO! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice1 == choice3:
            earnings += 200
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} Nice you got a COMBO! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice2 == "Dragon":
            earnings = randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} Discovered a Hidden Dragon! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice2 == "Tiger":
            earnings = randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} Spotted a Crouching Tiger! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice1 == "Dragon" and choice2 == "Dragon":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} NICE YOU GOT A HIDDEN DRAGON AND 2 COMBOS! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice2 == "Dragon" and choice3 == "Dragon":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} NICE YOU GOT A HIDDEN DRAGON AND 2 COMBOS! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice1 == "Tiger" and choice2 == "Tiger":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} CONGRATS YOU GOT A HIDDEN TIGER AND 2 COMBOS! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice2 == "Tiger" and choice3 == "Tiger":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} CONGRATS YOU GOT a HIDDEN TIGER AND 2 COMBOS! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice1 == "Tiger" and choice3 == "Tiger":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} CROUCHING TIGER PROVOKED! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        elif choice1 == "Dragon" and choice3 == "Dragon":
            earnings += randomAmount
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.win(me, earnings)
            await ctx.send(f"{me.mention} HIDDEN DRAGON AWAKENED! You have won {earnings} coins! Your new balance is: {wallet_amount} coins.")
            return
        else:
            wallet_amount = users["users"][str(me.id)]["wallet"]
            await self.lose(me, earnings)
            await ctx.send(f"{me.mention} No COMBOS! Nice try. All loses have been donated to Legends Bank. Your new balance is: {wallet_amount} coins.")
            return

##################################################################################################################################################

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="enter_evergaol", help="Pay 200 legend coins to enter evergaol")
    async def enter_evergaol(self, ctx):
        bankData = await self.get_bank_data()
        visitinghours = get(ctx.guild.roles, name="Visiting Hours")
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        fee = 200
        if bankData["users"][str(ctx.author.id)]["wallet"] < fee:
            await ctx.send("You do not have enough money!")
            return
        elif str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] -= fee
            await ctx.author.add_roles(visitinghours)
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            embedVar.set_image(
                url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
            await ctx.send(embed=embedVar)
            await ctx.send(f"Thank you for payment, enjoy your time in Evergaol! You have paid {fee} coins! Your new balance is {wallet_amount}.")

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name="escape_evergaol", help="Pay 1 million legend coins to escape evergaol")
    async def escape_evergaol(self, ctx):
        bankData = await self.get_bank_data()
        tarnished = get(ctx.guild.roles, name="TARNISHED")
        embedVar = discord.Embed(
            color=(discord.Colour.random()),
        )
        fee = 1000000
        if bankData["users"][str(ctx.author.id)]["wallet"] < fee:
            await ctx.send("You do not have enough money!")
            return
        elif str(ctx.author.id) not in bankData["users"]:
            await ctx.send("You do not have a bank account!")
            return
        else:
            bankData["users"][str(ctx.author.id)]["wallet"] -= fee
            await ctx.author.remove_roles(tarnished)
            wallet_amount = bankData["users"][str(ctx.author.id)]["wallet"]
            with open('bank.json', 'w') as outfile:
                json.dump(bankData, outfile, indent=2)
            # embedVar.set_image(url='https://c.tenor.com/ji7VSL5s1-0AAAAd/lilnasx-nas.gif')
            # await ctx.send(embed=embedVar)
            await ctx.send(f"Thank you for payment, you are now free from Evergaol! You have paid {fee} coins! Your new balance is {wallet_amount}.")

####################################################################################################################################################

    async def win(self, me, earnings):
        print("win")
        users = await self.get_bank_data()
        users["users"][str(me.id)]["wallet"] += earnings
        with open('bank.json', 'w') as outfile:
            users = json.dump(users, outfile, indent=2)
        return users

    async def lose(self, me, earnings):
        print("lose")
        users = await self.get_bank_data()
        users["users"][str(me.id)]["wallet"] -= earnings
        with open('bank.json', 'w') as outfile:
            users = json.dump(users, outfile, indent=2)
        return users

    async def open_account(self, user):
        users = await self.get_bank_data()
        if str(user.id) in users["users"]:
            return False
        else:
            users["users"][str(user.id)] = {"name": user.name, "wallet": 0}
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

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send('**:x: | You must be a moderator to use this! | **:x:')
