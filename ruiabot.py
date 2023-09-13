import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import os
from mytimer import timer
from random import randint


TOKEN = os.environ["DISCORD_BOT_TOKEN"]
PATH = os.getcwd()

client = discord.Client(intents=discord.Intents.all())
slash_client = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@slash_client.slash(name="timeschedule",
                    description="ポモドーロ用のスケジュールを送信します",
                    options=[
                        create_option(
                            name="start_time",
                            description="hh:mm",
                            option_type=3,
                            required=True
                        ),
                        create_option(
                            name="end_time",
                            description="hh:mm",
                            option_type=3,
                            required=True
                        )
                    ])
async def _timeschedule(ctx,start_time:str, end_time:str):
    timer(start_time,end_time).gen_pomodoro()
    await ctx.send(file=discord.File(PATH+'/table.png'))

@slash_client.slash(name="ping")
async def _ping(ctx):
    await ctx.send(f"Pong! ({client.latency*1000}ms)")

@slash_client.slash(name="d100",
                    description="1~100のランダムダイス",
                    options=[
                        create_option(
                            name="ccb",
                            description="5以下でクリティカル、96以上でファンブルにする。",
                            option_type=5,
                            required=False,
                            choices=[True,False]
                        ),
                        create_option(
                            name="target",
                            description="目標値。これ以下の出目で成功。",
                            option_type=4,
                            required=False
                        ),
                        create_option(
                            name="target_reverse",
                            description="(m)D(n)>=target 達成値を、それ以上の時に成功にする。Default:False",
                            option_type=5,
                            required=False,
                            choices=[True,False]
                        ),
                        create_option(
                            name="comment",
                            description='"(m)D(n) (comment)【聞き耳】”など。',
                            option_type=3,
                            required=False
                        )
                    ])
async def _d100(ctx,ccb:bool=False,target:int=-1,target_reverse:bool=False,comment:str=""):
    d = randint(1,100)
    if comment: comment=" "+comment
    com = ""
    if target != -1:
        if d<=target: com="成功"
        else: com="失敗"
    if ccb:
        if d>=96 and (target == -1 or d>target):
            com = "ファンブル"
        elif d<=5 and (target == -1 or d<=target):
            com = "クリティカル！"
    await ctx.send(f'{["1d100","CCB"][ccb]}{["",f"<={target}"][target != -1]}{comment}　＞　{d}　{com}')

@slash_client.slash(name="dice",
                    description="(m)D(n) n面ダイスをm回ロール",
                    options=[
                        create_option(
                            name="m",
                            description="試行回数",
                            option_type=4,
                            required=True
                        ),
                        create_option(
                            name="n",
                            description="ダイスの面数（=n面ダイス）",
                            option_type=4,
                            required=True
                        ),
                        create_option(
                            name="b_dice",
                            description="反復試行ダイス。(m)B(n)が出力される。達成値も個別に判定される。Default:False",
                            option_type=5,
                            required=False,
                            choices=[True,False]
                        ),
                        create_option(
                            name="target",
                            description="(m)D(n)<=target達成値。(m)B(n)の合計値がそれ以下であるかどうかで判定する。Default:-1(None)",
                            option_type=4,
                            required=False
                        ),
                        create_option(
                            name="target_reverse",
                            description="(m)D(n)>=target 達成値を、それ以上の時に成功にする。Default:False",
                            option_type=5,
                            required=False,
                            choices=[True,False]
                        ),
                        create_option(
                            name="comment",
                            description='"(m)D(n) (comment)【聞き耳】”など。',
                            option_type=3,
                            required=False
                        )
                    ])
async def _dice(ctx,m:int,n:int,b_dice:bool=False,target:int=-1,target_reverse:bool=False,comment:str=""):
    orT=target!=-1
    if comment:comment=" "+comment
    if not orT: target_reverse=False
    l=[]
    for i in range(m):
        l.append(randint(1,n))
    sum_l = sum(l)
    str_l = str(l)[1:-1]
    if len(str_l) > 1000:
        str_l = str_l[0:1000]
        str_l = str_l[:str_l.rfind(",")+1]+"…"
    sf=""
    if orT:
        if b_dice == False:
            if (sum_l <= target) ^ target_reverse:
                sf = "成功！"
            else:
                sf = "失敗"
        else:
            count = 0
            for i in l:
                if (i <= target) ^ target_reverse:
                    count += 1
            sf = f"成功数{count}"
    await ctx.send(f'{m}{"db"[b_dice]}{n}{["",f"<={target}",f">={target}"][orT+target_reverse]}{comment}　＞　{str_l}{[f"　＞　{sum_l}",""][b_dice]}{["","　＞　"+sf][orT]}')


client.run(TOKEN)