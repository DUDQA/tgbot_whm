Telegram game bot "WhoHasMore?"

A little pet project where I can combine business and pleasure.

Game principal:
1. You are sent two answer options in the form of two photos and buttons to them. Your task is to decide which of these two songs has more streams on Spotify.
2. If your answer is correct you get a message about it and recieve next two options. Previous options are deleted.
If you're wrong then you will receive a message with your score and a "Retry" button.


Operation principal:
1. Scraping the necessary data from Spotify website (bs4)
2. Preparing data and then loading it to the database (psycopg2)
3. Interaction with the telegram user (AIOgram, psycopg2)


If I have enough time and desire, another genres will be added
