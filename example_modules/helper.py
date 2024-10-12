import shutil
import os 
import sys
import better_profanity

def update_profanity_wordlist(flag=True):
    if (flag==True):
        file = "updated_profanity_wordlist.txt"
        dst_folder = os.path.dirname(better_profanity.__file__)
        fullpath = os.path.join(dst_folder, file)

        shutil.copyfile(file, fullpath)
        print('Profanity Wordlist Updated')
    else:
        print('No Update Profanity Wordlist')

def read_config():
    config = configparser.ConfigParser()
    config.read('config.txt')
    # chat = twitch.Chat(channel=config['twitch']['channel'],
    #                    nickname=config['twitch']['nickname'],
    #                    oauth=config['twitch']['oauth'],
    #                    helix=twitch.Helix(client_id=config['twitch']['client_id'],
    #                        client_secret=config['twitch']['client_secret'],
    #                        use_cache=True))
    # chat.subscribe(handle_message)
    # print('Twitch Chat connected. Ready for the jobs.')
    return config

# if __name__ == '__main__':
#     main()
