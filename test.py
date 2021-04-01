from tkinter import *
import math

root = Tk()
root.title("~quiz~")
root.geometry("500x300")

chapter_numbers = []

player_database  = {}
PD = open('data/users.txt')
for line in PD.readlines():
    nickname, chapter, code = line.split()
    chapter = int(chapter)
    chapter_numbers.append(chapter)
    progress = []
    for i in range(30):
        progress.append([int(code[3 * i + j]) for j in range(3)])
    player_database[nickname] = progress

keys = list(player_database.keys())
vals = [sum(map(sum,player_database[user])) for user in player_database]
leaderboard_info = {keys[i] : vals[i] for i in range(len(player_database))}

user_id = 0
nickname = ''
chapter_number = 0
set_chapter_number = StringVar()
chapter_progress = [0, 0, 0]
user_lvl = 0

def initialize_chapter():
    global chapter_number, set_chapter_number, chapter_progress
    set_chapter_number.set(str(chapter_number))
    chapter_progress = chapter_progress = player_database[nickname][chapter_number - 1]

def initialize_files(mode):
    mode.counter = 0

    ru_path = 'data/chapter' + str(chapter_number) + '/ru.txt'
    en_path = 'data/chapter' + str(chapter_number) + '/en.txt'
    an_path = 'data/chapter' + str(chapter_number) + '/an.txt'
    rus = [row.strip() for row in open(ru_path)]
    eng = [row.strip() for row in open(en_path)]
    ann = [row.strip() for row in open(an_path)]

    mode.words_number = len(rus)
    return [rus, eng, ann]

def clear(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    for item in _list:
        item.grid_forget()
    window.unbind_all('<Left>')
    window.unbind_all('<Right>')
    window.unbind_all('<Escape>')
    window.unbind_all('<Return>')

def authorize():
    lab = Label(root, text='Enter your nickname: ', font='Courier 14')
    ent = Entry(root, font='Courier 14', width=14)
    btn = Button(root, width=8, height=1, text='Log in', font='Courier 14')
    lab.grid(row=0, column=0, columnspan=1)
    ent.grid(row=0, column=1, columnspan=1)
    btn.grid(row=1, column=0, columnspan=1)
    btn.bind('<Button-1>', lambda event: login(event, ent))
    root.bind('<Return>', lambda event: login(event, ent))
    ent.focus()

def login(event, ent):
    global chapter_progress, nickname, user_id, chapter_number
    nickname = ent.get()
    ind = 0
    for key in player_database:
        if key == nickname:
            chapter_progress = player_database[nickname][chapter_number - 1]
            chapter_number = chapter_numbers[ind]
            break
        ind += 1
    if ind == len(player_database):
        player_database[nickname] = [[0 for i in range(3)] for j in range(30)]
        chapter_progress = [0, 0, 0]
        chapter_number = 1
    user_id = ind

    welcome(None)

def welcome(event):
    global set_chapter_number
    clear(root)
    initialize_chapter()
    lab1 = Label(root, text='Welcome! This is a word practice game.', font='Courier 14')
    btn1 = Button(root, width=8, height=1, text='Learn', font='Courier 14', background=('light green' if chapter_progress[0] else 'light blue'))
    btn2 = Button(root, width=8, height=1, text='Insert', font='Courier 14', background=('light green' if chapter_progress[1] else 'light blue'))
    btn3 = Button(root, width=8, height=1, text='Test', font='Courier 14', background=('light green' if chapter_progress[2] else 'light blue'))
    lab2 = Label(root, text='Current chapter: ', font='Courier 14')
    if chapter_number > 1:
        btn4 = Button(root, width=4, height=1, text='<<', font='Courier 14')
        btn4.grid(row=3, column=0, columnspan=1)
        btn4.bind('<Button-1>', prev_chapter)
        root.bind('<Left>', prev_chapter)
    lab3 = Label(root, textvariable=set_chapter_number, font='Courier 14')
    if chapter_number < 30:
        btn5 = Button(root, width=4, height=1, text='>>', font='Courier 14')
        btn5.grid(row=3, column=2, columnspan=1)
        btn5.bind('<Button-1>', next_chapter)
        root.bind('<Right>', next_chapter)
    btn6 = Button(root, width=8, height=1, text='Exit', font='Courier 14')
    btn7 = Button(root, height=1, text='See the leaderboard', font='Courier 14')

    lab1.grid(row=0, column=0, columnspan=4)
    btn1.grid(row=1, column=0, columnspan=1)
    btn2.grid(row=1, column=1, columnspan=1)
    btn3.grid(row=1, column=2, columnspan=1)
    lab2.grid(row=2, column=0, columnspan=2)
    lab3.grid(row=3, column=1, columnspan=1)
    btn6.grid(row=4, column=0, columnspan=1)
    btn7.grid(row=4, column=1, columnspan=2)
    
    btn1.bind('<Button-1>', learn)
    btn2.bind('<Button-1>', insert)
    btn3.bind('<Button-1>', test)
    btn6.bind('<Button-1>', finish)
    root.bind('<Escape>', finish)
    btn7.bind('<Button-1>', leaderboard)

def leaderboard(event):
    update_file
    lb = Toplevel()
    lb.geometry("300x500")
    lb.wm_title("Leaderboard")
    ind = 0
    for user in dict(sorted(leaderboard_info.items(), key=lambda item: item[1])[::-1]):
        lab1 = Label(lb, text=user, font='Courier 14')
        lab2 = Label(lb, text=leaderboard_info[user], font='Courier 14')
        lab1.grid(row=ind, column=0)
        lab2.grid(row=ind, column=1)
        ind += 1

    btn = Button(lb, text="Okay", command=lb.destroy)
    btn.grid(row=ind, column=0)

def next_chapter(event):
    global chapter_number, root
    if chapter_number < 30:
        player_database[nickname][chapter_number - 1] = chapter_progress
        chapter_number += 1
        welcome(None)
    
def prev_chapter(event):
    global chapter_number, root
    if chapter_number > 1:
        player_database[nickname][chapter_number - 1] = chapter_progress
        chapter_number -= 1
        welcome(None)

def learn(event):
    learner = LearnMode
    LearnMode.__init__(learner)

def insert(event):
    inserter = InsertMode
    InsertMode.__init__(inserter)

def test(event):
    tester = TestMode
    TestMode.__init__(tester)

class LearnMode:
    global chapter_number, initialize_files, clear, root, welcome
    counter = 0
    words_number = 0
    content = []
    set_word = StringVar()
    set_trans = StringVar()
    set_context = StringVar()
    lab1 = Label(root, textvariable=set_trans, font='Courier 14')
    lab2 = Label(root, textvariable=set_word, font='Courier 14')
    lab3 = Label(root, textvariable=set_context, font='Courier 14')
    btn1 = Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn2 = Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def initialize_word(self):
        word = self.content[0][self.counter]
        trans = self.content[1][self.counter]
        context = self.content[2][self.counter].replace('___', trans)
        
        self.set_word.set(str(word))
        self.set_trans.set(str(trans))
        self.set_context.set(str(context))

    def main(self):
        clear(root)
        self.lab1.grid(row=0, column=0, sticky="W")
        self.lab2.grid(row=1, column=0, sticky="W")
        self.lab3.grid(row=2, column=0, sticky="W")
        self.btn1.grid(row=3, column=0, sticky="W")
        self.btn1.bind('<Button-1>', lambda event: self.next(self, event))
        self.btn2.grid(row=3, column=0, sticky="W")
        self.btn2.bind('<Button-1>', welcome)
        root.bind('<Return>', lambda event: self.next(self, event))
        root.bind('<Escape>', welcome)

    def next(self, event):
        self.counter += 1
        if self.counter == self.words_number:
            self.finalize(self)
        else:
            self.initialize_word(self)
            self.main(self)

    def finalize(self):
        chapter_progress[0] = 1
        clear(root)
        lab1 = Label(root, text='Congrats, you have learnt ', font='Courier 14')
        lab2 = Label(root, text=str(self.words_number) + ' words!', font='Courier 14')
        lab1.grid(row=0, column=0, columnspan=2)
        lab2.grid(row=1, column=0, columnspan=1)
        btn = Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=2, column=1, columnspan=1)
        btn.bind('<Button-1>', welcome)
        root.bind('<Return>', welcome)
    
    def __init__(self):
        self.content = initialize_files(self)
        self.initialize_word(self)
        self.main(self)

class InsertMode:
    global chapter_number, initialize_files, clear, root, welcome
    hints_taken = 0
    failed_attempts = 0
    counter = 0
    score = 0
    temp_score = 0
    trans = ''
    words_number = 0
    content = []
    set_word = StringVar()
    set_trans = StringVar()
    set_context = StringVar()
    lab1 = Label(root, textvariable=set_word, font='Courier 14')
    lab2 = Label(root, textvariable=set_context, font='Courier 10')
    ent = Entry(root, font='Courier 14', width=14)
    btn1 = Button(root, width=4, height=1, text='Hint', font='Courier 14')
    btn2 = Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn3 = Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def initialize_word(self):
        word = self.content[0][self.counter]
        self.trans = self.content[1][self.counter]
        context = self.content[2][self.counter]
        
        self.set_word.set(str(word))
        self.set_trans.set(str(self.trans))
        self.set_context.set(str(context))

        self.hints_taken = 0
        self.failed_attempts = 0
        self.temp_score = 1

    def main(self):
        self.ent.configure(state=NORMAL)
        self.btn1.configure(state=NORMAL)
        self.ent.delete(0, END)
        clear(root)
        self.lab1.grid(row=0, column=0, sticky="W")
        self.ent.grid(row=0,column=1, sticky="W")
        self.lab2.grid(row=1, column=0, columnspan=2, sticky="W")
        self.btn1.grid(row=2, column=0, sticky="W")
        self.btn2.grid(row=2, column=1, sticky="W")
        self.btn3.grid(row=3, column=0, sticky="W")
        self.btn1.bind('<Button-1>', lambda event: self.hint(self, event))
        self.btn2.bind('<Button-1>', lambda event: self.next(self, event))
        self.btn3.bind('<Button-1>', welcome)
        root.bind('<Return>', lambda event: self.next(self, event))
        root.bind('<Escape>', welcome)
        self.ent.focus()

    def hint(self, event):
        if self.hints_taken < 3:
            self.hints_taken += 1
            self.temp_score -= 0.1
            self.ent.delete(0, END)
            self.ent.insert(0, self.trans[:(self.hints_taken)])
            self.ent.configure()

    def next(self, event):
        if self.ent.get() == self.trans:
            if self.failed_attempts < 3:
                self.score += self.temp_score
            self.counter += 1
            if self.counter < self.words_number:
                self.initialize_word(self)
                self.main(self)
            else:
                self.finalize(self)
        else:
            if self.failed_attempts < 3:
                self.failed_attempts += 1
                self.temp_score -= 0.2
                self.ent.selection_range(0, END)
            else:
                self.ent.delete(0, END)
                self.ent.insert(0, self.trans)
                self.ent.configure(state=DISABLED)
                self.btn1.configure(state=DISABLED)
            
    def finalize(self):
        if self.score >= 0.8 * self.words_number:
            chapter_progress[1] = 1
        clear(root)
        lab = Label(root, text='Your score from '+str(self.words_number)+': ' + str(round(self.score, 1)), font='Courier 14')
        lab.grid(row=0, column=0)
        btn = Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=1, column=0, columnspan=1, sticky="W")
        btn.bind('<Button-1>', welcome)
        root.bind('<Return>', welcome)
        self.score = 0
    
    def __init__(self):
        self.content = initialize_files(self)
        self.initialize_word(self)
        self.main(self)

class TestMode:
    global chapter_number, initialize_files, clear, root, welcome
    hints_taken = 0
    failed_attempts = 0
    counter = 0
    score = 0
    temp_score = 0
    trans = ''
    words_number = 0
    content = []
    set_word = StringVar()
    set_trans = StringVar()
    lab = Label(root, textvariable=set_word, font='Courier 14')
    ent = Entry(root,font='Courier 14', width=14)
    btn1 = Button(root, width=4, height=1, text='Hint', font='Courier 14')
    btn2 = Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn3 = Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def initialize_word(self):
        word = self.content[0][self.counter]
        self.trans = self.content[1][self.counter]
        
        self.set_word.set(str(word))
        self.set_trans.set(str(self.trans))

        self.hints_taken = 0
        self.failed_attempts = 0
        self.temp_score = 1

    def main(self):
        self.ent.configure(state=NORMAL)
        self.btn1.configure(state=NORMAL)
        self.ent.delete(0, END)
        clear(root)
        self.lab.grid(row=0, column=0, sticky="W")
        self.ent.grid(row=0, column=1, sticky="W")
        self.btn1.grid(row=1, column=0, sticky="W")
        self.btn2.grid(row=1, column=1, sticky="W")
        self.btn3.grid(row=2, column=0, sticky="W")
        self.btn1.bind('<Button-1>', lambda event: self.hint(self, event))
        self.btn2.bind('<Button-1>', lambda event: self.next(self, event))
        self.btn3.bind('<Button-1>', welcome)
        root.bind('<Return>', lambda event: self.next(self, event))
        root.bind('<Escape>', welcome)
        self.ent.focus()

    def hint(self, event):
        global hints_taken, trans, score
        if self.hints_taken < 3:
            self.hints_taken += 1
            self.temp_score -= 0.1
            self.ent.delete(0, END)
            self.ent.insert(0, self.trans[:(self.hints_taken)])
            self.ent.configure()

    def next(self, event):
        if self.ent.get() == self.trans:
            if self.failed_attempts < 3:
                self.score += self.temp_score
            self.counter += 1
            if self.counter < self.words_number:
                self.initialize_word(self)
                self.main(self)
            else:
                self.finalize(self)
        else:
            if self.failed_attempts < 3:
                self.failed_attempts += 1
                self.temp_score -= 0.2
                self.ent.selection_range(0, END)
            else:
                self.ent.delete(0, END)
                self.ent.insert(0, self.trans)
                self.ent.configure(state=DISABLED)
                self.btn1.configure(state=DISABLED)
                
    def finalize(self):
        if self.score >= 0.8 * self.words_number:
            chapter_progress[1] = 1
        clear(root)
        lab = Label(root, text='Your score from '+str(self.words_number)+': ' + str(round(self.score, 1)), font='Courier 14')
        lab.grid(row=0, column=0)
        btn = Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=1, column=0, columnspan=1, sticky="W")
        btn.bind('<Button-1>', welcome)
        root.bind('<Return>', welcome)
        self.score = 0

    def __init__(self):
        self.content = initialize_files(self)
        self.initialize_word(self)
        self.main(self)

def update_file():
    with open('data/users.txt', 'r') as file:
        file_copy = file.readlines()
        file.close()
    
    if user_id >= len(file_copy):
        file_copy.append([])
    
    file_copy[user_id] = nickname + ' ' + str(chapter_number) + ' '
    for chapter in player_database[nickname]:
        for task in chapter:
            file_copy[user_id] += str(task)
    file_copy[user_id] += '\n'

    with open('data/users.txt', 'w') as file:
        file.writelines(file_copy)
        file.close()

def finish(event):
    update_file()
    exit()

authorize()
