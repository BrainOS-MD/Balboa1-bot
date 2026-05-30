import gspread
import os

os.chdir('/Users/chrissimon/balboa1-bot')

gc = gspread.oauth(
    credentials_filename='./credentials/oauth_credentials.json',
    authorized_user_filename='./credentials/authorized_user.json'
)
sh = gc.open_by_key('1GT0JlOm0ehyycaQVkf93WjhYKrAJsN6ZzC_0c7ZGrOQ')
print('Auth successful. Worksheets:', [ws.title for ws in sh.worksheets()])
