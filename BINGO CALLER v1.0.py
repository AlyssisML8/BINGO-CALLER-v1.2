import random
import pyttsx3 as tts
import os
from tkinter import *
from tkinter import ttk

engine = tts.init()
root = Tk()
root.title('BINGO CALLER v1.0')

def exitfromwindow():
    root.after_cancel(mydid)
    numbersInWindow.pack_forget()
    exitbtn.pack_forget()
    showWinCheck()

def mainInterface():
    global numbersInWindow
    global exitbtn
    numbersInWindow = Label(root, text='No numbers.', font='Arial, 25', anchor=CENTER, foreground='#4287f5', width=15)
    numbersInWindow.pack()
    exitbtn = ttk.Button(root, text='Exit', command=exitfromwindow)
    exitbtn.pack()

mainInterface()

nums = []
flag = True

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 110)
engine.setProperty('volume', 1.0)

def main():
    global flag
    global nums
    global numbersInWindow
    if len(nums) < 60 and flag:
        num = random.randrange(1,61)
        if num not in nums:
            if len(nums) == 60:
                flag = False
            nums.append(num)
            lastfive = nums[-5:]
            os.system('cls')
            labelText = ''
            counter = 0
            for number in lastfive:
                counter += 1
                if counter == len(lastfive):
                    labelText += str(number)
                else:
                    labelText += str(number)+'\n'
            numbersInWindow.configure(text=labelText)
            num = str(num)
            engine.say(num)
            engine.runAndWait()
    global mydid
    mydid = root.after(3000, main)

mydid = root.after(1000, main)

def continue_game():
    checkfornums.pack_forget()
    checkbtn.pack_forget()
    continuegame.pack_forget()
    root.after(1000, main)
    mainInterface()
    pass

def showWinCheck():
    global checkfornums
    checkfornums = Entry(root, width=50)
    checkfornums.pack(pady=10, padx=5)

    def check():
        text = checkfornums.get()
        if text.isdigit():
            if int(text) == 61:
                return
            elif int(text) in nums:
                engine.say('Yes')
                engine.runAndWait()
            else:
                engine.say('No')
                engine.runAndWait()
    global checkbtn
    checkbtn = ttk.Button(root, text='Verify', command=check)
    checkbtn.pack()
    global continuegame
    continuegame = ttk.Button(root, text='Continue the game', command=continue_game)
    continuegame.pack(pady=10, padx=5)
    return

root.mainloop()