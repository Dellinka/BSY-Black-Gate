import random
import sys

from Bot import gist
from Bot import emojis


def set_alive(gist_api, filename):
    """
    Set level of cuteness to success emoji to show that bot si still alive.

    :param gist_api:
    :param filename:
    :return: None
    """
    # Check status (level of cuteness)
    content = gist.get_raw(gist_api, filename)
    content_split = content.split('\n')
    content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['success'])
    gist.update_gist(gist_api, filename, "\n".join(content_split))
    print("{} SAYS: DO NOT KILL ME PLS".format(filename))




