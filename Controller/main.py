import time
from Controller import gist
from Controller.Commands import alive

# Prepare helper folders
gist.init_folders()

# Define parameters
BOT_LIST = "CatsIWantToPet.md"
GIST_API = gist.get_gist_api()

# Create init bot list on gist
gist.init_bot_list(GIST_API, BOT_LIST)

# TO BE CONTINUED
while True:     # TODO not True but check user exit...?
    # Reset bots
    print("Starting reset ...")
    alive.reset_bots(GIST_API, BOT_LIST)
    time.sleep(15)
    # Check if bots are alive -> remove dead
    print("Removing dead ...")
    alive.check_bots(GIST_API, BOT_LIST)


# Cleanup all helper folders
# gist.clean_up_folders()
