import os
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv; load_dotenv()
from twitchio.ext import commands
from ttv_requests import TTV_requests
import loyalty

bot = commands.Bot(
    token = os.getenv('BOT_ACCESS_TOKEN'),
    client_id = os.getenv('CLIENT_ID'),
    nick = os.getenv('BOT_NAME'),
    prefix='!',
    initial_channels=[os.getenv('BROADCASTER_NAME')]
)

lurker_list = []

@bot.event()
async def event_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n{bot.nick} is ready!')

    task1 = asyncio.create_task(loyalty.async_setup())
    task2 = asyncio.create_task(init_env_commands())

    await asyncio.gather(task1, task2)


async def init_env_commands():
    link_command_json = os.getenv("LINKS")
    link_command_dict = json.loads(link_command_json)
    
    try:
        for command_name, data in link_command_dict.items():
            link = data['link']
            aliases = data['aliases']
            
            async def command(ctx, command_name=command_name, link=link):
                author = str(ctx.author.name).lower()
                await ctx.send(f'@{author} hier gehts zu meinen {command_name}: {link}')

            bot.add_command(commands.Command(name=command_name, func=command, aliases=aliases))

        return

    except Exception as err:
        print(f'[Error] {err}')



@bot.event()
async def event_message(message):

    time = datetime.now().strftime('%H:%M:%S')

    if message.author:
        author = str(message.author.name).lower()
    
    else:
        author = str(bot.nick).lower()

    print(f'{time} - [CHAT] {author}: {message.content}')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')



@commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
@bot.command(name='vips')
async def vips(ctx):
    ttv_requests = TTV_requests()

    vips_list = ttv_requests.get_vips()

    answer = f'@{ctx.author.name} hier sind alle VIPs: ' + ', '.join(f'{chatter}' for chatter in vips_list)
    await ctx.send(answer)


@commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
@bot.command(name='follower')
async def follower(ctx):
    ttv_requests = TTV_requests()

    follower_list = ttv_requests.get_followers()
    new_follower_list = []
    counter = 0
    first_answer = True

    for follower_name in follower_list:
        if counter <= 350:
            new_follower_list.append(follower_name)
        
        else:
            if first_answer:
                answer = f'@{ctx.author.name} hier sind alle Follower: ' + ', '.join(f'{chatter}' for chatter in new_follower_list)
                print(f'First Answer len: {len(answer)}')
                await ctx.send(answer)
                first_answer = False
            
            else:
                answer = f', '.join(f'{chatter}' for chatter in new_follower_list)
                print(f'Answer len: {len(answer)}')
                await ctx.send(answer)

            counter = 0
            new_follower_list = []

        counter += len(follower_name)
        print(counter)


@commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
@bot.command(name='viewer', aliases=['viewers', 'chatter', 'chatters'])
async def test(ctx):
    ttv_requests = TTV_requests()

    author_id = ttv_requests.fetch_user_id(ctx.author.name)
    print(f'Auhor ID: {author_id}\n')

    chatter_list = ttv_requests.get_chatters()

    for user in chatter_list:
        if user in lurker_list:
            chatter_list.remove(user)

    answer = f'@{ctx.author.name} hier sind alle live viewer: ' + ', '.join(f'{chatter}' for chatter in chatter_list)
    await ctx.send(answer)


@commands.cooldown(rate=2, per=30, bucket=commands.Bucket.user)
@bot.command(name='lurk')
async def lurk(ctx):
    author = str(ctx.author.name).lower()

    if author in lurker_list:
        lurker_list.remove(author)
        await ctx.send(f'@{author}: lurk = false')

    else:
        lurker_list.append(author)
        await ctx.send(f'@{author}: lurk = true')


@commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
@bot.command(name='lurker')
async def lurker(ctx):
    author = str(ctx.author.name).lower()

    if not lurker_list:
        await ctx.send(f'@{author} zu zeit lurk niemand')
    
    else:
        answer = f'@{author} hier sind alle lurker: ' + ', '.join(f'{username}' for username in lurker_list)

        await ctx.send(answer)


@commands.cooldown(rate=1, per=10, bucket=commands.Bucket.user)
@bot.command(name='loyalty', aliases=['points'])
async def get_loyalty(ctx):
    author = str(ctx.author.name).lower()

    message = str(ctx.message.content).lower()

    try:
        _, username = message.split(' ', 1)
        if username.startswith('@'):
            username = username[1:]

    except:
        username = author

    loyalty_points = loyalty.Loyalty().get_user_loyalty(username)

    if author == username:
        if loyalty_points == 0:
            answer = f'@{author} du hast keine Loyalty points'

        else:
            answer = f'@{author} du hast {loyalty_points} loyalty'

    else:
        if loyalty_points == 0:
            answer = f'@{username} hat keine Loyalty points'

        else:
            answer = f'@{username} hat {loyalty_points} loyalty'

    await ctx.send(answer)


# Moderation commands
@bot.command(name='title')
async def change_title(ctx):
    author = str(ctx.author.name).lower()

    message = str(ctx.message.content)

    _, title = message.split(' ', 1)

    ttv_requests = TTV_requests()
    
    if ttv_requests.is_moderator(author):
        if ttv_requests.modify_channel_information(type='title', data=title):
            answer = f'Der Title wurde zu: "{title}" geändert.'
        
        else:
            answer = f'Im Moment kann der Title nicht geändert werden.'

    else:
        answer = f'@{author} du hast nicht die benötigten Rechte dafür.'

    await ctx.send(answer)


@bot.command(name='game')
async def change_game(ctx):
    author = str(ctx.author.name).lower()

    message = str(ctx.message.content)

    _, game = message.split(' ', 1)

    ttv_requests = TTV_requests()
    
    if ttv_requests.is_moderator(author):
        if ttv_requests.modify_channel_information(type='game', data=game):
            answer = f'Das Game wurde zu: "{game}" geändert.'
        
        else:
            answer = f'Im Moment kann der Title nicht geändert werden.'

    else:
        answer = f'@{author} du hast nicht die benötigten Rechte dafür.'

    await ctx.send(answer)


@bot.command(name='addcommand')
async def add_command(ctx):
    author = str(ctx.author.name).lower()

    message = str(ctx.message.content).lower()

    if TTV_requests().is_moderator(author):
        try:
            _, command_name, content = message.split(' ', 2)

            async def command(ctx, content=content):
                await ctx.send(f'{content}')
            
            bot.add_command(commands.Command(name=command_name, func=command))

            answer = f'Der Befehl !{command_name} wurde hinzugefügt.'


        except Exception as err:
            print(f'[Error] {err}')
            answer = f'@{author} der Command geht wie folgt: !addcommand [command name] [content]'
    
    else:
        answer = f'@{author} du hast nicht die benötigten Rechte dafür.'

    await ctx.send(answer)


# Help commands
@bot.command(name='help', aliases=['commandlist', 'commands', 'command', 'info', 'h', 'i', 'c'])
async def help(ctx):
    author = str(ctx.author.name).lower()
    
    command_list = [command.name for command in bot.commands.values()]
    
    excluded_commands = ['ping', 'help']

    answer = f'@{author} hier sind die commands: ' + ', '.join(f'!{cmd}' for cmd in command_list if cmd not in excluded_commands)

    await ctx.send(answer)    





def setup():
    bot.run()

if __name__ == '__main__':
    setup()