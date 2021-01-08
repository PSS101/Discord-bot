import discord
from discord.ext import commands
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as  f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as  f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as  f:
      json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix changed to {prefix}')



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('I am a bot umu'))
    print("Bot is ready")


@client.event
async def on_member_join(member):
    print(f'{member.mention} Welcome to the server')

@client.event
async def on_member_leave(member):
    print(f'{member}has left the server')




@client.command()
async def ping(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    x = (f'{round(client.latency * 1000)}ms')
    embed.add_field(name=':ping_pong:   Ping   :ping_pong: ', value=x, inline=False)

    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def Help(ctx):
  author = ctx.message.author
  embed = discord.Embed(
      colour=discord.Colour.blue()
  )
  
  embed.set_author(name='Help')
  embed.add_field(name='-------------', value='here are the lists of the commands', inline=False)
  embed.add_field(name='.ping', value='Return the ping of the user', inline=False)
  embed.add_field(name='.clear', value='Clears the spam messages', inline=False)
  embed.add_field(name='.kick', value='Kicks the user out of the server', inline=False)
  embed.add_field(name='.ban', value='Bans the user' , inline=False)
  embed.add_field(name='.unban', value='Unbans the user', inline=False)
  embed.add_field(name='.userinfo', value='info the user', inline=False)

  channel = await author.create_dm()
  await channel.send(author.mention, embed=embed)
  await ctx.send(embed=embed)

@client.command()
async def members(ctx):
    members= ctx.guild.members
    for member in members:
        await ctx.send(member.name)

    await ctx.send("done")

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()

async def kick(ctx, member : discord.Member , *, reason=None):
    await member.kick()
    await ctx.send(f' {member.name} has been kicked ')
    print(f'{member.name},has been kicked')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member , *, reason=None):
    await member.ban()
    await ctx.send(f' {member.mention} has been banned ,'
                   f'F in the chat')
    print(f'{member.name},has been banned')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
          await ctx.guild.unban(user)
          await ctx.send(f'Successfully unbanned {user.mention}')
          print(f'Successfully unbanned {user.mention}')
          return

@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed.set_author(name='Userinfo')
    embed.add_field(name='Username ', value=user.name, inline=False)
    embed.add_field(name='The ID of the user is ', value=user.id, inline=True)
    embed.add_field(name='The status of the user is', value=user.status, inline=True)
    embed.add_field(name='Role of the user', value=user.top_role, inline=False)
    embed.add_field(name='The user joined at', value=user.joined_at, inline=True)

    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(':no_entry_sign:  Command not found')
@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArguments):
    await ctx.send('Syntax error please try again')


client.run('Nzk0NTk0MjUyNjg0MjYzNDM0.X-9FkA.ElyptcL30yc-979JZCz1qO6LRCQ')
