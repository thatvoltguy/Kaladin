# Kaladin - Chatbot based on your own Text Messages
Create a Personal Assistant that talks and responds like you.
Help to automate your life.

### Corpus Generation 
In order to get your corpus files for you need to use bagoup
	brew install bagoup
	bagoup -i chat.db -s me

### How to train
	python3 train.py training_sets/example.txt

### Enter Discord token in server.py file as "token" variable
	token = ""

### Run Bot
	python3 server.py

### Database will stay updated between runs so no need to save state

### You can intereact on command line using interact.py
