# BSY-Black-Gate

## Overview
In this project there are implemented bot and controller codes who communicate using the gist.github.com only. Using the controller user can send defined commands to the bot using bots id (can be listed using ls_bots command). Each bot has its own post on gist. All bots are listed inside ```CatsIWantToPet.md``` as the name of their post with the link. Using this list, controller can easily find all the bot posts.

Each bot has predefined post with these headings (SAME ORDER AND ### HEADINGS!)  
- Level of cuteness = status code (success, error, reset) for checking if command was completed successfully
- Level of fluffiness = specified command
- Interesting links = for sending small string data
- Image = for sending larger data


## IMPORTANT
The controller and bot communicates via gist.github.com. For that GitHub Personal access token with GIST access is improtant. You have to create a ```token.txt``` file (in this repository root directory) with this token to run the code. 

How to get the Personal access token with GIST access:
  - Click on your personal account profile (top right)
  - Click <b>Settings</b>
  - On the left menu bar go to <b>Developer settings</b> and choose <b>Personal access tokens</b>
  - <b>Generate new token</b> and write a name (note) of your token. The note does not affect the functionality, but choose a note that describes the purpose of the token e.g., <i>GIST_token</i>
  - Set a mark at <b>gist</b> (<i>Create gists</i>) and click on <b>Generate token</b> at the bottom of the page
  - IMPORTANT: The displayed token appears only once. Copy it and store it in your GitHub project as a secret and / or locally as an environment variable.



## Bot
**Bot** takes one parameter to run - PATH to directory with ```params.txt``` and ```imgs``` directory. Inside the ```params.txt``` is JSON with bots parameters including name, filename and urls (see example file for more info). Inside the ```imgs``` directory are possible images for use in gist.

After running the bot it reads and stores the parameters from specified PATH. If a bot with the same name already exists in the bot list ("CatsIWantToPet.md" file on gist), the code exits. Otherwise the bot creates a new post for himself and add himself to the bot list. Then he is waiting for commands.

## Controller
**Controller** has two threads, reader and executor. Inside reader thread the controller is waiting for user commands. The commands are stored in command array and are executed in order by executor thread. The executor thread also periodically (every 5 minutes) send ping command to all bots to check if they are still alive.
### Usage 
```
<command name> [bot name] [parameter1 ...]

ls_bots							(lists all currently available bots)
exists							(stop controller)
w  <bot filename> 				(lists users currently logged in)
ls <bot filename> <PATH> 		(list content of specified directory)
id <bot filename> 				(id of current user)
cp <bot filename> <PATH> 		(copy fole from the bot to controller)
exec <bot filename> <PATH> 		(execute a binary inside the bot given the name of the binary)
```

## Commands
All the commands are specified by controller in fluffiness level in the bot post. The status is then reset and controller is checking the status for response status.

## Bots checking
The controller sends ```ping``` command to all the bots every 5 minutes (the command is specified in the fluffiness level). If bot receives ping command, he change its status to success emoji. If the status is still reset after 15 seconds, controller removes the bot from bot list the and removes its bots post as well.