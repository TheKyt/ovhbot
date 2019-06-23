import discord
import json
import os
import difflib
import asyncio
import re
import math
from discord.ext import commands
from discord.ext.commands import ConversionError
from difflib import SequenceMatcher

#with open("prefixes.json") as f:
#    prefixes = json.load(f)

left = '⏪'
right = '⏩'

#OPEN PREFIX FILE
with open('prefixes.json') as server_prefix:
	oldprefixdata = json.load(server_prefix)
default_prefix = "$"

#SEARCH FOR SERVER PREFIX
def prefix(bot, message):
	id = message.guild.id
	print(id)
	print(oldprefixdata.get(str(id), default_prefix))
	return oldprefixdata.get(str(id), default_prefix)

client = commands.Bot(command_prefix=prefix, case_insensitive=True)
#client = commands.Bot(command_prefix = '.')
client.remove_command('help')

#OPEN DATABASE FOR HERO
with open('db.json') as hero_db:
	data = json.load(hero_db)

#KNOW WHEN BOT IS START UP
@client.event
async def on_ready():
	print('Bot is ready.')

'''
#COMMAND ERROR
@client.event
async def on_command_error(ctx, error):
	x = ""
	if isinstance(error, commands.BadArgument):
		print("bad argument")
	elif isinstance(error, Exception):
		x = str(error).upper().split()
		if "ValueError:".upper() in x:
			embedInvalid = discord.Embed(title="Command cancelled. You did not type a number.", color=0xee2002)
		elif "TimedoutError:".upper() in x:
			embedInvalid = discord.Embed(title="Command cancelled. User timeout.".format(oldprefixdata.get(str(ctx.guild.id))), color=0xee2002)
		#elif "Argument".upper() in x.upper():
		else:
			embedInvalid = discord.Embed(title="Command Error. Type *{}help* for help.".format(oldprefixdata.get(str(ctx.guild.id))), color=0xee2002)
		print("exception")
		print(x)
		print(str(error))
		await ctx.send(embed=embedInvalid)
	else:
		print("idk")
		embedInvalid = discord.Embed(title="Command Error. Type *{}help* for help.".format(oldprefixdata.get(str(ctx.guild.id))), color=0xee2002)
'''


#HELP COMMAND
@client.command()
async def help(ctx):
	await ctx.send('```\nCommands:\n\nhero (e.g. {prefix}hero young gleck)\ngrimoire (e.g. {prefix}grimoire ludmila)\nprefix (change prefix)\nleader (e.g. {prefix}leader)\ncredits\n\nAbbreviations:\nhr (hero)\ngr (grimoire)\nldr (leader)\n```')

#PREFIX CHANGE
#ctx.guild.id in a command or message.guild.id in an event
@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, *, prefixsymbol):
	print(ctx.guild.id)
	#if ctx.message.author.guild_permissions.manage_server:
	newSymbol = {str(ctx.guild.id): str(prefixsymbol)}
	oldprefixdata.update(newSymbol)
	with open('prefixes.json', 'w') as someData:
		json.dump(oldprefixdata, someData)
	await ctx.send('Prefix Updated to ' + prefixsymbol)
	#else:
	#    await ctx.send('Only mods can set prefix!')

#SKILLS
@client.command(aliases = ['hr'])
async def hero(ctx, *, name):
		comparedHero = ""
		x = 0
		y = 0
		for hero in data:
			if name.upper() == hero['name'].upper():
				reply = (f'```css\n.' +
							hero['name'] + ' - ' + hero['rarity'] + ' ' + hero['attribute'] + ' ' + hero['class type'] + '\n' +
							hero['leader name'] + ' - ' + hero['leader skill'] +
							'\n\n.S1 ' + hero['s1 name'] + ' - ' + hero['s1 cdr'] +
							' cd\n' + hero['s1'] +
							'\n\n.MAX\n' +
							hero['s1 max'] +
							'\n\n.S2 ' + hero['s2 name'] +' - ' + hero['s2 cdr'] +
							' cd\n' + hero['s2'] +
							'\n\n.MAX\n' +
							hero['s2 max'] +
							'\n```')
				break
			else:
				test = SequenceMatcher(None, name.upper(), hero['name'].upper()).ratio()
				if test >= 0.6:
					print(f'test1 = ' + str(test) + ' - ' + hero['name'])
					x += x + 1
					#print(data.index(hero))
					#print(len(data))
					if data.index(hero) == len(data)-1 and x > 1:
						comparedHero = comparedHero + ' or '
					elif data.index(hero) < len(data) and x > 1:
						comparedHero = comparedHero + ', '

					comparedHero = comparedHero + hero['name']
				elif data.index(hero) == len(data)-1 and x == 0:
					comparedHero = 'something else'
					y = 1

				if y == 1:
					reply = (f'Could not find ' + '***' + name + '***' + '. Try ' + comparedHero + '.')
				else:
					reply = (f'Could not find ' + '***' + name + '***' + '. Do you mean ' + '***' + comparedHero + '***' + '?')
		await ctx.send(reply)

#GRIMOIRE
@client.command(aliases = ['gr', 'grimoire'])
async def grim(ctx, *, name):
		comparedHero = ""
		x = 0
		y = 0
		for hero in data:
			if name.upper() == hero['name'].upper():
				reply = (f'```css\n.' +
							hero['name'] + ' - ' + hero['grimoire item'] +
							'\nSkill: ' + hero['grimoire name'] + ' ' +
							'\n' + hero['grimoire skill'] +
							'\n```')
				break
			else:
				test = SequenceMatcher(None, name.upper(), hero['name'].upper()).ratio()
				if test >= 0.6:
					print(f'test1 = ' + str(test) + ' - ' + hero['name'])
					x += x + 1
					#print(data.index(hero))
					#print(len(data))
					if data.index(hero) == len(data)-1 and x > 1:
						comparedHero = comparedHero + ' or '
					elif data.index(hero) < len(data) and x > 1:
						comparedHero = comparedHero + ', '

					comparedHero = comparedHero + hero['name']
				elif data.index(hero) == len(data)-1 and x == 0:
					comparedHero = 'something else'
					y = 1

				if y == 1:
					reply = (f'Could not find ' + '***' + name + '***' + '\'s grimoire.' + '. Try ' + comparedHero + '.')
				else:
					reply = (f'Could not find ' + '***' + name + '***' + '\'s grimoire.' + '. Do you mean ' + '***' + comparedHero + '***' + '?')
		await ctx.send(reply)

#SEARCH BY RARITY
@client.command(aliases=['rar'])
async def rarity(ctx, *, rarityInput):
	listofheroes = ""
	y = 0
	x = 0
	for hero in data:
		if rarityInput.upper() == hero['rarity'].upper():
			x = x + 1

			if data.index(hero) == len(data)-1 and x > 1:
				listofheroes = listofheroes + ' and '
			elif data.index(hero) < len(data) and x > 1:
				listofheroes = listofheroes + ', '

			listofheroes = listofheroes + '**' + hero['name'] + '**'
		elif data.index(hero) == len(data)-1 and x == 0:
			y = 1

	if y == 1:
		reply = ('Please type **SR** or **SSR**.')
	else:
		reply = (f'List of ' + rarityInput + ' heroes include: ') + listofheroes + '.'
	await ctx.send(reply)


def predicate(message, l, r):
	def check2(reaction, user):
		#if reaction.message.id != message.author or user == message.author:
		if reaction.message.id != message.id or user == client.user:
			return False
		if l and reaction.emoji == left:
			return True
		if r and reaction.emoji == right:
			return True
		return False
	return check2

def listMatchedHeroes(matchedLeaderList, index):
	msg = ''
	for numberMatch in matchedLeaderList:
		msg = msg + '\n**' + str(index) + '** - ' + matchedLeaderList[index]
		index+=1
	return msg

#FOR LISTING OUT KEYWORDS IN DESC
def listKeywords(ldrSKillsKeywords, index):
	msg = ''
	for numberMatch in ldrSKillsKeywords:
		notation = index+1
		msg = msg + '\n**' + str(notation) + '** - ' + ldrSKillsKeywords[index]
		index+=1
	return msg

#TO CHECK SENDER
def check(author):
	def inner_check(message):
		if message.author != author:
			return False

		return inner_check

#SEARCH BY LDR SKILL
@client.command(aliases=['ldr'])
async def leader(ctx, *, name):
	comparedHero = ""
	x = 0
	y = 0
	for hero in data:
		if name.upper() == hero['name'].upper():
			reply = (f'```css\n.' +
						hero['name'] + ' - ' +
						hero['leader name'] + '\n' + hero['leader skill'] +
						'\n```')
			break
		else:
			test = SequenceMatcher(None, name.upper(), hero['name'].upper()).ratio()
			if test >= 0.6:
				print(f'test1 = ' + str(test) + ' - ' + hero['name'])
				x += x + 1
				#print(data.index(hero))
				#print(len(data))
				if data.index(hero) == len(data)-1 and x > 1:
					comparedHero = comparedHero + ' or '
				elif data.index(hero) < len(data) and x > 1:
					comparedHero = comparedHero + ', '

				comparedHero = comparedHero + hero['name']
			elif data.index(hero) == len(data)-1 and x == 0:
				comparedHero = 'something else'
				y = 1

			if y == 1:
				reply = (f'Could not find ' + '***' + name + '***' + '. Try ' + comparedHero + '.')
			else:
				reply = (f'Could not find ' + '***' + name + '***' + '. Do you mean ' + '***' + comparedHero + '***' + '?')
	await ctx.send(reply)

#SEARCH Command
@client.command()
async def search(ctx, *, searchInput):
	index = 0
	msg = ''
	res = None
	matchedLeaderList = list()
	matchedLeaderListSkills = list()
	matchedHeroList = list()
	userInput = ""
	totalPages = 0
	pageIndex = 1
	ldrSKillsKeywords = ("Attack", "Defense", "Crit Dmg", "Crit Rate", "Damage Reduction", "Fire", "Water", "Wind", "Dark", "Light")
	leaderSearch = ("leader", "ldr", "ls")
	raritySearch = ("rar", "rarity", "listall")
	raritySearchKeywords = ("UR", "SR", "SSR")
	typeSearchKeywords = ("Fire", "Water", "Wind", "Dark", "Light")
	typeSearch = ("element", "ele", "type", "attribute", "attr")
	helpSearch = ("help")
	descString = ""
	setResultsPerPage = 0

	#HELP SEARCH
	if searchInput.lower() in helpSearch:
		print(oldprefixdata.get(str(ctx.guild.id)))
		embedHelp = discord.Embed(title="{}search leader".format(oldprefixdata.get(str(ctx.guild.id))), description="list", color=0x00ff00)
		await ctx.send(embed=embedHelp)

	#ELEMENT TYPE SEARCH
	if searchInput.lower() in typeSearch:
		setResultsPerPage = 15
		embedList = discord.Embed(title="Type a number from `1-" + str(len(typeSearchKeywords)) + "`", description=listKeywords(typeSearchKeywords, index), color=0x00ff00)

		botMsg = await ctx.send(embed=embedList)
		msg = await client.wait_for('message', check=check(ctx.author), timeout=30)

		try:
			chosenKeyword = int(msg.content)
		except ValueError:
			print("value error2")

		chosenKeyword = int(msg.content)
		if chosenKeyword >= 1 and chosenKeyword <= len(typeSearchKeywords):
			userInput = typeSearchKeywords[chosenKeyword-1]
			print("length " + str(len(typeSearchKeywords)))
			print("userinput " + str(userInput))
			print("chosenkeyword " + str(chosenKeyword))
			#delete the response user typed
			await msg.delete()

			#CREATE NEW LIST OF MATCHES
			for hero in data:
				match = re.findall(userInput.upper(), hero['attribute'].upper())
				if match:
					matchedHeroList.append(hero['name'])
					#print(matchedHeroList)

			matchedHeroList.sort()
			print(matchedHeroList)
			#print(matchedLeaderListSkills2)
			#SEND OUT MATCHED LIST BASED ON SELECTION
			while True:
				maxResultsPerPage = 0
				print("HELLO")
				totalPages = math.ceil(len(matchedHeroList)/setResultsPerPage)
				l = pageIndex != 1
				r = pageIndex != totalPages

				if pageIndex == 1:
					index = 0
				else:
					index = (pageIndex-1) * setResultsPerPage
				print("Index at 1: " + str(index))
				print("HELLO2")

				if pageIndex == totalPages:
					resultsInPage = len(matchedHeroList) %  setResultsPerPage
					if resultsInPage == 0:
						resultsInPage = setResultsPerPage
				else:
					resultsInPage = setResultsPerPage

				while maxResultsPerPage < resultsInPage:
					descString = descString + "\n**" + str(index+1) + "** - " + matchedHeroList[index]
					maxResultsPerPage+=1
					index+=1

				embed = discord.Embed(title="Search results based on \"*" +userInput.upper() + "*\" element:\n  Type `{}hr Riah` for more info on hero.".format(oldprefixdata.get(str(ctx.guild.id))), description=descString, color=0x00ff00)
				embed.set_footer(text="Page " + str(pageIndex) + " of " + str(totalPages) + ".")

				print("HELLO4")
				#EDIT MESSAGE FROM EARLIER
				await botMsg.edit(embed=embed)
				descString = ""
				await botMsg.add_reaction(left)
				await botMsg.add_reaction(right)
				react, user = await client.wait_for('reaction_add', check=predicate(botMsg, l, r))
				await botMsg.remove_reaction(react.emoji, user)
				print("user: " + str(user))
				print("ctx.author: " + str(ctx.author))
				if str(ctx.author) == str(user):
					if react.emoji == left:
						pageIndex -= 1
					elif react.emoji == right:
						pageIndex += 1

		else:
			embedInvalid = discord.Embed(title="Invalid Command. Please type a number from `1 -" + len(typeSearchKeywords) + "`.", color=0xee2002)
			await ctx.send(embed=embedInvalid)


	#RARITY SEARCH
	if searchInput.lower() in raritySearch:
		#LIST OUT RARITY
		setResultsPerPage = 15
		embedList = discord.Embed(title="Type a number from `1-3`", description=listKeywords(raritySearchKeywords, index), color=0x00ff00)

		botMsg = await ctx.send(embed=embedList)
		#while True:
		msg = await client.wait_for('message', check=check(ctx.author), timeout=30)

		try:
			chosenKeyword = int(msg.content)
		except ValueError:
			print("value error2")

		chosenKeyword = int(msg.content)
		if chosenKeyword >= 1 and chosenKeyword <= 3:
			if chosenKeyword == 1: #chose Attack Increase
				userInput = "UR"
			elif chosenKeyword == 2:
				userInput = "SSR"
			elif chosenKeyword == 3:
				userInput = "SR"
			else:
				userInput = False
			print(userInput)
			print(chosenKeyword)
			#delete the response user typed
			await msg.delete()

			#CREATE NEW LIST OF MATCHES
			for hero in data:
				if userInput.upper() == hero['rarity'].upper():
					matchedHeroList.append(hero['name'])
					print(matchedHeroList)

			matchedHeroList.sort()
			print(matchedHeroList)
			#print(matchedLeaderListSkills2)
			#SEND OUT MATCHED LIST BASED ON SELECTION
			while True:
				maxResultsPerPage = 0
				print("HELLO")
				totalPages = math.ceil(len(matchedHeroList)/setResultsPerPage)
				l = pageIndex != 1
				r = pageIndex != totalPages

				if pageIndex == 1:
					index = 0
				else:
					index = (pageIndex-1) * setResultsPerPage
				print("Index at 1: " + str(index))
				print("HELLO2")

				if pageIndex == totalPages:
					resultsInPage = len(matchedHeroList) % setResultsPerPage
				else:
					resultsInPage = setResultsPerPage

				while maxResultsPerPage < resultsInPage:
					descString = descString + "\n**" + str(index+1) + "** - " + matchedHeroList[index]
					maxResultsPerPage+=1
					index+=1

				embed = discord.Embed(title="Search results based on \"*" +userInput.upper() + "*\" element:\n  Type `{}hr Riah` for more info on hero.".format(oldprefixdata.get(str(ctx.guild.id))), description=descString, color=0x00ff00)
				embed.set_footer(text="Page " + str(pageIndex) + " of " + str(totalPages) + ".")

				print("HELLO4")
				#EDIT MESSAGE FROM EARLIER
				await botMsg.edit(embed=embed)
				descString = ""
				await botMsg.add_reaction(left)
				await botMsg.add_reaction(right)
				react, user = await client.wait_for('reaction_add', check=predicate(botMsg, l, r))
				await botMsg.remove_reaction(react.emoji, user)
				print("user: " + str(user))
				print("ctx.author: " + str(ctx.author))
				if str(ctx.author) == str(user):
					if react.emoji == left:
						pageIndex -= 1
					elif react.emoji == right:
						pageIndex += 1

		else:
			embedInvalid = discord.Embed(title="Invalid Command. Please type a number from `1 -" + len(matchedHeroList) + "`.", color=0xee2002)
			await ctx.send(embed=embedInvalid)


	#LEADER SEARCH
	if searchInput.lower() in leaderSearch:
		#LIST OUT POSSIBLE LEADERSKILL KEYWORDS
		setResultsPerPage = 5
		embedList = discord.Embed(title="Type a number from `1-10`", description=listKeywords(ldrSKillsKeywords, index), color=0x00ff00)

		botMsg = await ctx.send(embed=embedList)
		#while True:
		msg = await client.wait_for('message', check=check(ctx.author), timeout=30)

		try:
			chosenKeyword = int(msg.content)
		except ValueError:
			print("value error2")

		chosenKeyword = int(msg.content)
		if chosenKeyword >= 1 and chosenKeyword <= 10:
			if chosenKeyword == 1: #chose Attack Increase
				userInput = "ATK"
			elif chosenKeyword == 2:
				userInput = "DEF"
			elif chosenKeyword == 3:
				userInput = "CRIT Dmg"
			elif chosenKeyword == 4:
				userInput = "CRIT rate"
			elif chosenKeyword == 5:
				userInput = "DMG taken"
			elif chosenKeyword == 6:
				userInput = "Fire"
			elif chosenKeyword == 7:
				userInput = "Water"
			elif chosenKeyword == 8:
				userInput ="Wind"
			elif chosenKeyword == 9:
				userInput = "Dark"
			elif chosenKeyword == 10:
				userInput = "Light"
			else:
				userInput = False
			print(userInput)
			print(chosenKeyword)
			#delete the response user typed
			await msg.delete()

			#CREATE NEW LIST OF MATCHES
			for hero in data:
				match = re.findall(userInput.upper(), hero['leader skill'].upper())
				if match:
					matchedLeaderList.append(hero['name'])
					matchedLeaderListSkills.append(hero['leader skill'])
					print(matchedLeaderList)

			matchedLeaderList, matchedLeaderListSkills = zip(*sorted(zip(matchedLeaderList, matchedLeaderListSkills)))
			print(list(zip(matchedLeaderList, matchedLeaderListSkills)))
			print(matchedLeaderList)
			print(matchedLeaderListSkills)
			#print(matchedLeaderListSkills2)
			#SEND OUT MATCHED LIST BASED ON SELECTION
			while True:
				maxResultsPerPage = 0
				print("HELLO")
				totalPages = math.ceil(len(matchedLeaderList)/setResultsPerPage)
				l = pageIndex != 1
				r = pageIndex != totalPages

				if pageIndex == 1:
					index = 0
				else:
					index = (pageIndex-1) * setResultsPerPage
				print("Index at 1: " + str(index))
				print("HELLO2")
				embed = discord.Embed(title="Search results based on \"*" +userInput.upper() + "*\":", description="", color=0x00ff00)
				embed.set_footer(text="Page " + str(pageIndex) + " of " + str(totalPages) + ".")
				if pageIndex == totalPages:
					resultsInPage = len(matchedLeaderList) % setResultsPerPage
				else:
					resultsInPage = setResultsPerPage
				while maxResultsPerPage < resultsInPage:
					embed.add_field(name=matchedLeaderList[index], value=matchedLeaderListSkills[index], inline=False)
					maxResultsPerPage+=1
					index+=1

				print("HELLO4")
				#EDIT MESSAGE FROM EARLIER
				await botMsg.edit(embed=embed)
				await botMsg.add_reaction(left)
				await botMsg.add_reaction(right)
				react, user = await client.wait_for('reaction_add', check=predicate(botMsg, l, r))
				await botMsg.remove_reaction(react.emoji, user)
				print("user: " + str(user))
				print("ctx.author: " + str(ctx.author))
				if str(ctx.author) == str(user):
					if react.emoji == left:
						pageIndex -= 1
					elif react.emoji == right:
						pageIndex += 1
		else:
			embedInvalid = discord.Embed(title="Invalid Command. Please type a number from `1 -" + len(chosenKeyword) + "`.", color=0xee2002)
			await ctx.send(embed=embedInvalid)



'''
@leader.error
async def leader_error(ctx, error):
	if isinstance(error, ConversionError):
		await ctx.send("Invalid Command")
	elif isinstance(error, discord.ext.commands.BadArgument):
		await ctx.send('Invalid Command')
'''

#    for hero in data:
#        if any(keyword in hero["leader skill"].lower() for keyword in leaderInput.lower()):
#            await ctx.send('```css\n.' + hero["name"] + ' - ' + hero["leader name"] + '\n\n' + hero["leader skill"] + '```')

#CREDIT
@client.command(aliases = ['credits'])
async def credit(ctx):
	await ctx.send(f'Coded by Cosmic#2229. Thanks to Shurik#0243 for the ability descriptions and T100 for the support in making this client.')

client.run('NTkwMDUwMzMxNTM1MjEyNTQ1.XQclNg.tkALlcE5NNV4xfwsxiiehxTZ4Kk')
