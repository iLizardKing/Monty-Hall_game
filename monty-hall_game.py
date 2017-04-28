import random
from tkinter import *


class MontyHallModel:
    def __init__(self):
        self.boxes = []
        self.boxes_amount = None
        self.round = None
        self.wins = None
        self.fails = None
        self.choice = None

    def start_game(self, boxes_amount=3):
        self.boxes_amount = boxes_amount
        self.round = 0
        self.wins = 0
        self.fails = 0

    def get_distribution(self):
        self.choice = None
        self.round += 1
        self.boxes = [0] * self.boxes_amount
        prize = random.randint(0, self.boxes_amount - 1)
        self.boxes[prize] = 1

    def made_choice(self, choice):
        self.choice = choice
        if self.boxes[self.choice] == 1:
            self.wins += 1
        else:
            self.fails += 1

    def get_tips(self, choice):
        boxes_to_open = list(range(len(self.boxes)))
        boxes_to_open.remove(choice)
        right_answ = self.boxes.index(1)
        if choice == right_answ:
            boxes_to_open.remove(random.choice(boxes_to_open))
        else:
            boxes_to_open.remove(right_answ)
        return boxes_to_open


class MontyHallController:
    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.with_tips = True
        self.rounds_amount = None
        self.is_final_guess = True
        self.after_id = None

    def set_view(self, view):
        self.view = view

    def start(self):
        if self.after_id:
            self.view.after_cancel(self.after_id)
        self.with_tips, boxes_amount, self.rounds_amount = self.view.get_settings()
        self.model.start_game(boxes_amount)
        self.new_round()

    def new_round(self):
        self.is_final_guess = True
        self.model.get_distribution()
        self.view.refresh_score()
        self.view.draw_buttons()

    def choose(self, chosen_box):
        if self.with_tips:
            self.is_final_guess = not self.is_final_guess
        if self.is_final_guess:
            self.model.made_choice(chosen_box)
            self.view.refresh_score()
            self.view.open_boxes(list(range(len(self.model.boxes))))
            if self.model.round < self.rounds_amount:
                self.after_id = self.view.after(5000, self.new_round)
            else:
                self.view.stop_game()
        else:
            boxes_to_open = self.model.get_tips(chosen_box)
            self.view.open_boxes(boxes_to_open)


class MontyHallInterface(Frame):
    def __init__(self, master=None, model=None, controller=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.master = master
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
        self.buttons = []
        # widgets
        self.score_lab = None
        self.frame_boxes_child = None
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
        try:
            self.result_lab.destroy()
        except AttributeError:
            pass
        while self.buttons:
            button = self.buttons.pop()
            button.destroy()
        for i in range(self.model.boxes_amount):
            self.buttons.append(
                Button(self.frame_boxes_child,
                       text=str(i+1),
                       command=lambda choice=i: self.controller.choose(choice),
                       width=3,
                       bg='black',
                       fg='white',
                       activebackground='#ffddaa',
                       activeforeground='black',
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
            color = '#bed6be' if self.model.boxes[box_num] else \
                    '#ffddaa' if box_num == self.model.choice else \
                    'systembuttonface'
            self.buttons[box_num].config(
                text='\uff04' if self.model.boxes[box_num] else '',
                state='disabled',
                disabledforeground='black',
                bg=color,
                relief='sunken')

    def refresh_score(self):
        self.score_lab.config(text='Round: {:2} | Wins: {:2} | Fails: {:2}'.format(
            self.model.round,
            self.model.wins,
            self.model.fails))

    def stop_game(self):
        while self.buttons:
            button = self.buttons.pop()
            button.destroy()
        self.result_lab = Label(self.frame_boxes_child,
                                text='{:2}% of wins!'.format(
                                    round(self.model.wins / self.model.round * 100)),
                                font=('Consolas', '40', 'bold'))
        self.result_lab.pack()


root = Tk()
root.title('Monty Hall game')
root.minsize(width=450, height=240)

MH_model = MontyHallModel()
MH_controller = MontyHallController(MH_model)
MH_view = MontyHallInterface(root, MH_model, MH_controller)

MH_view.mainloop()