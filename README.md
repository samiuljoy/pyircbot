> [!NOTICE]
> # ⚠️ Update, December 2024: Account Migration to [github.com/samiulahmedjoy](https://samiulahmedjoy)

## A basic IRC bot written in Python 3.9

### Capabilities;

* Invoke the bot with a `!hello` message/command and see it reply back to you

* Show the time with `!time` command

* Show the weather with `!weather` or `!what is the weather?` command (output may vary)

* Ask the bot it's name by invoking `!what is your name?`

* Show Wikipedia contents for a search term, for example, `!wiki russia` for a short summary about Russia

* Show the google search result of a thing by invoking `!google russia`

* Show the meaning of a term/word by invoking dictionary command, `!dic ecstasy`

### Working on;

* Show the last seen status of a user

* Do `sed` substitutions on PRIVMSG's

* Addquote for a user

* Implementing ssl on port 6697

* Making it more compatible with other servers, for now it works on LiberaChat

* Code Refactor

### Library/Module Dependencies

* requests (for making requests to servers)
* ntplib (for time command)
* curl (self explanatory)
* googleapiclient (for google api)
* BeautifulSoup (for parsing search results)
