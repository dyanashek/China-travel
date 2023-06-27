# Information bot
## Изменить язык: [Русский](README.md)
***
A telegram bot representing the services of a company for the delivery of goods from China.
## [DEMO](README.demo.md)
## [LIVE](https://t.me/ChinaTrevel_bot)
## Functionality:
1. Navigation menu to answer the most popular questions
2. Distribution of users between managers
3. Calculation of the cost of delivery (forwarding a message to the corresponding chat and receiving a response from it)
4. Collecting statistics on users, tracking visited sections
5. Notification of the assigned manager about a user who has not contacted him within 15 minutes from the start of using the bot
## Commands:
**For convenience, it is recommended to add these commands to the side menu of the bot using [BotFather](https://t.me/BotFather).**
- /menu - start menu;
- /stat - displays information about all users who have used the bot for the first time since the last time this command was entered (only **DIRECTOR_ID** is available);
- /user - the command that the manager enters, indicating the nickname of the user who contacted him (counts the user in the manager's statistics, **MANAGER_ID** is available);
## Installation and use:
- Create an .env file containing the following variables:
> the file is created in the root folder of the project
   - specify the bot's telegram token in the file:\
   **TELEGRAM_TOKEN**=TOKEN
   - Bot ID (numbers in the token):
   **BOT_ID**=ID
   - **DIRECTOR_ID** contains the ID of the user who has access to execute the stat command. (for example: DIRECTOR_ID=1234)
> To determine the user ID, you need to send any message from the corresponding account to the next [bot] (https://t.me/getmyid_bot). The value contained in **Your user ID** - the user ID
- Add managers to china_travel.db in the managers table according to the fields (manager id, his name, nickname in telegram)
- Install the virtual environment and activate it (if necessary):
> Installation and activation in the root folder of the project
```sh
python3 -m venv venv
source venv/bin/activate # for macOS
source venv/Scripts/activate # for Windows
```
- Install dependencies:
```sh
pip install -r requirements.txt
```
- Run project:
```sh
python3 main.py
```