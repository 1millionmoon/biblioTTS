# from twitchAPI.twitch import Twitch
# from twitchAPI.helper import first
# import asyncio


# async def twitch_example():
#     app_id = 'bhjavszn7zzzz0m5celjhv4sbshb7y'
#     app_secret = 'r62rh70vm8efzwpqm89r4c7fx9wo68'
#     # initialize the twitch instance, this will by default also create a app authentication for you
#     twitch = await Twitch(app_id, app_secret)
#     # call the API for the data of your twitch user
#     # this returns a async generator that can be used to iterate over all results
#     # but we are just interested in the first result
#     # using the first helper makes this easy.
#     user = await first(twitch.get_users(logins='1millionmoon'))
#     # print the ID of your user or do whatever else you want with it
#     print(user.id)

# # run this example
# asyncio.run(twitch_example())

from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
import asyncio
from pprint import pprint
from uuid import UUID

APP_ID = 'bhjavszn7zzzz0m5celjhv4sbshb7y'
APP_SECRET = 'r62rh70vm8efzwpqm89r4c7fx9wo68'
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]
TARGET_CHANNEL = '1millionmoon'

async def callback_whisper(uuid: UUID, data: dict) -> None:
    print('got callback for UUID ' + str(uuid))
    pprint(data)


async def run_example():
    # setting up Authentication and getting your user id
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
    token, refresh_token = await auth.authenticate()
    # you can get your user auth token and user auth refresh token following the example in twitchAPI.oauth
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    user = await first(twitch.get_users(logins=[TARGET_CHANNEL]))

    # starting up PubSub
    pubsub = PubSub(twitch)
    pubsub.start()
    # you can either start listening before or after you started pubsub.
    uuid = await pubsub.listen_channel_points(user.id, callback_whisper)
    input('press ENTER to close...')
    # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
    await pubsub.unlisten(uuid)
    pubsub.stop()
    await twitch.close()

asyncio.run(run_example())

