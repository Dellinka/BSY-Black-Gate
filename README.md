# BSY-Black-Gate

## Usage 
```
<command name> [bot name] [parameter1 ...]

ls_bots					(lists all currently available bots)
w  <bot id> 			(lists users currently logged in)
ls <bot id> <PATH> 		(list content of specified directory)
id <bot id> 			(id of current user)
cp <bot id> <PATH> 		(copy fole from the bot to controller)
exec <bot id> <PATH> 	(execute a binary inside the bot given the name of the binary)
```

## Overview
In this project there are implemented bot and controller codes who communicate using the gist.github.com only. Using the controller user can send defined commands to the bot using bots id (can be listed using ls_bots command). Each bot has its own post on gist. All bots are listed inside ```CatsIWantToPet.md``` as the name of their post with the link. Using this list, controller can easily find all the bot posts.

Each bot has predefined post with these headings (SAME ORDER AND ### HEADINGS!)  
- Level of cuteness = status code (success, error, reset) for checking if command was completed successfully
- Level of fluffiness = specified command
- Interesting links = for sending small string data
- Image = for sending larger data

## Bot
**Bot** takes one parameter to run - PATH to directory with ```params.txt``` and ```imgs``` directory. Inside the ```params.txt``` is JSON with bots parameters including name, filename and urls. Inside the ```imgs``` directory are possible images for use in gist.

After running the bot it reads and stores the parameters from specified PATH. If a bot with the same name already exists in the bot list ("CatsIWantToPet.md" file on gist), the code exits. Otherwise the bot creates a new post for himself and add himself to the bot list. Then he is waiting for commands.

## Controller
**Controller** has two threads, reader and executor. Inside reader thred the controller is waiting for user command. The commands are stored in command array and are executed in order by executor thread. The executor thread also periodically (every 5 minutes) send ping command to all bots to check if they are still alive.

## Commands
All the commands are specified by controller in fluffiness level in the bot post. The status is then reset and controller is checking the status for response status.

### Bots checking
The controller sends ```ping``` command to all the bots every 5 minutes. The command is specified in the fluffiness level. If bot receives ping command, he change its status to success emoji. If the status is still reset after 15 seconds, controller removes the bot from bot list the and removes its bots post as well.