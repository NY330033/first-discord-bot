import discord
from discord.ext import commands
from dico_token import Token

import logging # 로깅모듈 추가

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG) #디버그레벨로 로깅시작
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#discord.log라는 파일로 기록될 것임. utf-8 인코딩을 사용하며 write mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(LeveLname)s:%(name)s: %(message)s'))
#로그는 위와 같은 포맷으로 작성될 것입
logger.addHandler(handler)
''' 로깅 설정 끝 '''

intents = discord.Intents.default()
intents.message_content=True

bot = commands.Bot(command_prefix='!', intents=intents)
#bot event나 eommand로 만들면 됨됨

# on_ready는 시작할 때 한번만 실행.
@bot.event
async def on_ready():
    print('Login...')
    print(f'{bot.user}에 로그인하였습니다.')
    print(f'ID: {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('만두랑 해파리 연구'))
 
@bot.event
async def on_message(message):
	# message.content.startswith()는 해당 문자로 시작하는 단어에 대해서
	# 인식하여 메시지 전송. ==로 비교 시 해당 문자만 인식

    if message.content.startswith('테스트'):
        await message.channel.send("{} | {}, 안녕!".format(message.author, message.author.mention))
 
    if message.content == '테스트':
        # 채널에 메시지 전송
        await message.channel.send("{} | {}, 어서오세요!".format(message.author, message.author.mention))

 
bot.run(Token)
