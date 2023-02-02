# **HelloBot**
*This is pet-project for python learning  is called HelloBot.*

## QuickStart
For successful launch the bot, you will need a [Telegram-token](https://core.telegram.org/bots) as variable `BOT_TOKEN = "your token"`,<br>
Google Analytics url

## Making Docker Container
Project contains Dockerfile that will help you to make container.
After clone repository use  `docker build .` command from project directory to make docker image.
And after docker image creation use `docker run --env-file .env IMAGE ID` where IMAGE ID is id of your early created docker image(to see IMAGE ID use `docker images` command) and .env is file with your enviroment variables.

## Making .env file
.env file must contain enviroment variables, looks like:<br>
BOT_TOKEN=your token<br>
DB_URL=your url<br>
OWNER_USER_ID=your telegram id<br>
SHARE_URL=your url google analytics<br>