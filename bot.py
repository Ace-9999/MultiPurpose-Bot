import discord, time, random, asyncio, json, os
from datetime import datetime, timedelta
from discord.ext import commands

bot = commands.Bot(command_prefix = '//')


@bot.event
async def on_ready():
	print('Logged in')
	print("I'm online and working")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You"))

@bot.command()
async def echo(ctx, channel,  msg_echo):
	guild = bot.get_guild(799907027832537088)
	channelid = channel.replace('<#','')
	channelid = channelid.replace('>','')
	channel = guild.get_channel(int(channelid))
	await channel.send(str(msg_echo))

@bot.command(aliases = ['sm'])
async def slowmode(ctx, no_time):
	if ctx.author.guild_permissions.manage_channels == True:
		if 'remove' in no_time or no_time == '0':
			await ctx.channel.edit(slowmode_delay=0)
			await ctx.channel.send(f'The Slowmode has been removed.')
		elif 's' in no_time:
			t = no_time.strip('s')
			t = int(t)
			f_time = int(t)
			if t == 0:
				await ctx.send(f'The Slowmode has been removed.')
			else:
				await ctx.send(f'The Slowmode is now {t} seconds.')

		elif 'h' in no_time:
			t = no_time.strip('h')
			t = int(t)
			f_time = int(t * 3600)
			await ctx.send(f'The Slowmode is now {t} hours.')

		elif 'm' in no_time:
			t = no_time.strip('m')
			t = int(t)
			f_time = int(t * 60)
			await ctx.send(f'The Slowmode is now {t} minutes.') 
		await ctx.channel.edit(slowmode_delay=f_time)
	else:
		await ctx.delete()
		return

@bot.command(aliases = ['lk', 'l'])
async def lock(ctx, *, reason=None):
	if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True:
		overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = False
		await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		x = reason
		if x == None:
			embed = discord.Embed(title = 'Channel Locked :lock:', description = f'By - {ctx.author.mention} \nReason - None Given', colour = discord.Colour.magenta())
		else:
			embed = discord.Embed(title = 'Channel Locked :lock:', description = f'By - {ctx.author.mention} \nReason - {x}', colour = discord.Colour.magenta())
		await ctx.send(embed=embed)
	else:
		await ctx.delete()

@bot.command(aliases = ['unlk', 'ul'])
async def unlock(ctx, *, reason=None):
	if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True:
		overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = True
		await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		x = reason
		if x == None:
			embed = discord.Embed(title = 'Channel Unlocked :unlock:', description = f'By - {ctx.author.mention} \nReason - None Given', colour = discord.Colour.magenta())
		else:
			embed = discord.Embed(title = 'Channel Unlocked :unlock:', description = f'By - {ctx.author.mention} \nReason - {x}', colour = discord.Colour.magenta())
		await ctx.send(embed=embed)
	else:
		await ctx.delete()

@bot.command(aliases = ['p'])
async def purge(ctx, lim):
	if ctx.author.guild_permissions.manage_messages == True:
		lim = int(lim)
		if lim < 1:
			await ctx.delete()
			await ctx.channel.send(f'Mhmm. Pretty sure i can\'t purge less than 1 messages {ctx.author.mention}.')
		else:
			await ctx.channel.purge(limit=lim+1)
			x = await ctx.channel.send(f'Purged **{lim}** messages')
			await asyncio.sleep(5)
			await x.delete()
	else:
		await ctx.delete()
		return

@bot.command(aliases = ['latency'])
async def ping(ctx):
	embed=discord.Embed(title = "My Current Latency Is", description = f"{round(bot.latency*1000)} ms", color = discord.Color.magenta())
	await ctx.send(embed=embed)

@bot.command(aliases = ['die'])
async def logout(ctx):
	devs = ['775198018441838642', '802883472628121620']
	if str(ctx.author.id) not in devs:
		await ctx.reply(f'Only **The Devs** can log me out.\nCurrent Devs are <@{devs[0]}>, <@{devs[1]}>')
		return
	embed=discord.Embed(title = "Logged Out", description = f"With Latency {round(bot.latency*1000)}", color = discord.Color.red())
	await ctx.send(embed=embed)
	await bot.logout()

@bot.command()
async def simprate(ctx, *, torate=None):
	if torate == None:
		torate = ctx.author.display_name
	percent = random.randrange(0,100)
	gembed = discord.Embed(title = 'SimpRate Machine', description = f"{torate} is {percent}% Simp :blush:", colour = discord.Colour.magenta())
	await ctx.send(embed=gembed)

@bot.command()
async def coolrate(ctx, *, torate=None):
	if torate == None:
		torate = ctx.author.display_name
	percent = random.randrange(0,100)
	gembed = discord.Embed(title = 'CoolRate Machine', description = f"{torate} is {percent}% Cool :sunglasses:", colour = 00000)
	await ctx.send(embed=gembed)

@bot.command(aliases = ['howgay'])
async def gayrate(ctx, *, torate=None):
	if torate == None:
		torate = ctx.author.display_name
	percent = random.randrange(0,100)
	gembed = discord.Embed(title = 'GayRate Machine', description = f"{torate} is {percent}% Gay :gay_pride_flag:", colour = discord.Colour.blurple())
	await ctx.send(embed=gembed)

@bot.command(aliases = ['ask8', 'magic8', '8ball'])
async def magic_8_ball(ctx, *, question=None):
	random_answers = ['No Doubt', 'My sources tell me YES', 'You can rely on that', 'Better not tell you', 'Reply Hazy, Try Again', 'Nah, I wouldn\'nt keep my hopes high on that', 'Highly Doubtful', 'Hell No']
	if question == None:
		await ctx.reply('Ask a question so that i can reply to it smh')
		return
	embed=discord.Embed(description=random.choice(random_answers), colour = discord.Color.blurple())
	embed.set_author(name = question, icon_url = ctx.author.avatar_url)
	await ctx.send(embed=embed)

@bot.command(aliases = ['m'])
async def mute(ctx, member:discord.User=None, no_time = None, *, reason=None):
	if member == None:
		await ctx.reply('Can\'t mute yourself')
		return
	if ctx.author.top_role < member.top_role:
		await ctx.reply('You can only mute Members below you.')
		return
	if no_time == None:
		muterole = discord.utils.get(ctx.guild.roles, name = '・Muted')
		await member.add_roles(muterole)
		await ctx.reply(f'Muted **{member.name}** with reason **{reason}**')
		await member.send(f'You were Muted in Peaky Dankers for Reason: **{reason}**')
		return
	else:
		muterole = discord.utils.get(ctx.guild.roles, name = '・Muted')
		await member.add_roles(muterole)
		if 's' in no_time:
			t = no_time.strip('s')
			t = int(t)
			f_time = int(t)

		elif 'h' in no_time:
			t = no_time.strip('h')
			t = int(t)
			f_time = int(t * 3600)

		elif 'm' in no_time:
			t = no_time.strip('m')
			t = int(t)
			f_time = int(t * 60)
		await ctx.reply(f'Muted **{member.name}** with reason **{reason}**')
		await member.send(f'You were Muted in Peaky Dankers for {f_time} seconds with Reason: **{reason}**')
		await asyncio.sleep(f_time)
		await member.remove_roles(muterole)

@bot.command(aliases = ['um'])
async def unmute(ctx, user:discord.User=None):
	if user == None:
		await ctx.reply('Mention a muted person to unmute.')
		return
	if discord.utils.get(user.roles, name = '・Muted') is None:
		await ctx.reply('This Person is not Muted.')
		return
	if ctx.author.top_role < user.top_role:
		await ctx.reply('Can only unmute people below you.')
		return
	muterole = discord.utils.get(ctx.guild.roles, name = '・Muted')
	await user.remove_roles(muterole)

@bot.command(aliases = ['k'])
async def kick(ctx, person:discord.User=None, *, reason=None):
	if ctx.author.guild_permissions.kick_members != True:
		await ctx.reply('You don\'t have the `Kick Members` Permission')
		return
	if person == None:
		await ctx.send('Can\'t kick yourself')
		return
	if ctx.author.top_role < person.top_role:
		await ctx.reply('Cannot do this action due to role hierarchy.\nThis person is higher than you.')
		return
	try:
		await ctx.guild.kick(person, reason=reason)
		embed=discord.Embed(title = f"Kicked {person.name}", description = f'Reason - {reason}\nModerator: {ctx.author.name}', colour=discord.Color.red())
		embed.set_thumbnail(url = person.avatar_url)
		await ctx.send(embed=embed)
	except:
		await ctx.reply('**Error:**\nThis user is higher than me in the role hierarchy.')
		return

@bot.command(aliases = ['b', 'hammer'])
async def ban(ctx, person:discord.User=None, *, reason=None):
	if ctx.author.guild_permissions.ban_members != True:
		await ctx.reply('You don\'t have the `Ban Members` Permission')
		return
	if person == None:
		await ctx.send('Can\'t ban yourself')
		return
	if ctx.author.top_role < person.top_role:
		await ctx.reply('Cannot do this action due to role hierarchy.\nThis person is higher than you.')
		return
	else:
		try:
			await ctx.guild.ban(person, reason=reason)
			embed=discord.Embed(title = f"Banned {person.name}", description = f'Reason - {reason}\nModerator: {ctx.author.name}', colour=discord.Color.red())
			embed.set_thumbnail(url = person.avatar_url)
			await ctx.send(embed=embed)
		except:
			await ctx.reply('**Error:**\nThis user is higher than me in the role hierarchy.')
			return


bot.run('TOKEN')

