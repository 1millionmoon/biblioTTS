#
#
# helper.py is only examples on how to update the profanity wordlist and reading the config.ini file
#
#
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
    config.read('config.ini')
    return config

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config_example.ini')
    sa = config["twitch"]["redeem_list"]
    print(sa)
