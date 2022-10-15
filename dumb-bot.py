from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response

chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot,
    logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                "response_selection_method": get_most_frequent_response,
                "filters": ["chatterbot.filters.get_recent_repeated_responses"],
                'maximum_similarity_threshold': 0.7,
                'default_response': 'I don\'t have a response for that. What else can we talk about?'
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            }
        ]
)

# Train the chatbot based on the english corpus
#trainer.train("chatterbot.corpus.english")

while True:
    try:
        user_input = input()

        bot_response = chatbot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break