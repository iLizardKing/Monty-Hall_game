import random
from tkinter import *


class Monty_Hall_Game:
    def __init__(self, count=3, rounds=20):
        self.count = count
        self.round = 0
        self.rounds_count = rounds
        self.wins = 0
        self.fails = 0
        self.create_form()
        self.get_distribution()

    def create_form(self):
        self.root = Tk()
        self.root.title('Monty Hall paradox')
        self.root.geometry('300x170+300+200')
        self.fnt1 = ('Consolas', '18')
        self.fnt2 = ('Consolas', '12')
        self.score_lab = Label(self.root, font=self.fnt1)
        self.score_lab['text'] = 'Score: {0}-{1}'.format(str(self.wins).zfill(2),
                                                         str(self.fails).zfill(2))
        self.score_lab.pack(side='top')
        self.mess_lab = Label(self.root, font=self.fnt2)
        self.mess_lab['text'] = 'Choose one of several elements:'
        self.mess_lab.pack(side='top')
        self.frame1 = Frame(self.root, height=100, width=300)
        self.frame1.pack(side='top')
        # buttons
        self.option_but1 = Button(self.frame1, text='1', font=self.fnt1, bd=5, width=3,
                                  command=lambda: self.choose(0))
        self.option_but1.pack(side='left')
        self.option_but2 = Button(self.frame1, text='2', font=self.fnt1, bd=5, width=3,
                                  command=lambda: self.choose(1))
        self.option_but2.pack(side='left')
        self.option_but3 = Button(self.frame1, text='3', font=self.fnt1, bd=5, width=3,
                                  command=lambda: self.choose(2))
        self.option_but3.pack(side='left')
        self.buttons = [self.option_but1, self.option_but2, self.option_but3]
        self.next_but = Button(self.root, text='Next', font=self.fnt2, bd=5, width=5,
                               command=self.next_round)
        self.next_but.pack(side='bottom')

    def get_distribution(self):
        self.option_but1['bg'] = '#FFFFFF'
        self.option_but2['bg'] = '#FFFFFF'
        self.option_but3['bg'] = '#FFFFFF'
        self.next_but['state'] = DISABLED
        self.option_but1['state'] = NORMAL
        self.option_but2['state'] = NORMAL
        self.option_but3['state'] = NORMAL
        self.boxes = [0] * self.count
        self.choice = -1
        self.empty_box = -1
        self.round += 1
        prize = random.randint(0, self.count - 1)
        self.boxes[prize] = 1
        print(self.boxes)

    def next_round(self):
        if self.round < self.rounds_count:
            self.get_distribution()
            self.mess_lab['text'] = 'Choose one of several elements:'
        else:
            self.mess_lab['text'] = 'Game is over!'
            self.option_but1['state'] = DISABLED
            self.option_but2['state'] = DISABLED
            self.option_but3['state'] = DISABLED
            self.next_but['state'] = DISABLED

    def choose(self, choice):
        if self.choice == -1:
            if choice == 0:
                self.choice = 0
                self.option_but1['bg'] = '#9090FF'
            elif choice == 1:
                self.choice = 1
                self.option_but2['bg'] = '#9090FF'
            else:
                self.choice = 2
                self.option_but3['bg'] = '#9090FF'
            self.open_empty_boxes()
            self.mess_lab['text'] = 'Change your choice?'
        else:
            if choice == 0:
                self.choice = 0
                self.get_result()
            elif choice == 1:
                self.choice = 1
                self.get_result()
            else:
                self.choice = 2
                self.get_result()
            self.option_but1['state'] = DISABLED
            self.option_but2['state'] = DISABLED
            self.option_but3['state'] = DISABLED

    def open_empty_boxes(self):
        side = random.choice([True, False])
        if side:
            for i in range(3):
                if self.boxes[i] == 0 and i != self.choice:
                    self.empty_box = i
                    self.buttons[i]['bg'] = '#FF9090'
                    break
        else:
            for i in range(2, -1, -1):
                if self.boxes[i] == 0 and i != self.choice:
                    self.empty_box = i
                    self.buttons[i]['bg'] = '#FF9090'
                    break

    def get_result(self):
        for i in range(3):
            if self.boxes[i] == 1:
                self.buttons[i]['bg'] = '#90FF90'
            else:
                self.buttons[i]['bg'] = '#FF9090'
        if self.boxes[self.choice] == 1:
            self.wins += 1
            self.mess_lab['text'] = 'You win!'
            self.score_lab['text'] = 'Score: {0}-{1}'.format(str(self.wins).zfill(2),
                                                             str(self.fails).zfill(2))
        else:
            self.fails += 1
            self.mess_lab['text'] = 'You lose...'
            self.score_lab['text'] = 'Score: {0}-{1}'.format(str(self.wins).zfill(2),
                                                             str(self.fails).zfill(2))
        self.next_but['state'] = NORMAL


play1 = Monty_Hall_Game(5)
play1.root.mainloop()

