import discord
from discord.ext import commands
import random
import csv

DISCORD_BOT_CODE = ''
PREFIX = ''
MAX_ROLL = 0
MAX_MOD = 0

with open('RollerHelperVars.csv') as csvFile:
    CSVdata = csv.reader(csvFile, delimiter=',')
    for row in CSVdata:
        DISCORD_BOT_CODE = str(row[0])
        PREFIX = str(row[1])
        MAX_ROLL = int(row[2])
        MAX_MOD = int(row[3])
csvFile.close()

#Set up the bot
bot = commands.Bot(command_prefix=PREFIX, help_command=None)

@bot.event
async def on_ready():
    activity = discord.Game(name=PREFIX + 'roll | ' + PREFIX + 'help', type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready')

#Prints all of the bot's commands
@bot.command()
async def help(ctx):
    await ctx.send('>>> This bot\'s commands:\n\t' + PREFIX + 'roll \n\t\tTyping in just the command will roll a d20 \n\t\tTyping in advantage or disadvantage after the command will roll a d20 with advantage or disadvantage \n\t\tTo roll anything else, you can format it as #d# (the first number being the number of dice, the second number being the number of sides on the dice) \n\t\tYou are also able to add modifiers to this roll by either adding +# or -# to the end of the dice roll (exp. 2d4+3) \n\t' + PREFIX + 'fate\n\t\tTyping a number after this command will roll that number of fate dice\n\t\tYou are also able to add modifiers to this roll the same way you can add them to the ' + PREFIX + 'roll command')

#Main function of the bot, rolls any number of an any-sided dice
@bot.command()
async def roll(ctx, dice: str = None):
    #Base cases for dice roll, either a d20 roll or d20 at advantage or disadvantage
    if not dice: #Same as 1d20
        await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(random.randint(1,20)))
        return
    elif dice.upper() == 'ADVANTAGE': #Same as 2d20 but it only prints the highest result
        diceRollOne = random.randint(1,20)
        diceRollTwo = random.randint(1,20)
        if(diceRollOne >= diceRollTwo):
            await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(diceRollOne) + ' Rolls: ' + str(diceRollOne) + ', ' + str(diceRollTwo))
        else:
            await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(diceRollTwo) + ' Rolls: ' + str(diceRollOne) + ', ' + str(diceRollTwo))
        return
    elif dice.upper() == 'DISADVANTAGE': #Same as 2d20 but it only prints the lowest result
        diceRollOne = random.randint(1,20)
        diceRollTwo = random.randint(1,20)
        if(diceRollOne <= diceRollTwo):
            await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(diceRollOne) + ' Rolls: ' + str(diceRollOne) + ', ' + str(diceRollTwo))
        else:
            await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(diceRollTwo) + ' Rolls: ' + str(diceRollOne) + ', ' + str(diceRollTwo))
        return
    
    total = 0
    
    #Makes sure that the message is properly formatted
    try:  
        #Checks to see if the dice roll has any modifiers
        if '+' in dice:
            diceReplace = dice.replace('+', 'd')
            diceSplit = diceReplace.split('d')
            if int(diceSplit[0]) > MAX_ROLL or int(diceSplit[1]) > MAX_ROLL or int(diceSplit[2]) > MAX_MOD:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(diceSplit[0]) 
            limit = int(diceSplit[1])
            total = int(diceSplit[2])
        elif '-' in dice:
            diceReplace = dice.replace('-', 'd')
            diceSplit = diceReplace.split('d')
            if int(diceSplit[0]) > MAX_ROLL or int(diceSplit[1]) > MAX_ROLL or int(diceSplit[2]) > MAX_MOD:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(diceSplit[0]) 
            limit = int(diceSplit[1])
            total = int(diceSplit[2]) * -1
        else:
            diceSplit = dice.split('d')
            if int(diceSplit[0]) > MAX_ROLL or int(diceSplit[1]) > MAX_ROLL:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(diceSplit[0])
            limit = int(diceSplit[1])
    except Exception: 
        await ctx.send('>>> ' + ctx.author.mention + ' Use #d# formating. For more information, use the ' + PREFIX + 'help command')
        return
    
    results = ''
    
    #Each loop rolls a dice and adds the result to the total as well as saving the roll to the result to be printed 
    for r in range(rolls):
        numberRolled = random.randint(1, limit)
        total += numberRolled
        results += str(numberRolled)
        if r < (rolls - 1):
            results += ', '
    
    await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(total) + ' Rolls: ' + results)

#Rolls using the Fate dice system
@bot.command()
async def fate(ctx, dice: str = None):
    total = 0
    
    #Checks to see if the message is formatted correctly as well as if there is a modifier added 
    try:
        if '+' in dice: 
            diceSplit = dice.split('+')
            if int(diceSplit[0]) > MAX_ROLL or int(diceSplit[1]) > MAX_MOD:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(diceSplit[0])
            total = int(diceSplit[1])
        elif '-' in dice:
            diceSplit = dice.split('-')
            if int(diceSplit[0]) > MAX_ROLL or int(diceSplit[1]) > MAX_MOD:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(diceSplit[0])
            total = int(diceSplit[1]) * -1
        else:
            if int(dice) > MAX_ROLL:
                await ctx.send('>>> ' + ctx.author.mention + ' Please use a smaller number')
                return
            rolls = int(dice)
    except Exception:
        await ctx.send('>>> ' + ctx.author.mention + ' Use a whole number. For more information, us the ' + PREFIX + 'help command')
        return
    
    results = ''
    
    #Each loop rolls a dice and adds the result to the total as well as saving the roll to the result to be printed
    #It converts the number rolled to either +, -, or 0 when it is added to the return message
    for r in range(rolls):
        numberRolled = random.randint(1, 3)
        if(numberRolled == 1):
            results += '-'
            total -= 1
        elif(numberRolled == 2):
            results += '0'
        else:
            results += '+'
            total += 1
        if r < (rolls - 1):
            results += ', '
    
    #Prints the message in the correct format
    if(total > 0):
        await ctx.send('>>> ' + ctx.author.mention + ' Total: +' + str(total) + ' Rolls: ' + results)
    else:
        await ctx.send('>>> ' + ctx.author.mention + ' Total: ' + str(total) + ' Rolls: ' + results)

bot.run(DISCORD_BOT_CODE)