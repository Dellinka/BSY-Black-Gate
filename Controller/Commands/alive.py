import random
import sys

from Controller import gist
from Controller import emojis


def reset_bots(gist_api, bot_list):
    """
    Add reset emoji to all the bots' status (level of cuteness).

    :param gist_api:
    :param bot_list:
    :return: None
    """
    # Reset status code (level of cuteness)
    bot_list_content = gist.get_raw(gist_api, bot_list)
    lines = bot_list_content.split('\n')
    for line in lines:
        if not line.startswith('###'):
            continue

        # Change level of cuteness to reset emoji
        filename = line.split("(")[1].split("#")[1].rstrip(')')
        bot_content = gist.get_raw(gist_api, filename)
        content_split = bot_content.split('\n')
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['reset'])
        gist.update_gist(gist_api, filename, "\n".join(content_split))

    print("Reset done ({} bots in the list)".format(len(lines) - 1))


def check_bots(gist_api, bot_list):
    """
    Check status code (level of cuteness) -> if still reset -> kill them

    :param gist_api:
    :param bot_list:
    :return: None
    """
    new_bot_list_split = []
    bot_list_content = gist.get_raw(gist_api, bot_list)
    lines = bot_list_content.split('\n')
    for line in lines:
        if not line.startswith('###'):
            new_bot_list_split.append(line)
            continue

        # Check status
        filename = line.split("(")[1].split("#")[1].rstrip(')')
        bot_content = gist.get_raw(gist_api, filename)
        status = bot_content.split('\n')[1].split("cuteness")[-1].strip()
        if status in emojis.status_code['reset']:
            # DEAD -> KILL IT (remove post, do not add to bot list)
            print("KILLING {}".format(filename), file=sys.stderr)
            gist_api.delete_gist(gist_id=line.split("(")[1].split("#")[0].split("/")[-1])
        else:
            new_bot_list_split.append(line)

        # Update bot list
        gist.update_gist(gist_api, bot_list, "\n".join(new_bot_list_split))
        print("ALL DEAD GONE ({} still alive)".format(len(new_bot_list_split) - 1))


