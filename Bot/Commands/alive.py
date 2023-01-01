import random
import sys

from Bot import gist
from Bot import emojis


def i_am(gist_api, filename):
    # Check status (level of cuteness)
    content = gist.get_raw(gist_api, filename)
    status = content.split('\n')[1].split("cuteness")[-1].strip()
    if status in emojis.status_code['reset']:
        content_split = content.split('\n')
        content_split[1] = "### Level of cuteness " + random.choice(emojis.status_code['success'])
        gist.update_gist(gist_api, filename, "\n".join(content_split))
        print("{} SAYS: DO NOT KILL ME PLS".format(filename))




