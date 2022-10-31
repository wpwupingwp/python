import time
import tkinter as tk
from tkinter import messagebox


def submit():
    h = hour.get()
    m = minute.get()
    s = second.get()
    try:
        temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
    except:
        print("Please input the right value")
    while temp >-1:
        mins,secs = divmod(temp,60)
        hours=0
        if mins >60:
            hours, mins = divmod(mins, 60)
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        root.update()
        time.sleep(1)
        if (temp == 0):
            messagebox.showinfo("Time Countdown", "Time's up ")
            hour.set("{0:2d}".format(int(h)))
            minute.set("{0:2d}".format(int(m)))
            second.set("{0:2d}".format(int(s)))
        temp -= 1
    return


root = tk.Tk()
root.geometry("300x150")
hour=tk.StringVar()
minute=tk.StringVar()
second=tk.StringVar()
hour.set("00")
minute.set("00")
second.set("00")
hourEntry=tk.Entry(root, width=3, font=("Arial",18,""), 
                   textvariable=hour)
hourEntry.place(x=80, y=20)
minuteEntry= tk.Entry(root, width=3, font=("Arial",18,""), 
                      textvariable=minute)
minuteEntry.place(x=130, y=20)
secondEntry= tk.Entry(root, width=3, font=("Arial",18,""), 
                      textvariable=second)
secondEntry.place(x=180, y=20)
btn = tk.Button(root, text='Set Time Countdown', bd='5',
            command= submit)
btn.place(x=70, y=80)
root.mainloop()

