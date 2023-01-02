from Controller import gist


def list_current_bots(gist_api, bot_list):
    to_print = "Name\t\t\tFilename\t\t\tId\n"
    bot_list_content = gist.get_raw(gist_api, bot_list)
    lines = bot_list_content.split('\n')
    for line in lines:
        if not line.startswith('###'):
            continue

        # Name, Filename, Id
        name = line.split("[")[1].split("]")[0]
        filename = line.split("(")[1].split("#")[1].rstrip(')')
        id = line.split("(")[1].split("#")[0].split("/")[-1]

        to_print += name + "\t\t" + filename + "\t\t" + id + "\n"

    print(to_print)
