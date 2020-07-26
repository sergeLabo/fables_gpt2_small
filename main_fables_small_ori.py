#!python3


from time import sleep
import threading
from random import randint

from irc_fables_small import RomanIrcBot
from testing_fables_small import Roman


# Serveur IRC
SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#labomedia"
NICKNAME = "Fables"
REALNAME = "de Jean De La Fontaine"


class Bidon:

    def __init__(self):
        self.num = 0
        self.quest_rep = {}
        self.quest_rep[0] = ["L'oiseau et le lion"]
        self.alive = 1

    def send_pubmsg(self, what):
        pass


def get_reponse_new_question(text, question):
    """
    lines = ['Romeo n'est pas gentil',
             'et juliette aussi, elle esp']
    reponse['Romeo n'est pas gentil',
             'et juliette aussi, elle']
    new_question = 'est pas gentil et juliette aussi, elle'
    """

    lines = text.splitlines()

    # Pas d'envoi du dernier mot de la dernière ligne
    # La dernière ligne = lines[-1]
    # La dernière ligne sans le dernier mot en liste
    last_line_list = lines[-1].split(" ")[:-1]
    # Conversion de la liste de mots en une ligne
    last_line = ""
    for mot in last_line_list:
        last_line += mot + ' '
    # Suppression du dernier espace
    last_line = last_line[:-1]
    # Set de la dernière ligne
    lines[-1] = last_line

    # la réponse en str
    resp = ""
    for item in lines:
        resp += item + '\n'
    # sans le \n de la dernière ligne
    resp = resp[:-2]
    # Sauf le prompt = question
    resp = resp.replace(question, "")
    # La réponse en liste
    reponse = resp.splitlines()

    # La nouvelle question
    mots = resp.replace("\n", " ").split(" ")
    # Récup de x mots
    nbmots = 40
    new_question_list = mots[-nbmots:]
    new_question = ""
    for mot in new_question_list:
        new_question += mot + ' '

    return reponse, new_question


def generate_local(vocab_size):

    bot = Bidon()
    roman = Roman(vocab_size)
    print("\n"*30)

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        if bot.new == 0 and bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    bot.new = 1
                    try:
                        question = bot.quest_rep[num][0]
                    except:
                        question = "Quoi"
                        len_max = 50
                        temp = 1
                    if len(question) > 50:
                        question = "Quoi"
                    # Il y a une nouvelle question
                    bot.new = 1
                    print('\n\n', question)
        if bot.new == 1:
            len_max = 60
            temp = 0.5
            try:
                text_list = roman.get_irc_response(question, len_max, temp)
            except:
                text_list = ["Je ne comprends pas la question!"]
            # text_list[0] est le 1er texte généré
            reponse, new_question = get_reponse_new_question(text_list[0],
                                                             question)

            for line in reponse:
                bot.send_pubmsg(line)
                sleep(1)
                print(line)

            # Nouvelle question
            sleep(10)
            bot.num += 1
            num = bot.num
            bot.quest_rep[num] = [new_question]  # liste
            question = new_question # str


def generate_irc(vocab_size, boucle):
    bot = RomanIrcBot(boucle, CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
    thread_dialog = threading.Thread(target=bot.start)
    thread_dialog.setDaemon(True)
    thread_dialog.start()
    roman = Roman(vocab_size)

    sleep(1)
    bot.new = 0
    while bot.alive:
        num = bot.num
        sleep(0.1)
        if not bot.stop:
            print("1")
            if bot.new == 0 and bot.quest_rep:
                print("2")
                if not bot.init:
                    print("3")
                    if len(bot.quest_rep) == num + 1:
                        print("4")
                        if len(bot.quest_rep[num]) == 1:
                            print("5")
                            print("début", bot.quest_rep)
                            try:
                                question = bot.quest_rep[num][0]
                            except:
                                question, len_max, temp = "Quoi", 50, 1
                            # Il y a une nouvelle question
                            bot.new = 1
                else:
                    print("Relance", bot.quest_rep)
                    try:
                        question = bot.quest_rep[1]
                    except:
                        question = "Quoi"
                    # Il y a une nouvelle question
                    bot.new = 1
                    bot.init = 0

                # Seulement les 100 premiers
                question = question[:100]
                sleep(1)
                bot.send_pubmsg(question)
                print('\n\nNouvelle question:', question, '\n\n')

            if bot.new == 1:
                len_max, temp = 60, 1
                try:
                    text_list = roman.get_irc_response(question, len_max, temp)
                except:
                    text_list = ["Je ne comprends pas la question!"]
                # text_list[0] est le 1er texte généré
                reponse, new_question = get_reponse_new_question(text_list[0],
                                                                 question)

                for line in reponse:
                    bot.send_pubmsg(line)
                    sleep(4)
                    print(line)

                # Boucle
                if boucle:
                    if not bot.new and not bot.init:
                        num = bot.num = 1
                        bot.quest_rep[num] = [new_question]  # liste
                        question = new_question # str
                else:
                    bot.num += 1




if __name__ == '__main__':
    vocab_size = 50257

    # #generate_local(vocab_size)

    boucle = 0
    generate_irc(vocab_size, boucle)
