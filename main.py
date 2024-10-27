from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
from uuid import UUID
import asyncio
import shutil
import os 
import sys
import configparser
import better_profanity
import pyttsx3


def init_config(): 
    global TARGET_CHANNEL 
    global APP_ID
    global APP_SECRET 
    global REDEEM_LIST 
    global USER_SCOPE 
    global TEXT_CHAR_LEN 
    global CST_WORDLIST 
    try  :
        config = configparser.ConfigParser()
        config.read('config.ini')

        TARGET_CHANNEL = config['twitch']['channel']
        APP_ID = config['twitch']['app_id']
        APP_SECRET = config['twitch']['app_secret']
        REDEEM_LIST = str(config['twitch']['redeem_list']).lower().replace(" ", "").split(";")
        USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]

        TEXT_CHAR_LEN = int(config['text']['text_character_length'])
        CST_WORDLIST = config['text']['custom_wordlist']

        if not (all([APP_ID,APP_SECRET,TARGET_CHANNEL,REDEEM_LIST,USER_SCOPE,TEXT_CHAR_LEN,CST_WORDLIST])):
            print("Missing value in config.ini")
            raise Exception("Missing value")

    except Exception as e: 
        print("config.ini error")

# Load the customized wordlist by adding it into the original better_profanity library directory 
def custom_profanity_wordlist(custom):
    try : 
        if (CST_WORDLIST=="True"):
            file = "custom_profanity_wordlist.txt"
            dst_folder = os.path.dirname(better_profanity.__file__)
            fullpath = os.path.join(dst_folder, file)

            shutil.copyfile(file, fullpath)
            better_profanity.profanity.load_censor_words_from_file(file)
            print('Using customized profanity wordlist ')
        else:
            print('Not using customized profanity wordlist')
            better_profanity.profanity.load_censor_words() # load default list of words
    except Exception as e :
        print("Custom profanity wordlist error")

def text_filter(text):
    censored_text = text
    try : 
        censored_text = better_profanity.profanity.censor(text)
    except Exception as e: 
        print("Text filter error")
    return censored_text

def call_tts(text):
    try : 
        print("Call TTS : " + text)
        tts_engine = pyttsx3.init("sapi5")
        tts_engine.say(text)
        tts_engine.runAndWait()
        tts_engine.stop()
    except Exception as e: 
        print("Call TTS error")

async def callback_response(uuid: UUID, data: dict) -> None:
    try: 
        if(data["type"]=="reward-redeemed"):
            redemption_data = data["data"]["redemption"]

            for redeem in REDEEM_LIST : 
                if (str(redemption_data["reward"]["title"]).lower().replace(" ", "") == redeem):
                    redeem_text = str(redemption_data["user_input"]).lower()
                    filtered_text = text_filter(redeem_text[:TEXT_CHAR_LEN])
                    call_tts(filtered_text)
                # else :
                    # print("Redeem name doesn't match")
        # else:
        #     print("Type doesn't match")

    except Exception as e :
        print("Callback response error")

async def connect_twitch():
    # setting up Authentication and getting your user id
    print('starting program...')

    try : 
        twitch = await Twitch(APP_ID, APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
        token, refresh_token = await auth.authenticate()

        # you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
    except Exception as e: 
        print("Twitch authentication error")

    # starting up PubSub
    pubsub = PubSub(twitch)
    pubsub.start()

    # you can either start listening before or after you started pubsub.
    try : 
        uuid = await pubsub.listen_channel_points(user.id ,callback_response)
    except Exception as e: 
        print("PubSub listen error")

    input('program is running . press ENTER to stop program...')
    print('\nStopping program...')
    # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
    await pubsub.unlisten(uuid)
    pubsub.stop()
    await twitch.close()
    print('Program stopped')

def main():
    init_config()
    custom_profanity_wordlist(CST_WORDLIST)
    asyncio.run(connect_twitch())

if __name__ == '__main__':
    
    TARGET_CHANNEL = None
    APP_ID = None
    APP_SECRET = None
    REDEEM_LIST = None
    USER_SCOPE = None

    TEXT_CHAR_LEN = None
    CST_WORDLIST = None
    
    main()

    input('press ENTER to close...\n')


