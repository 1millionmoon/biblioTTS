from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
import asyncio
from pprint import pprint
from uuid import UUID
import configparser

config = configparser.ConfigParser()
config.read('config.txt')
debug = config['twitch']['debug']
APP_ID = config['twitch']['client_id']
APP_SECRET = config['twitch']['client_secret']

TARGET_CHANNEL = config['twitch']['channel']
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]
if (debug=='True'):
    USER_SCOPE = [AuthScope.CHANNEL_MODERATE, AuthScope.CHANNEL_READ_REDEMPTIONS]

async def callback_whisper(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    pprint(data)

async def run_example():
    # setting up Authentication and getting your user id
    print('starting program...')
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
    token, refresh_token = await auth.authenticate()
    # you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))

    # starting up PubSub
    pubsub = PubSub(twitch)
    pubsub.start()
    if (debug=='False'):
        reward_list = await twitch.get_custom_reward(user.id, reward_id=None, only_manageable_rewards=False)
        pprint(reward_list)

    # you can either start listening before or after you started pubsub.
    if (debug=='True'):
        uuid = await pubsub.listen_chat_moderator_actions(user.id, user.id ,callback_whisper)
    else:
        uuid = await pubsub.listen_chat_moderator_actions(user.id, user.id ,callback_whisper)
    input('program is running . press ENTER to close...\n')
    print('closing program...')
    # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
    await pubsub.unlisten(uuid)
    pubsub.stop()
    await twitch.close()

asyncio.run(run_example())

