import os
import sys

import requests
import gistyc


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
    Get content of the post

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
    f = open("tmp/" + filename, "w")
    f.write(content)
    f.close()
    gist_api.update_gist('tmp/' + filename)
    os.remove('tmp/' + filename)


def init_folders():
    # Create tmp dir if not exists
    if not os.path.exists('tmp'):
        os.mkdir('tmp')


def clean_up_folders():
    os.rmdir('tmp')
