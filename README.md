Run AutoChat Bot
Create an API Key:

Go to Gaia API Keys and create a new key. Save the API key somewhere since you won't be able to access it again.
Download the Python Script:

Run:
curl -L -o gaiabot.py https://github.com/0xmoei/Gaianet-AI/raw/main/gaiabot.py
Run the Script:

Open a screen to run the bot in the background, so if you closed the terminal, it won't stop:
screen -S gaiabot
Now run this command to start the bot:
python3 gaiabot.py
Enter your Gaia API key when prompted.
To minmize the screen, press Ctrl+A+D
To return the screen, enter command: screen -r gaiabot
To stop and kill the bot, press CTRL+C inside the screen & run this command: screen -XS gaiabot quit
It might gives you failed attempts which is because of networks floods, as you can see in the picture that I may get a successfull response after 3 or more attempts# GaiaNet-AI
