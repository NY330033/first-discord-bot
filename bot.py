import discord
from discord.ext import commands
from dico_token import Token
from datetime import datetime, timezone, timedelta

TIMEZONE_KST = timezone(timedelta(hours=9))  # 한국 시간 (UTC+9)

#---------------- 봇에서 사용하는거 임포트 -------------------- 

import logging # 로깅모듈 추가
import traceback #트레이스백도 추가

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG) #디버그레벨로 로깅시작
log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_discord.log" #파일이름에 날짜 시간 포함 
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
#discord.log라는 파일로 기록될 것임. utf-8 인코딩을 사용함
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#로그는 위와 같은 포맷으로 작성될 것임
logger.addHandler(handler)
''' 로깅 설정 끝 '''

#-------------------------- 로깅 설정 -------------------------- 

intents = discord.Intents.default()
intents.message_content=True

description = '테스트중'

bot = commands.Bot(command_prefix='/', description=description, intents=intents)
#bot event나 eommand로 만들면 됨

# on_ready는 시작할 때 한번만 실행.
@bot.event
async def on_ready():
    print('Login...')
    print(f'{bot.user}에 로그인하였습니다.')
    print(f'ID: {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('만두랑 해파리 연구'))

# onmessage로 해둔 테스트문구 있으니까 command를 못받길래 지움!! 

#--------------------------- 봇 기본 설정 --------------------------

async def fetch_message(channel, target_date, keyword=None, limit=10):
    """ 특정 날짜 및 키워드로 메시지 검색 """
    messages = [msg async for msg in channel.history(limit=limit, around=target_date)]
    logger.debug(f"메시지: {messages}")
    print(f"메시지: {messages}")
    #메시지 내용 말고 id만 뜬다 그래서 검색이 제대로 우리가 기댛나느 결과가 안나온듯? 

    if not messages:
        return None

    # 키워드 필터링 추가
    if keyword:
        messages = [msg for msg in messages if keyword.lower() in msg.content.lower()]

    return messages[0] if messages else None

'''메시지 필터링하고 검색하는 함수'''

# --------------------------------------

@bot.command()
async def hello(ctx):
    '''그냥 테스트용 명령어'''
    await ctx.channel.send("테스트용 명령어입니다.")

@bot.command()
async def find(ctx, date_str: str, time_str: str):
    #/find 날짜문자열(형식이 지정되어있음) < 입력을 받아서 실행되는 명령어
    try: 
        
        #datetime으로 파싱
        target_date_kst = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        target_date_utc = target_date_kst.astimezone(timezone.utc)
        logger.debug(f"input-date: {target_date_kst}")
        print(f"input-date: {target_date_kst}")
        logger.debug(f"input_date_utc: {target_date_utc}")

        found_message = await fetch_message(ctx.channel, target_date_utc)

        if found_message:
            created_at_kst = found_message.created_at.astimezone(TIMEZONE_KST)  # KST 변환
            response = (
                f"**검색 결과:**\n"
                f"`{found_message.content}`\n" #content가 지금 id로 표기되고 있다. 일정 시간 지난 메시지는 그렇게 뜨는듯?? 
                f"**작성자:** {found_message.author}\n"
                f"**작성 시간 (KST):** {created_at_kst.strftime('%Y-%m-%d %H:%M')}"
            )
        else:
            response = "메시지를 찾을 수 없습니다."

        await ctx.channel.send(response)

    except ValueError as e:
        logger.error(f"오류 발생: {e}")
        logger.error("예외 발생 위치: \n"+traceback.format_exc())
        await ctx.channel.send("입력 형식이 잘못되었습니다. YYYY-MM-DD HH:MM와 같이 입력해주세요. ")

bot.run(Token)
