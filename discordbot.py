from discord.ext import commands
import os
import traceback
import requests

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    
ID_CHANNEL_WELCOME = 611805940240482320 # 入室用チャンネルのID(int)
ID_ROLE_WELCOME = 617002862538653696 # 付けたい役職のID(int)
EMOJI_WELCOME = '✅' # 対応する絵文字

# 役職を付与する非同期関数を定義
async def grant_role(payload):
    # 絵文字が異なる場合は処理を打ち切る
    if payload.emoji.name != EMOJI_WELCOME: 
        return

    # チャンネルが異なる場合は処理を打ち切る
    channel = client.get_channel(payload.channel_id)
    if channel.id != ID_CHANNEL_README:
        return

    # Member オブジェクトと Role オブジェクトを取得して役職を付与
    member = channel.guild.get_member(payload.user_id)
    role = guild.get_role(ID_ROLE_WELCOME)
    await member.add_roles(role)
    return member

# リアクション追加時に実行されるイベントハンドラを定義
@client.event
async def on_raw_reaction_add(payload):
    # 役職を付与する非同期関数を実行して Optional[Member] オブジェクトを取得
    member = await grant_role(payload)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def getname(ctx, member: discord.Member):

    await ctx.send(f'User name: {member.name}, id: {member.id}')

    with requests.get(member.avatar_url_as(format='png')) as r:
        img_data = r.content
    with open(f'{member.name}.png', 'wb') as f:
        f.write(img_data)

bot.run(token)
