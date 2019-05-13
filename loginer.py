import getpass

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions.string import StringSession

string = "1BJWapzMBu2Xy-XhWR24vNIzWOSW3Cg6F6_xeUyhzBEj9D5M_gHLKKab19o7aCpYSbCagZY8EHVA3x37KQnuuwGVMH91HTnhNFbxGoT_Pxb29ZtU4zGOj7ItRCT754YAfqF_ko0RCv88UiFsAFnnfAE3JbG1mktbUWypINVAd4TGocyZ_AUJSeeP8o6mpvahgRk5_EMVQRmTWZQPgVU_wwTAYQufg56BwzAQjYFAYJRi4O7mYedsJpJ5vjYeOR8k0JiPiR5gvIqk1gourZliROwODUZh5IIzkTvFxxflFH_oEJm_ESL-FMxs78960EpKqC4f4gckOYwuFn1DnHmhNVaWLNvHR8Gc="
client = TelegramClient(
        StringSession(string=string),
        api_id=818262,
        api_hash='ad7bc7b2bfcc08ffd16f59e73bf3630d',
    )
client.connect()
client.sign_in(password='Ing0dwetru5T01031988')
[print(dialog) for dialog in client.iter_dialogs() ]