import math
import tkinter as tk
from abc import ABC, abstractmethod

root = tk.Tk()
root.title("~quiz~")
root.geometry("500x300")

class Data:
    chapter_numbers = []
    player_database  = {}
    keys = []
    vals = []
    leaderboard_info = {}

    def __init__(self, PATH):
        with open(PATH) as PD:
            for line in PD.readlines():
                nick, chapter, code = line.split()
                self.chapter_numbers.append(int(chapter))
                progress = []
                for i in range(30):
                    progress.append([int(code[3 * i + j]) for j in range(3)])
                self.player_database[nick] = progress

        self.keys = list(self.player_database.keys())
        self.vals = [sum(map(sum,self.player_database[user])) for user in self.player_database]
        self.leaderboard_info = {self.keys[i] : self.vals[i] for i in range(len(self.player_database))}

    def leaderboard(self, event, user, chapter_number, data):
        user.update_userlog(chapter_number, data)
        lb = tk.Toplevel()
        lb.geometry("300x500")
        lb.wm_title("Leaderboard")
        ind = 0
        for name in dict(sorted(self.leaderboard_info.items(), key=lambda item: item[1])[::-1]):
            lab1 = tk.Label(lb, text=name, font='Courier 14')
            lab2 = tk.Label(lb, text=self.leaderboard_info[name], font='Courier 14')
            lab1.grid(row=ind, column=0)
            lab2.grid(row=ind, column=1)
            ind += 1

        btn = tk.Button(lb, text="Okay", command=lb.destroy)
        btn.grid(row=ind, column=0)

class User:
    user_id = 0
    nickname = ''

    def login(self, event, ent, user, chapter, data):
        self.nickname = ent.get()
        self.user_id = chapter.initialize_chapter(self.nickname, data)
        welcome(None, user, chapter, data)
    
    def update_userlog(self, chapter_number, data):
        with open('data/users.txt', 'r') as file:
            file_copy = file.readlines()
            file.close()
        
        if self.user_id >= len(file_copy):
            file_copy.append([])
        
        file_copy[self.user_id] = self.nickname + ' ' + str(chapter_number) + ' '
        for chapter in data.player_database[self.nickname]:
            for task in chapter:
                file_copy[self.user_id] += str(task)
        file_copy[self.user_id] += '\n'

        with open('data/users.txt', 'w') as file:
            file.writelines(file_copy)
            file.close()

    def finish(self, event, user, chapter_number, data):
        user.update_userlog(chapter_number, data)
        exit()

class Chapter:
    def __init__(self):
        self.chapter_number = 0
        self.set_chapter_number = tk.StringVar()
        self.chapter_progress = [0, 0, 0]

    def initialize_chapter(self, nickname, data):
        ind = 0
        for (ind, key) in enumerate(data.player_database):
            if key == nickname:
                self.chapter_progress = data.player_database[nickname][self.chapter_number - 1]
                self.chapter_number = data.chapter_numbers[ind]
                break
        else:
            data.player_database[nickname] = [[0 for i in range(3)] for j in range(30)]
            self.chapter_progress = [0, 0, 0]
            self.chapter_number = 1
        return ind

    def update_chapter(self, nickname, data):
        self.set_chapter_number.set(str(self.chapter_number))
        self.chapter_progress = data.player_database[nickname][self.chapter_number - 1]

    def initialize_files(self, mode):
        mode.counter = 0

        ru_path = 'data/chapter' + str(self.chapter_number) + '/ru.txt'
        en_path = 'data/chapter' + str(self.chapter_number) + '/en.txt'
        an_path = 'data/chapter' + str(self.chapter_number) + '/an.txt'
        rus = [row.strip() for row in open(ru_path)]
        eng = [row.strip() for row in open(en_path)]
        ann = [row.strip() for row in open(an_path)]

        mode.words_number = len(rus)
        return [rus, eng, ann]

    def next_chapter(self, event, user, chapter, data):
        if self.chapter_number < 30:
            data.player_database[user.nickname][self.chapter_number - 1] = self.chapter_progress
            self.chapter_number += 1
            welcome(None, user, chapter, data)
        
    def prev_chapter(self, event, user, chapter, data):
        if self.chapter_number > 1:
            data.player_database[user.nickname][self.chapter_number - 1] = self.chapter_progress
            self.chapter_number -= 1
            welcome(None, user, chapter, data)

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

def authorize(user, chapter, data):
    lab = tk.Label(root, text='Enter your nickname: ', font='Courier 14')
    ent = tk.Entry(root, font='Courier 14', width=14)
    btn = tk.Button(root, width=8, height=1, text='Log in', font='Courier 14')
    lab.grid(row=0, column=0, columnspan=1)
    ent.grid(row=0, column=1, columnspan=1)
    btn.grid(row=1, column=0, columnspan=1)
    btn.bind('<Button-1>', lambda event: user.login(event, ent, user, chapter, data))
    root.bind('<Return>', lambda event: user.login(event, ent, user, chapter, data))
    ent.focus()

def welcome(event, user, chapter, data):
    clear(root)
    chapter.update_chapter(user.nickname, data)
    lab1 = tk.Label(root, text='Welcome! This is a word practice game.', font='Courier 14')
    btn1 = tk.Button(root, width=8, height=1, text='Learn', font='Courier 14', background=('light green' if chapter.chapter_progress[0] else 'light blue'))
    btn2 = tk.Button(root, width=8, height=1, text='Insert', font='Courier 14', background=('light green' if chapter.chapter_progress[1] else 'light blue'))
    btn3 = tk.Button(root, width=8, height=1, text='Test', font='Courier 14', background=('light green' if chapter.chapter_progress[2] else 'light blue'))
    lab2 = tk.Label(root, text='Current chapter: ', font='Courier 14')
    if chapter.chapter_number > 1:
        btn4 = tk.Button(root, width=4, height=1, text='<<', font='Courier 14')
        btn4.grid(row=3, column=0, columnspan=1)
        btn4.bind('<Button-1>', lambda event: chapter.prev_chapter(event, user, chapter, data))
        root.bind('<Left>', lambda event: chapter.prev_chapter(event, user, chapter, data))
    lab3 = tk.Label(root, textvariable=chapter.set_chapter_number, font='Courier 14')
    if chapter.chapter_number < 30:
        btn5 = tk.Button(root, width=4, height=1, text='>>', font='Courier 14')
        btn5.grid(row=3, column=2, columnspan=1)
        btn5.bind('<Button-1>', lambda event: chapter.next_chapter(event, user, chapter, data))
        root.bind('<Right>', lambda event: chapter.next_chapter(event, user, chapter, data))
    btn6 = tk.Button(root, width=8, height=1, text='Exit', font='Courier 14')
    btn7 = tk.Button(root, height=1, text='See the leaderboard', font='Courier 14')

    lab1.grid(row=0, column=0, columnspan=4)
    btn1.grid(row=1, column=0, columnspan=1)
    btn2.grid(row=1, column=1, columnspan=1)
    btn3.grid(row=1, column=2, columnspan=1)
    lab2.grid(row=2, column=0, columnspan=2)
    lab3.grid(row=3, column=1, columnspan=1)
    btn6.grid(row=4, column=0, columnspan=1)
    btn7.grid(row=4, column=1, columnspan=2)
    
    btn1.bind('<Button-1>', lambda event: LearnMode(event, user, chapter, data))
    btn2.bind('<Button-1>', lambda event: InsertMode(event, user, chapter, data))
    btn3.bind('<Button-1>', lambda event: TestMode(event, user, chapter, data))
    btn6.bind('<Button-1>', lambda event: user.finish(event, user, chapter.chapter_number, data))
    root.bind('<Escape>', lambda event: user.finish(event, user, chapter.chapter_number, data))
    btn7.bind('<Button-1>', lambda event: data.leaderboard(event, user, chapter.chapter_number, data))

class AbstractMode(ABC):
    counter = 0
    words_number = 0
    hints_taken = 0
    failed_attempts = 0
    counter = 0
    score = 0
    temp_score = 0
    trans = ''
    @abstractmethod
    def __init__(self, event, user, chapter, data):
        self.content = chapter.initialize_files(self)
        self.initialize_word()
        self.main()
        self.user = user
        self.chapter = chapter
        self.data = data

    @abstractmethod
    def initialize_word(self):
        raise NotImplementedError()

    @abstractmethod
    def main(self):
        raise NotImplementedError()

    @abstractmethod
    def next(self, event):
        raise NotImplementedError()

    @abstractmethod
    def finalize(self):
        raise NotImplementedError()

class LearnMode(AbstractMode):
    set_word = tk.StringVar()
    set_trans = tk.StringVar()
    set_context = tk.StringVar()
    lab1 = tk.Label(root, textvariable=set_trans, font='Courier 14')
    lab2 = tk.Label(root, textvariable=set_word, font='Courier 14')
    lab3 = tk.Label(root, textvariable=set_context, font='Courier 14')
    btn1 = tk.Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn2 = tk.Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def __init__(self, event, user, chapter, data):
        super().__init__(event, user, chapter, data)

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
        self.btn1.bind('<Button-1>', lambda event: self.next(event))
        self.btn2.grid(row=3, column=0, sticky="W")
        self.btn2.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: self.next(event))
        root.bind('<Escape>', lambda event: welcome(event, self.user, self.chapter, self.data))

    def next(self, event):
        self.counter += 1
        if self.counter == self.words_number:
            self.finalize()
        else:
            self.initialize_word()
            self.main()

    def finalize(self):
        self.chapter.chapter_progress[0] = 1
        clear(root)
        lab1 = tk.Label(root, text='Congrats, you have learnt ', font='Courier 14')
        lab2 = tk.Label(root, text=str(self.words_number) + ' words!', font='Courier 14')
        lab1.grid(row=0, column=0, columnspan=2)
        lab2.grid(row=1, column=0, columnspan=1)
        btn = tk.Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=2, column=1, columnspan=1)
        btn.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: welcome(event, self.user, self.chapter, self.data))

class InsertMode(AbstractMode):
    set_word = tk.StringVar()
    set_trans = tk.StringVar()
    set_context = tk.StringVar()
    lab1 = tk.Label(root, textvariable=set_word, font='Courier 14')
    lab2 = tk.Label(root, textvariable=set_context, font='Courier 10')
    ent = tk.Entry(root, font='Courier 14', width=14)
    btn1 = tk.Button(root, width=4, height=1, text='Hint', font='Courier 14')
    btn2 = tk.Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn3 = tk.Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def __init__(self, event, user, chapter, data):
        super().__init__(event, user, chapter, data)

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
        self.ent.configure(state=tk.NORMAL)
        self.btn1.configure(state=tk.NORMAL)
        self.ent.delete(0, tk.END)
        clear(root)
        self.lab1.grid(row=0, column=0, sticky="W")
        self.ent.grid(row=0,column=1, sticky="W")
        self.lab2.grid(row=1, column=0, columnspan=2, sticky="W")
        self.btn1.grid(row=2, column=0, sticky="W")
        self.btn2.grid(row=2, column=1, sticky="W")
        self.btn3.grid(row=3, column=0, sticky="W")
        self.btn1.bind('<Button-1>', lambda event: self.hint(event))
        self.btn2.bind('<Button-1>', lambda event: self.next(event))
        self.btn3.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: self.next(event))
        root.bind('<Escape>', lambda event: welcome(event, self.user, self.chapter, self.data))
        self.ent.focus()

    def hint(self, event):
        if self.hints_taken < 3:
            self.hints_taken += 1
            self.temp_score -= 0.1
            self.ent.delete(0, tk.END)
            self.ent.insert(0, self.trans[:(self.hints_taken)])
            self.ent.configure()

    def next(self, event):
        if self.ent.get() == self.trans:
            if self.failed_attempts < 3:
                self.score += self.temp_score
            self.counter += 1
            if self.counter < self.words_number:
                self.initialize_word()
                self.main()
            else:
                self.finalize()
        else:
            if self.failed_attempts < 3:
                self.failed_attempts += 1
                self.temp_score -= 0.2
                self.ent.selection_range(0, tk.END)
            else:
                self.ent.delete(0, tk.END)
                self.ent.insert(0, self.trans)
                self.ent.configure(state=tk.DISABLED)
                self.btn1.configure(state=tk.DISABLED)
            
    def finalize(self):
        if self.score >= 0.8 * self.words_number:
            self.chapter.chapter_progress[1] = 1
        clear(root)
        lab = tk.Label(root, text='Your score from '+str(self.words_number)+': ' + str(round(self.score, 1)), font='Courier 14')
        lab.grid(row=0, column=0)
        btn = tk.Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=1, column=0, columnspan=1, sticky="W")
        btn.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: welcome(event, self.user, self.chapter, self.data))
        self.score = 0

class TestMode(AbstractMode):
    set_word = tk.StringVar()
    set_trans = tk.StringVar()
    set_context = tk.StringVar()
    lab = tk.Label(root,textvariable=set_word, font='Courier 14')
    ent = tk.Entry(root,font='Courier 14', width=14)
    btn1 = tk.Button(root, width=4, height=1, text='Hint', font='Courier 14')
    btn2 = tk.Button(root, width=4, height=1, text='>>', font='Courier 14')
    btn3 = tk.Button(root, width=4, height=1, text='Exit', font='Courier 14')

    def __init__(self, event, user, chapter, data):
        super().__init__(event, user, chapter, data)

    def initialize_word(self):
        word = self.content[0][self.counter]
        self.trans = self.content[1][self.counter]
        
        self.set_word.set(str(word))
        self.set_trans.set(str(self.trans))

        self.hints_taken = 0
        self.failed_attempts = 0
        self.temp_score = 1

    def main(self):
        self.ent.configure(state=tk.NORMAL)
        self.btn1.configure(state=tk.NORMAL)
        self.ent.delete(0, tk.END)
        clear(root)
        self.lab.grid(row=0, column=0, sticky="W")
        self.ent.grid(row=0, column=1, sticky="W")
        self.btn1.grid(row=1, column=0, sticky="W")
        self.btn2.grid(row=1, column=1, sticky="W")
        self.btn3.grid(row=2, column=0, sticky="W")
        self.btn1.bind('<Button-1>', lambda event: self.hint(event))
        self.btn2.bind('<Button-1>', lambda event: self.next(event))
        self.btn3.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: self.next(event))
        root.bind('<Escape>', lambda event: welcome(event, self.user, self.chapter, self.data))
        self.ent.focus()

    def hint(self, event):
        global hints_taken, trans, score
        if self.hints_taken < 3:
            self.hints_taken += 1
            self.temp_score -= 0.1
            self.ent.delete(0, tk.END)
            self.ent.insert(0, self.trans[:(self.hints_taken)])
            self.ent.configure()

    def next(self, event):
        if self.ent.get() == self.trans:
            if self.failed_attempts < 3:
                self.score += self.temp_score
            self.counter += 1
            if self.counter < self.words_number:
                self.initialize_word()
                self.main()
            else:
                self.finalize()
        else:
            if self.failed_attempts < 3:
                self.failed_attempts += 1
                self.temp_score -= 0.2
                self.ent.selection_range(0, tk.END)
            else:
                self.ent.delete(0, tk.END)
                self.ent.insert(0, self.trans)
                self.ent.configure(state=tk.DISABLED)
                self.btn1.configure(state=tk.DISABLED)
                
    def finalize(self):
        if self.score >= 0.8 * self.words_number:
            self.chapter.chapter_progress[1] = 1
        clear(root)
        lab = tk.Label(root, text='Your score from '+str(self.words_number)+': ' + str(round(self.score, 1)), font='Courier 14')
        lab.grid(row=0, column=0)
        btn = tk.Button(root, width=15, height=1, text='Back to menu', font='Courier 14')
        btn.grid(row=1, column=0, columnspan=1, sticky="W")
        btn.bind('<Button-1>', lambda event: welcome(event, self.user, self.chapter, self.data))
        root.bind('<Return>', lambda event: welcome(event, self.user, self.chapter, self.data))
        self.score = 0

def main():
    user = User()
    chapter = Chapter()
    data = Data('data/users.txt')
    authorize(user, chapter, data)

if __name__ == "__main__":
    main()
