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


#OPEN PREFIX FILE
with open('prefixes.json') as server_prefix:
	oldprefixdata = json.load(server_prefix)
default_prefix = "$"

def prefix(bot, message):
	id = message.guild.id
	print(id)
	print(oldprefixdata.get(str(id), default_prefix))
	return oldprefixdata.get(str(id), default_prefix)

client = commands.Bot(command_prefix=prefix, case_insensitive=True)
#client = commands.Bot(command_prefix = '.')
client.remove_command('help')
#os.chdir(r'E:\Program Files\Personal Folder\discord stuff\discordjs\SophiaBot')

left = '⏪'
right = '⏩'

@client.event
async def on_ready():
	print('Bot is ready.')

@client.command()
async def help(ctx):
	await ctx.send('```\nCommands:\n\nhero (e.g. {prefix}hero young gleck)\ngrimoire (e.g. {prefix}grimoire ludmila)\nprefix (change prefix)\nleader (e.g. {prefix}leader)\ncredits\n\nAbbreviations:\nhr (hero)\ngr (grimoire)\nldr (leader)\n```')

#HERO DB
with open('db.json') as hero_db:
	data = json.load(hero_db)

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

#for hero in data:
#	match = re.findall(leaderInput.upper(), hero['leader skill'].upper())
#	if match:
		#await ctx.send('```css\n.' + hero["name"] + ' - ' + hero["leader name"] + '\n\n' + hero["leader skill"] + '```')

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
		try:
			int(message.content)
			return True
		except ValueError:
			return False
	return inner_check

#SEARCH BY LDR SKILL
@client.command(aliases=['ldr'])
async def leader(ctx):
	index = 0
	msg = ''
	res = None
	matchedLeaderList = list()
	matchedLeaderListSkills = list()
	leaderInput = ""
	breakCmd = False
	totalPages = 0
	pageIndex = 1
	#action = ctx.send
	ldrSKillsKeywords = ("Attack", "DEF", "Crit Dmg", "Crit Rate", "Damage Reduction", "Fire", "Water", "Wind", "Dark", "Light")

	#LIST OUT POSSIBLE LEADERSKILL KEYWORDS
	while True:
		embedList = discord.Embed(title="Type a number from 1-9", description=listKeywords(ldrSKillsKeywords, index), color=0x00ff00)

		botMsg = await ctx.send(embed=embedList)
		try:
			msg = await client.wait_for('message', check=check(ctx.author), timeout=30)
		except asyncio.TimeoutError:
			embedError = discord.Embed(title="Command timed out." , color=0xee2002)
			await ctx.send(embed=embedError)
		chosenKeyword = int(msg.content)
		#action = ctx.edit

		if chosenKeyword == 1: #chose Attack Increase
			leaderInput = "ATK"
		elif chosenKeyword == 2:
			leaderInput == "DEF"
		elif chosenKeyword == 3:
			leaderInput = "CRIT Dmg"
		elif chosenKeyword == 4:
			leaderInput = "CRIT rate"
		elif chosenKeyword == 5:
			leaderInput = "DMG taken"
		elif chosenKeyword == 6:
			leaderInput = "Fire"
		elif chosenKeyword == 7:
			leaderInput = "Water"
		elif chosenKeyword == 8:
			leaderInput ="Wind"
		elif chosenKeyword == 9:
			leaderInput = "Dark"
		elif chosenKeyword == 10:
			leaderInput = "Light"
		else:
			leaderInput = False
			breakCmd = True
		print(leaderInput)
		print(chosenKeyword)
		#delete the response user typed
		await msg.delete()

		#CREATE NEW LIST OF MATCHES
		for hero in data:
			match = re.findall(leaderInput.upper(), hero['leader skill'].upper())
			if match:
				matchedLeaderList.append(hero['name'])
				matchedLeaderListSkills.append(hero['leader skill'])
				print(matchedLeaderList)

		matchedLeaderList, matchedLeaderListSkills = zip(*sorted(zip(matchedLeaderList, matchedLeaderListSkills)))
		print(list(zip(matchedLeaderList, matchedLeaderListSkills)))
		print(matchedLeaderList)
		print(matchedLeaderListSkills)
		#SEND OUT MATCHED LIST BASED ON SELECTION
		while True:
			maxResultsPerPage = 0
			print("HELLO")
			totalPages = math.ceil(len(matchedLeaderList)/5)
			l = pageIndex != 1
			r = pageIndex != totalPages

			if pageIndex == 1:
				index = 0
			else:
				index = (pageIndex-1) * 5
			print("Index at 1: " + str(index))
			print("HELLO2")
			embed = discord.Embed(title="Search results based on \"*" +leaderInput + "*\".", description="", color=0x00ff00)
			embed.set_footer(text="Page " + str(pageIndex) + " of " + str(totalPages) + ".")
			if pageIndex == totalPages:
				resultsInPage = len(matchedLeaderList) % 5
			else:
				resultsInPage = 5
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

@leader.error
async def leader_error(ctx, error):
	if isinstance(error, ConversionError):
		await ctx.send("Invalid Command")
	elif isinstance(error, discord.ext.commands.BadArgument):
		await ctx.send('Invalid Command')

#    for hero in data:
#        if any(keyword in hero["leader skill"].lower() for keyword in leaderInput.lower()):
#            await ctx.send('```css\n.' + hero["name"] + ' - ' + hero["leader name"] + '\n\n' + hero["leader skill"] + '```')

#CREDIT
@client.command(aliases = ['credits'])
async def credit(ctx):
	await ctx.send(f'Coded by Cosmic#2229. Thanks to Shurik#0243 for the ability descriptions and T100 for the support in making this client.')

client.run('NTg5NTMzNzg5NDU0MzM2MDAx.XQXbSA.hQ5fjrfqM33ZBtFdNV7UaP2-CmU')
