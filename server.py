#import discord
from chatterbot import ChatBot
#from chatterbot.filters import get_recent_repeated_responses
from chatterbot.response_selection import get_random_response
import discord

chatbot = ChatBot("Kaladin",  
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": get_random_response,
            "filters": ["chatterbot.filters.get_recent_repeated_responses"],
            'maximum_similarity_threshold': 0.7,
            'default_response': 'I don\'t have a response for that. What else can we talk about?'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ],

)

token = ""

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    resp = chatbot.get_response(message.content)
    await message.channel.send(resp)

client.run(token)
