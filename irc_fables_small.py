#!python3


from time import sleep

import irc.bot
import irc.strings


class RomanIrcBot(irc.bot.SingleServerIRCBot):

    def __init__(self, boucle, channel, nickname, realname, server, port=6667):
        super().__init__([(server, port)], nickname, realname)

        self.boucle = boucle
        self.channel = channel
        self.question = "Qui es-tu ?"
        self.response = "I'm stupid"

        self.num = 0
        self.quest_rep = {}
        self.alive = 1
        self.init = 0
        self.stop = 0

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        print("on_nicknameinuse")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("Welcome on #labomedia IRC")

    def on_pubmsg(self, c, e):

        # a est le messge reçu
        msg = e.arguments[0].split(":", 1)

        i_am = irc.strings.lower(self.connection.get_nickname())
        # Si le message commence par le nickname
        if len(msg) > 1 and irc.strings.lower(msg[0]) == i_am:
            # La commande est la suite du nickname: texte_du_message
            self.do_command(e, msg[1].strip())

    def do_command(self, e, cmd):

        if "mort aux vaches" in cmd:
            self.alive = 0
            print("Stop du bot irc")
            self.die()
        elif "tais_toi" in cmd:
            self.new == 0
            self.num = 1
            self.init = 0
            self.quest_rep = {}
            self.stop = 1
            print("Stop ...")
        else:
            if self.boucle:
                self.stop = 0
                question = cmd
                self.new = 0
                self.num = 1
                self.init = 1
                self.quest_rep = {self.num: question}
                print("Relance ...")
            else:
                self.question = cmd
                print(f"Question: {self.question}")
                self.quest_rep[self.num] = [self.question]
                while len(self.quest_rep[self.num]) == 1:
                    sleep(0.01)
                if len(self.quest_rep[self.num]) == 2:
                    rep = self.quest_rep[self.num][1]
                    for item in rep:
                        lines = item.splitlines()
                        for line in lines:
                            self.send_pubmsg(line)
                            sleep(4)
                    self.num += 1


    def send_pubmsg(self, msg):
        """msg est un str sans \n"""

        self.connection.privmsg("#labomedia",  msg)
        sleep(0.1)


def fable_irc_bot_main():

    server = "irc.freenode.net"
    port = 6667
    channel = "#labomedia"
    nickname = "fable"
    realname = "De La Fontaine"

    boucle = 0
    bot = RomanIrcBot(boucle, channel, nickname, realname, server, port)
    bot.start()




if __name__ == "__main__":
    fable_irc_bot_main()
