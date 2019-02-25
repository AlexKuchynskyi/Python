# -*- coding: utf- 8 -*-

"""
This file has to be in the same folder with the portraits' folders.
In the general folder it's supposed to be 6 portrait-folders (8 portraits each, 1 folder for each layout from 6), 
two separate 'min.gif' and 'max.gif' for selection and this file. 
"""

import Tkinter as tk
from Tkinter import*
import os, random, time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


LARGE_FONT = ("Verdana", 12)

class Select_App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        global window_width, window_height
        window_width= self.winfo_screenwidth() - 20                 # set_ the window's height, width and x,y position
        window_height = self.winfo_screenheight() - 80              # x and y are the coordinates of the upper left corner
        x = 1
        y = 1
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
        global counter_selection_minus, counter_selection_plus      # counts selected "plus" "minus" images on each sheet
        counter_selection_plus = 0
        counter_selection_minus = 0
        global window_number
        self.sheet('%d' %window_number)
        self.title('%s' %str(window_number))
        self.move_select()

    def sheet(self, foldername):
        global images
        images = os.listdir(foldername)
        random.shuffle(images)
        global set_                                         # set of 8 images
        set_ = []
        counter_position = 0
        pos_x_up = 0
        pos_x_down = 0
        panel_width = window_width / 4                      # 8 panels on window (4x2)
        panel_height = window_height / 2                    #
        # draw 8 images (it's supposed to be 8 imgs in 'foldername') and put them into the set[]
        for name in images:
            photo = PhotoImage(file='%s/%s' %(foldername, name))
            panel = Label(self, image=photo, bg='black', bd=1)
            panel.photo = photo
            panel.pack()
            set_.append(panel)
            if counter_position < 4:
                panel.place(x=pos_x_up, y=0)
                pos_x_up = pos_x_up + panel_width
            else:
                panel.place(x=pos_x_down, y=panel_height - 15)
                pos_x_down = pos_x_down + panel_width
            counter_position += 1

        start = 0                                                                 # highlight 1st img (set[0])
        global index_                                                             # and set focus on it
        index_ = start
        set_[index_].config(bg='red', bd=5)
        set_[index_].focus_force()

    def rightKey(self, event):
        global index_
        if index_ != 7:
            set_[index_ + 1].config(bg='red', bd=5)         # highlight next (right) img
            set_[index_].config(bg='black', bd=1)           # and unhighlight current img
            index_ = index_ + 1

    def leftKey(self, event):
        global index_
        if index_ != 0:
            set_[index_ - 1].config(bg='red', bd=5)
            set_[index_].config(bg='black', bd=1)
            index_ = index_ - 1

    def upKey(self, event):
        global index_
        if index_ >= 4:
            set_[index_ - 4].config(bg='red', bd=5)
            set_[index_].config(bg='black', bd=1)
            index_ = index_ - 4

    def downKey(self, event):
        global index_
        if index_ < 4:
            set_[index_ + 4].config(bg='red', bd=5)
            set_[index_].config(bg='black', bd=1)
            index_ = index_ + 4

    def plusKey(self, event):
        global counter_selection_plus
        if counter_selection_plus < 2:
            self.change_to('plus')
            counter_selection_plus += 1

    def minusKey(self, event):
        global counter_selection_minus
        if counter_selection_minus < 2:
            self.change_to('minus')
            counter_selection_minus += 1

    def change_to(self, sign):
        set_[index_].config(bg='black', bd=1)
        current_x = set_[index_].winfo_x()              # get position of set_[index_] in order to put "plus"
        current_y = set_[index_].winfo_y()              # or "minus" in proper place
        if sign == 'minus':
            img_name = os.path.splitext(images[index_])[0]  #The splitext method separates the name from
            selected_minus.append(img_name)                 #the extension creating a tuple:
            photo = PhotoImage(file='min.gif')              # os.path.splitext("name.extention"), the created tuple
                                                            # now contains the strings "name" and "extention".
        if sign == 'plus':
            img_name = os.path.splitext(images[index_])[0]
            selected_plus.append(img_name)
            photo = PhotoImage(file='max.gif')
        panel = Label(self, image=photo, bg='red', bd=5)
        panel.photo = photo
        panel.pack()
        set_[index_] = panel
        panel.place(x=current_x, y=current_y)

    def move_select(self):
        set_[index_].bind("<Right>", self.rightKey)
        set_[index_].bind("<Left>", self.leftKey)
        set_[index_].bind("<Up>", self.upKey)
        set_[index_].bind("<Down>", self.downKey)
        set_[index_].bind("<+>", self.plusKey)
        set_[index_].bind("<minus>", self.minusKey)
        self.update_window()

    def update_window(self):
        self.protocol('WM_DELETE_WINDOW', lambda: sys.exit())
        if counter_selection_minus + counter_selection_plus == 4:
           self.destroy()
        self.after(1000, self.update_window)


class PageThree(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home") #,
                             #command=lambda: controller.show_frame(StartPage))
        button1.pack()
        f = Figure(figsize=(10, 5), dpi=100)
        a = f.add_subplot(111)
        """
        #a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        #a.bar(ind, vals, width)
        y = range (8)
        #N = len(y)
        x = ['h', 'hy', 'd', 'e', 'k', 'm', 'p', 's',]
        width = 1 / 1.5
        a.bar(x, y, width, color="blue")
        """
        for i in selected_plus:
            D['%s' %i] += 1
        for i in selected_minus:
            D['%s' % i] -= 1
        width = 1 / 1.5
        a.bar(D.keys(), D.values(), width, align='center')


        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
if __name__== "__main__":
    selected_plus = []                                               # arrays totally selected imgs (names of imgs)
    selected_minus = []
    D = {'h': 0, 'hy': 0, 'd': 0, 'e': 0, 'k': 0, 'm': 0, 'p': 0, 's': 0}

    for window_number in range (1, 7):
        app = Select_App()
        app.mainloop()
        print('Plus: %s' % selected_plus)
        print('Minus: %s' %selected_minus)

    graf = PageThree()
    print('Final: %s' % D)
    graf.mainloop()
