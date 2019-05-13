from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 335756
api_hash = '1143152ae67c4bf49acdcc3dffca3b25'
string = '1BJWapzMBuxG6fNwK9qk0ptber5aHh4l3ZaDHKxXXDvq2rPPWo' \
         'oOVllCdz2Dn_DRAaawfY3ut9rHAlC1RMDcDxtWGyskZGFB1E2Mq' \
         'pJp7RjrAuLQBosV96qq4chwDUY_5S5eVBxeJZAdPNX3GSDw5jh6' \
         'yU3W_i61u7XvqjUnnP3ov1Eehsl06PhOvroWbjmLcMTnAq0Dc6Yd' \
         'H2crYIniHSZpxC0v-Gxj86JuWIZmvlKqCWLWtUvmXJzlifZShUwLn' \
         '1rYLNTyo5pgdSJfV07uJbHU_b3PmcDzlhmyU-vCt9oEJyctvIPjlUsKaqziB_IR_AQ8O6UD44SwZQ3g0vKhM8e7AorYUw2c= '
phone_number = '+380660119000'

client = TelegramClient(StringSession(), api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    code = input("Код")
    me = client.sign_in(phone=phone_number, code=code)
    print(client.session.save())