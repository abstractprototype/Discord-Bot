import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from SpawnCoins import Spawn
from LegendTasks import Tasks
from Rewards import Reward
from Games import Game

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='legends ',
    intents=intents,
    allowed_mentions=discord.AllowedMentions(
        everyone=False,  # Whether to ping @everyone or @here mentions
    ))
# bot.remove_command("help")
bot.add_cog(Spawn(bot))
bot.add_cog(Tasks(bot))
bot.add_cog(Reward(bot))
bot.add_cog(Game(bot))

# tracks cooldowns, user input, missing perms, error handler


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        minutes, seconds = divmod(seconds, 60)
        msg = ':exclamation: This command is on cooldown, please try again in {:.0f} minutes  :exclamation:'.format(
            minutes, seconds)
    elif isinstance(error, commands.MissingRequiredArgument):
        msg = f"Missing a required argument: {error.param}"
    elif isinstance(error, commands.MissingPermissions):
        msg = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        msg = "Something about your input was wrong, please check your input and try again!"
    # else:
    #     msg = "Oh no! Something went wrong while running the command!"
    await ctx.send(msg, delete_after=10)
    await ctx.message.delete(delay=10)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # await bot.wait_until_ready()
    # channel = bot.get_channel(951726208599597116)
    # await channel.send('Hello I am alive.')

# msg = ['msg1','msg2','msg3']

# @bot.command()
# async def test(message):
#   while True:
#     chance = random.randint(1,4)
#     print(chance)
#     if chance == 1:
#       msj = random.choice(msg)
#       await message.send(msj)
#     time = random.randint(60,3600)
#     print(time)
#     await asyncio.sleep(time)
# bot.loop.create_task(test("!test"))

keep_alive()
bot.run(os.environ['SECRET'])
