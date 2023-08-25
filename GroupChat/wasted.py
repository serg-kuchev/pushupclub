from dispatcher import bot
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


sp_id = "1KAY73XEKsV4H-TL4jPRqAR6CIm5rIR79ZNkeJEpn0qk"
CREDENTIALS_FILE = 'sportbot-396814-5f4c6812d902.json'
credentials = Credentials.from_service_account_file('sportbot-396814-5f4c6812d902.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)

async def print_wasted():
    result = service.spreadsheets().values().get(spreadsheetId=sp_id, range='Календарь!B3:C3').execute()
    wasted = result.get('values')[0]
    #result = service.spreadsheets().values().get(spreadsheetId=sp_id, range='Календарь!B8:C8').execute()
    #wasted = result.get('values', [])
    wasted_joined = ""
    wasted_joined = '\n'.join(wasted)
    if wasted:
         await bot.send_message(428170144, f"Список провалившихся участников {wasted_joined}")
    await bot.send_message(428170144, 'timed')
