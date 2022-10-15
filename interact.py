#import discord
from chatterbot import ChatBot
#from chatterbot.filters import get_recent_repeated_responses
from chatterbot.response_selection import get_most_frequent_response

chatbot = ChatBot("Kaladin",  
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": get_most_frequent_response,
            "filters": ["chatterbot.filters.get_recent_repeated_responses"]
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ],

)

while True:
    try:
        user_input = input()

        bot_response = chatbot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
