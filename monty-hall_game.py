import random
from tkinter import *


class MontyHallModel:
    def __init__(self):
        self.boxes = []
        self.boxes_amount = 3  # for default
        self.choice = None
        self.round = 1
        self.wins = 0
        self.fails = 0

    def start_game(self, boxes_amount=3):
        self.boxes_amount = boxes_amount
        self.round = 0
        self.wins = 0
        self.fails = 0

    def get_distribution(self):
        self.round += 1
        self.boxes = [0] * self.boxes_amount
        self.choice = None
        prize = random.randint(0, self.boxes_amount - 1)
        self.boxes[prize] = 1
        print(self.boxes)

    def made_choice(self, choice):
        self.choice = choice
        if self.boxes[self.choice] == 1:
            self.wins += 1
        else:
            self.fails += 1

    def get_tips(self):
        boxes_to_open = list(range(len(self.boxes)))
        del boxes_to_open[self.choice]
        del boxes_to_open[random.choice(boxes_to_open)]
        print(self.boxes, self.choice, boxes_to_open)
        return boxes_to_open


class MontyHallController:
    def __init__(self, model):
        self.model = model
        self.with_tips = True
        self.rounds_amount = None

    def set_view(self, view):
        self.view = view

    def start(self):
        self.with_tips, boxes_amount, self.rounds_amount = self.view.get_settings()
        self.model.start_game(boxes_amount)
        self.model.get_distribution()
        self.view.refresh_score()
        self.view.draw_buttons()

    def choose(self, chosen_box):
        self.model.made_choice(chosen_box)
        if self.with_tips:
            pass
        else:
            self.view.refresh_score()
            self.view.open_boxes(range(len(self.model.boxes)))
            self.view.after(5000, self.new_round)

    def new_round(self):
        self.model.get_distribution()
        self.view.refresh_score()
        self.view.draw_buttons()


class MontyHallInterface(Frame):
    def __init__(self, master=None, model=None, controller=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.master = master
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
        self.buttons = []
        self.mode_var = BooleanVar()
        self.mode_var.set(True)
        self.boxes_count_var = IntVar()
        self.boxes_count_var.set(3)
        self.rounds_count_var = IntVar()
        self.rounds_count_var.set(20)
        self.create_widgets()

    def create_widgets(self):
        # settings
        settings_frame_parent = Frame(self, bg='grey')
        settings_frame_child = Frame(settings_frame_parent, bg='grey')
        tips_lab = Label(settings_frame_child, text='Tips:',
                      bg='grey', font=('Consolas', '14'))
        mode_check = Checkbutton(settings_frame_child,
                                 variable=self.mode_var,
                                 font=('Consolas', '14'),
                                 bg='grey')
        rounds_count_lab = Label(settings_frame_child, text='Rounds:',
                             bg='grey', font=('Consolas', '14'))
        rounds_count_spinbox = Spinbox(settings_frame_child,
                                      from_=1, to=100,
                                      width=3,
                                      textvariable=self.rounds_count_var,
                                      font=('Consolas','18','bold'))
        boxes_count_lab = Label(settings_frame_child, text='Boxes:',
                             bg='grey', font=('Consolas', '14'))
        boxes_count_spinbox = Spinbox(settings_frame_child,
                                      from_=3, to=10,
                                      width=3,
                                      textvariable=self.boxes_count_var,
                                      font=('Consolas','18','bold'))
        start_but = Button(settings_frame_child, text='START',
                           command=self.controller.start,
                           font=('Consolas', '16', 'bold'))
        # guess boxes
        score_frame = Frame(self, bg='red')
        self.score_lab = Label(score_frame,
                               bg='white',
                               text='Round: 00 | Wins: 00 | Fails: 00',
                               font=('Consolas','18','bold'))
        # boxes
        frame_boxes_parent = Frame(self)
        self.frame_boxes_child = Frame(frame_boxes_parent)
        self.draw_buttons()
        # PACKED
        settings_frame_parent.pack(fill='x')
        settings_frame_child.pack(expand=True, padx=5, pady=5)
        tips_lab.pack(side='left')
        mode_check.pack(side='left')
        rounds_count_lab.pack(side='left')
        rounds_count_spinbox.pack(side='left', fill='y')
        boxes_count_lab.pack(side='left')
        boxes_count_spinbox.pack(side='left', fill='y')
        start_but.pack(side='left', fill='y', padx=5)
        score_frame.pack(fill='x')
        self.score_lab.pack(fill='x')
        frame_boxes_parent.pack(fill='both', expand=True)
        self.frame_boxes_child.pack(expand=True, padx=20, pady=20)

    def draw_buttons(self):
        while self.buttons:
            button = self.buttons.pop()
            button.destroy()
        for i in range(self.model.boxes_amount):
            self.buttons.append(
                Button(self.frame_boxes_child,
                       text=str(i+1),
                       command=lambda: self.controller.choose(i),
                       width=3,
                       bg='black',
                       fg='white',
                       bd=5,
                       font=('Consolas', '28', 'bold')))
            self.buttons[i].pack(side='left', padx=10)
        master_width = 450 if i < 4 else 450+(i-3)*100
        self.master.geometry('{}x{}'.format(master_width, 240))
        self.master.minsize(width=master_width, height=240)

    def get_settings(self):
        return self.mode_var.get(),\
               self.boxes_count_var.get(),\
               self.rounds_count_var.get()

    def open_boxes(self, boxes_to_open):
        for box_num in boxes_to_open:
            self.buttons[box_num].config(
                text='\u2605' if self.model.boxes[box_num] else '')

    def refresh_score(self):
        self.score_lab.config(text='Round: {:2} | Wins: {:2} | Fails: {:2}'.format(
            self.model.round,
            self.model.wins,
            self.model.fails))

root = Tk()
root.title('Monty Hall game')
root.minsize(width=450, height=240)

MH_model = MontyHallModel()
MH_controller = MontyHallController(MH_model)
MH_view = MontyHallInterface(root, MH_model, MH_controller)
MH_view.mainloop()





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


# play1 = Monty_Hall_Game(5)
# play1.root.mainloop()

