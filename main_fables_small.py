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


def improve_resp(text_list):
    """text_list =
    ["Le lion et la souris, le ver, enfin chacun\nAille puiser son âme en un
    trésor commun :\nToutes sont donc de même trempe ;\nMais agissant
    diversement\nSelon l'herbe menue,\nSelon les laissa faire, et se
    pique\nN'une s'une si chère Epouseentraimaient,\nJet"]
    """

    # #lines = text_list[0].splitlines()
    # ## Pas d'envoi du dernier mot de la dernière ligne
    # ## La dernière ligne = lines[-1]
    # ## La dernière ligne sans le dernier mot en liste
    # #last_line_list = lines[-1].split(" ")[:-1]
    # ## Conversion de la liste de mots en une ligne
    # #last_line = ""
    # #for mot in last_line_list:
        # #last_line += mot + ' '
    # ## Suppression du dernier espace
    # #last_line = last_line[:-1]
    # ## Set de la dernière ligne
    # #lines[-1] = last_line

    # ## la réponse en str
    # #resp = ""
    # #for item in lines:
        # #resp += item + '\n'
    # ## sans le \n de la dernière ligne
    # #resp = resp[:-2]

    phrase = text_list[0].split(".")

    # la réponse en str
    resp = ""
    # Suppression de la dernière phrase
    for item in phrase[:-1]:
        resp += item + '.\n'
    # ## sans le \n de la dernière ligne
    # #resp = resp[:-2]

    # La réponse en liste
    reponse = resp.splitlines()

    return reponse




def generate_irc(vocab_size, boucle):

    bot = RomanIrcBot(boucle, CHANNEL, NICKNAME, REALNAME, SERVER, PORT)
    thread_dialog = threading.Thread(target=bot.start)
    thread_dialog.setDaemon(True)
    thread_dialog.start()
    roman = Roman(vocab_size)
    sleep(1)

    while bot.alive:
        a = 0
        num = bot.num
        if bot.quest_rep:
            if len(bot.quest_rep) == num + 1:
                if len(bot.quest_rep[num]) == 1:
                    a = 1
                    try:
                        print(bot.quest_rep)
                        # 100 maxi, question est le 1er item de
                        question = bot.quest_rep[num][0][:100]
                    except:
                        question = "Quoi"


        if a == 1:
            len_max = 120
            temp = 1
            try:
                text_list = roman.get_irc_response(question, len_max, temp)
            except:
                text_list = ["Je ne comprends pas la question!"]

            # Envoi de la réponse
            print("\nQuestion n°:", num)
            print("Question:", bot.quest_rep[num])
            print("\nAvant amélioration:", text_list[0])
            reponse = improve_resp(text_list)
            print("\nRéponse sans le dernier mot:", reponse)
            bot.quest_rep[num].append(reponse)


if __name__ == '__main__':
    vocab_size = 50257
    boucle = 0
    generate_irc(vocab_size, boucle)
