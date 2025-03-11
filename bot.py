import discord
from discord.ext import commands
from dico_token import Token
from datetime import datetime

import logging # 로깅모듈 추가
import traceback #트레이스백도 추가가

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG) #디버그레벨로 로깅시작
log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_discord.log" #파일이름에 날짜 시간 포함 
handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
#discord.log라는 파일로 기록될 것임. utf-8 인코딩을 사용함
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#로그는 위와 같은 포맷으로 작성될 것임
logger.addHandler(handler)
''' 로깅 설정 끝 '''

intents = discord.Intents.default()
intents.message_content=True

description = '테스트중중'

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

@bot.command()
async def hello(ctx):
    '''그냥 테스트용 명령어'''
    await ctx.channel.send("테스트용 명령어입니다.")

@bot.command()
async def find(ctx, date_str: str):
    try: 

        #datetime으로 파싱
        input_date = datetime.strptime(date_str, "%Y-%m-%d-%H")
        logger.debug(f"input-date: {input_date}")

        #메시지 검색
        messages = [] # < 이게 지금 자꾸 에러가난다... 
        '''
        현재까지 겪은 에러 젠냥이의 편안한개발을 위해 기록해주기 
        1) 비동기 제너레이터를 반환해서 리스트 변환하려고 flatten 쓰니까 그거업더염 시전
        2) 원래 파싱할때 형식을 월-날짜 ~시로 받았더니 띄어쓰기 기준으로 구분해서 시간 누락
        3) 플래튼 안된대서 리스트로 바꾸니까 시간대 정보가 없어서(ㅆㅂ미친아) 오류남
        ^ 이게 왜 발생하냐면 datetime 객체 사이에 1) 시간대 정보 있는 객체랑 2) 없는 객체 섞여있어서 그렇다 함
        그래서 해결법: 시간대정보를 추가하거나 제거해서 통일하면 된대... 
        아마 input_date가 시간대가 없는 객체고 created_at이 시간대가 있는 객체일거래 ㅁㅊ 
        듣고보니까 근데 납득이 됨 input_date는 내가 걍 입력한거라 시간대가 없겠지
        근데 디코에서 검색해서 받아온거면 시간대가 있겠네? 지금 혼자 납득했음 ㅅㅂ 
        그래서 이걸...? input_date에 시간대 정보를 추가해서 변경하면 된다는데
        이걸 쓰려면 pytz를 쓰면 된다는데 나 잘래 여기서부터 젠냥이가 봐 (뭐지) 
        '''
        ans = discord.utils.find(lambda x: x.created_at < input_date, messages)

        if ans:
            await ctx.channel.send(f"조건을 만족하는 가장 나중 메시지: {ans.content}")
        else:
            await ctx.channel.send("조건을 만족하는 메시지가 없습니다.")

    except ValueError as e:
        logger.error(f"오류 발생: {e}")
        logger.error("예외 발생 위치: \n"+traceback.format_exc())
        await ctx.channel.send("입력 형식이 잘못되었습니다. YYYY-MM-DD-H와 같이 입력해주세요. ")

bot.run(Token)
