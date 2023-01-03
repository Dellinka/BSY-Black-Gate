# BSY-Black-Gate

## Overview
In this project there are implemented bot and controller codes who communicate using the gist.github.com only. Using the controller user can send defined commands to the bot using bots post filename (can be listed using ls_bots command). Each bot has its own post on gist. All bots are listed inside ```CatsIWantToPet.md``` as the name of their post with the link. Using this list, controller can easily find all the bot posts.

Each bot has predefined post with these headings (SAME ORDER AND ### HEADINGS!)  
- Level of cuteness = status code (success, error, reset) for checking if command was completed successfully
- Level of fluffiness = specified command
- Interesting links = for sending encrypted data (Originally the idea was to send longer/all responses from bot using image with data embedded at the end. However I found out that Gist API does not support binary data)

### How does the communication work?
After sending command to controller, the controller updates command emoji in the Level of fluffiness and reset status emoji in Level of cuteness in defined bot's post. Than he is waiting for a response by checking the status emoji. Bots are checking the status periodically and if the status is changed to reset the bot reads the command emoji. When bot executes defined command he updates the status to success/error and send encrypted response at the end of the last url in post. Controller than sees the status and can read the response from post. As the response can be quite long (it is a problem as gist than show the url instead of the link name) the controller removes it immediately after reading.

For more information on the emojis coding see the ```emojis.py``` in Controller or Bot directory.


## IMPORTANT
The controller and bot communicates via gist.github.com. For that GitHub Personal access token with GIST access is improtant. You have to create a ```token.txt``` file (in this repository root directory) with this token to run the code. 

How to get the Personal access token with GIST access:
  - Click on your personal account profile (top right)
  - Click <b>Settings</b>
  - On the left menu bar go to <b>Developer settings</b> and choose <b>Personal access tokens</b>
  - <b>Generate new token</b> and write a name (note) of your token. The note does not affect the functionality, but choose a note that describes the purpose of the token e.g., <i>GIST_token</i>
  - Set a mark at <b>gist</b> (<i>Create gists</i>) and click on <b>Generate token</b> at the bottom of the page
  - IMPORTANT: The displayed token appears only once. Copy it and store it in your GitHub project as a secret and / or locally as an environment variable.


## How to run the code
Both bot and controller have own run script in their respective directories. The scripts create virtual environment, download all the dependencied from ```requirements.txt``` and run the code.  Run the code using the command below
 -```./run.sh```
 -```./run.sh <PATH_TO_JSON_FILE>``` 


## Bot
**Bot** takes one parameter to run - PATH to json file with bot parameters. There are two examples in Cats directory. Inside the ```<params>.json``` is JSON with bots parameters including name, filename and urls. In the urls array has to be at least one url, as the bot use it to communicate responses to commands (see example files in Cats directory for more info).

After running the bot it reads and stores the parameters from specified parameters file defined in PATH. If a bot with the same name already exists in the bot list ("CatsIWantToPet.md" file on gist), the code exits. Otherwise the bot creates a new post for himself and add himself to the bot list. Then he is waiting for commands.

## Controller
**Controller** has two threads, reader and executor. Inside reader thread the controller is waiting for user commands. The commands are stored in command array and are executed in order by executor thread. The executor thread also periodically (every 5 minutes) send ping command to all bots to check if they are still alive.
### Usage 
```
<command name> [bot name] [parameter1 ...]

help                          (list possible commands)
ls_bots							          (lists all currently available bots)
todo                          (list all the queued commands)
exit  							          (stop controller)
ping                          (ping all bots manually)
w  <bot filename> 				    (lists users currently logged in)
ls <bot filename> <PATH> 	    (list content of specified directory)
id <bot filename> 				    (id of current user)
cp <bot filename> <PATH> 		  (copy fole from the bot to controller)
exec <bot filename> <PATH> 		(execute a binary inside the bot given the name of the binary)
```

## Bots checking
The controller sends ```ping``` command to all the bots every 5 minutes (the command is specified in the fluffiness level). If bot receives ping command, he change its status to success emoji. If the status is still reset after 15 seconds, controller removes the bot from bot list the and removes its bots post as well.