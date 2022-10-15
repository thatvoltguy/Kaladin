from locale import currency
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import datetime
import glob

from sqlalchemy import false

def get_corpus_from_file(filename):
    conversations = []
    curr_conversation = []
    conv_init_words = ["hi", "hey", "heyy", "heyyy", "how", "yo", "yoo", "yooo", "going", "wyd", "been"]
    depth = 0
    past_speaker = ""
    in_conversation = False
    lock = set()
    
    with open(filename, "r") as f:
            text = f.readlines()
            c_date = re.search(r'.(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})] ([a-zA-Z\d+]*):', text[0])
            last_date = datetime.datetime.strptime(c_date.group(1), '%Y-%m-%d %H:%M:%S')

            for line in text:
                line = line.replace("’", "\'")
                line = ''.join([i if ord(i) < 128 else ' ' for i in line]).strip()
                match = re.search(r'.(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})] ([a-zA-Z\d+]*):', line)
                if match:
                    #print(match)
                    speaker = match.group(2)
                    date = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                    message = line.replace(match.group(0), '')
                    message = message.strip()
                    if message:
                        time_delta = (date - last_date).total_seconds() / 3600
                        list_of_message_words = [word.lower() for word in re.split('\s+', message)]
                        matched_init_word = set(conv_init_words) & set(list_of_message_words)
                        has_init_word = True if matched_init_word else False
                        #has_time_delta = True if time_delta > 36 else False
                        has_question = True if "?" in message else False
                        new_speaker = True if speaker != past_speaker else False

                        #print(str(depth) + " - " + str(in_conversation))
                        #print("new speaker: " + str(new_speaker) + ", New speaker: " + str(speaker) +  ", older speaker: " + str(past_speaker))
                        
                        if depth >= 0 and not in_conversation:
                            if (has_init_word or has_question):
                                lock = (matched_init_word, has_question)
                                #print(has_time_delta)
                                in_conversation = True
                                #print(str(matched_init_word) +" - "+ message)
                                curr_conversation.append(message)
                                depth += 1
                            continue

                        if (depth < 3 and depth >= 1) and in_conversation:
                            if not new_speaker:
                                curr_conversation.append(message)
                            else: 
                                curr_conversation.append(message)
                                depth += 1
                            continue
                        
                        if depth >= 3 and in_conversation:
                            curr_conversation.append(message)
                            #conversations.append((lock, curr_conversation))
                            conversations.append(curr_conversation)
                            curr_conversation = []
                            depth = 0
                            in_conversation = False

                        if new_speaker:
                            past_speaker = speaker
                        last_date = date
    return conversations

def main():
    master_convo = []
    stormlight = ["Kaladin, say the words", "Life before death...Strength before weakness...Journey before destination"]
    training_files = glob.glob("./training_sets/*.txt")
    for f in training_files:
        print("Generating corpus for " + str(f))
        temp_convo = get_corpus_from_file(f)
        master_convo += temp_convo


    with open("test.txt", "w") as f:
        for conv in master_convo:
            f.write("-----------New Convo-------------\n")
            f.write(str(conv) + "\n")

    chatbot = ChatBot("Kaladin")
    trainer = ListTrainer(chatbot)
    count = 0
    total = str(len(master_convo))
    for convo in master_convo:
        print("Training Count: " + str(count) + " : " + total)
        trainer.train(convo)
        count += 1
    trainer.train(stormlight)

    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train(
        "chatterbot.corpus.english"
    )


main()