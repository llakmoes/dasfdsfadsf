from telethon import TelegramClient, sync
from telethon.sessions.string import StringSession
import re
api_id = 335756
api_hash = '1143152ae67c4bf49acdcc3dffca3b25'
string = '1BJWapzMBu4A0TgNJJFEGRMVdhyh5mAwPSI0EW-C02usm9P0y3z5lYGWq5GRkb-TDwPXPL5_lSOaGV1OZ6agHV6aqKu8PJA_y7R2-W5J--p1lVr3FCy3DiIjqAMMBxzf5LMUy99_em-YbxZuzTub_L2Y5SY9GhpvAz4-MoJaWA9CjGWZ3Kao5ULPiSN3VJOVQCeQ6RDzsLc1QcW1oWf4mZCgU-XGyir0BVfgAvlSgKkTa67bY4OKVvflrjzImwOzEN6FeLgU1GRG9iRNFzGraqfSpffDb9wGt2Eub_Y8Vgfqzm3GZkemEtMTWqJUbA3sEFgfYAHX29Jiyt5tXCNu7wPl8dc_yEB0='
with TelegramClient(StringSession(string), api_id, api_hash) as client:
    client.connect()
    for chat in client.iter_dialogs():
        getmessage = client.get_messages(chat.id, limit=400)
        print(chat.name)
        print("*"*10)
        for message in getmessage:
            print(message.message)
