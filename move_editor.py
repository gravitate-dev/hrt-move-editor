from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

from me.controller.ModController import ModController


class App():

    def save(self):
        self.mod_controller.save();
        messagebox.showinfo("Success", "Only checked moves are kept")

    def restore(self):
        self.mod_controller.restore_everything()
        self.mod_controller.save()
        self.refresh()
        messagebox.showinfo("Success", "All moves are enabled")

    def disable_all(self):
        self.mod_controller.disable_everything()
        self.mod_controller.save()
        self.refresh()
        messagebox.showinfo("Success", "Disabled all moves")

    def refresh(self):
        self.mod_controller.load(MOD_FOLDER_CONST)
        for mod_list in self.mod_controller.get_mod_lists():
            tokens = mod_list.full_mod_path.split(os.sep);
            one_dir_up = tokens[-2] + os.sep + tokens[-1]
            temp = mod_list.get_move_delta()
            for move_delta in temp.keys():
                self.tk_mod_data[one_dir_up][move_delta].set(temp[move_delta])

    def cb_on_checked(self,mod_label,mod_move):
        mod_value = self.tk_mod_data[mod_label][mod_move].get()
        if mod_value==1:
            self.mod_controller.add_move(mod_label,mod_move)
        else:
            self.mod_controller.remove_move(mod_label,mod_move)

    def __init__(self, *args, **kwargs):
        self.mod_controller = ModController()
        root = Tk();
        root.attributes("-topmost", True)
        root.configure(background='white')
        root.geometry('640x480')
        canvas = Canvas(root, bg='white')
        root.wm_title("Move Editor")

        style = ttk.Style()
        style.configure("White.TCheckbutton", background="white")
        style.configure("White.TButton", background="white")

        top_frame= Frame(root, bg='white')
        top_frame.pack(side=TOP)
        btn1 = ttk.Button(top_frame, text='Restore All', command=self.restore)
        btn2 = ttk.Button(top_frame, text='Save', command=self.save)
        btn3 = ttk.Button(top_frame, text='Refresh', command=self.refresh)
        btn4 = ttk.Button(top_frame, text='Disable All', command=self.disable_all)

        btn1.configure(style="White.TButton")
        btn2.configure(style="White.TButton")
        btn3.configure(style="White.TButton")
        btn4.configure(style="White.TButton")

        btn1.pack(side=LEFT)
        btn2.pack(side=RIGHT)
        btn4.pack(side=LEFT)
        btn3.pack(side=RIGHT)


        frame_left = Frame(canvas, bg='white')

        vertscroll = Scrollbar(canvas, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vertscroll.set)

        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def app_width_resize(event, canvas_frame):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width=canvas_width)

        def mouse_scroll(event, canvas):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

                canvas.yview_scroll(move, 'units')

        root.bind('<Configure>', lambda event, canvas=canvas: onFrameConfigure(canvas))
        root.bind_all('<MouseWheel>', lambda event, canvas=canvas: mouse_scroll(event, canvas))
        root.bind_all('<Button-4>', lambda event, canvas=canvas: mouse_scroll(event, canvas))
        root.bind_all('<Button-5>', lambda event, canvas=canvas: mouse_scroll(event, canvas))

        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        canvas_frame = canvas.create_window((4, 4), window=frame_left, anchor="nw")
        vertscroll.pack(side=RIGHT, fill=Y)
        canvas.bind('<Configure>', lambda event, canvas_frame=canvas_frame: app_width_resize(event, canvas_frame))

        self.mod_controller.load(MOD_FOLDER_CONST)
        self.tk_mod_data = {}
        for mod_list in self.mod_controller.get_mod_lists():
            tokens = mod_list.full_mod_path.split(os.sep);
            one_dir_up = tokens[-2] + os.sep + tokens[-1]
            temp = mod_list.get_move_delta()
            for move_delta in temp.keys():
                temp[move_delta] = IntVar(master=root, value=temp[move_delta])
            self.tk_mod_data[one_dir_up] = temp

        max_col = 3

        for mod_label in self.tk_mod_data:
            if len(self.tk_mod_data[mod_label])==0:
                continue
            lbl = Label(frame_left, text=mod_label);
            lbl.grid(sticky=W)
            row = lbl.grid_info()['row'] + 1
            col = 0

            def cb_btn(mLabel, mMove):
                def func(): return self.cb_on_checked(mLabel, mMove)
                return func
            for mod_move in self.tk_mod_data[mod_label]:


                fn = cb_btn(mod_label,mod_move);
                cb = ttk.Checkbutton(frame_left, text=mod_move, variable=self.tk_mod_data[mod_label][mod_move], onvalue=1,
                                     offvalue=0,command=fn)
                cb.configure(style="White.TCheckbutton")
                cb.grid(column=col, row=row, sticky=W, padx=4)
                if (col == max_col-1):
                    row = row + 1
                col = (col + 1) % (max_col)
            row = row + 1

        root.mainloop()

def getModFolderPath():
    """ Gets the players full mod path folder"""
    guess_data_dir = os.getcwd()+os.sep+"data"
    if os.path.exists(guess_data_dir):
        return guess_data_dir
    root = Tk()
    root.withdraw()
    ans = filedialog.askdirectory(title='PLEASE select your mod root directory (the /data folder) in your game')
    root.update()
    root.destroy()
    return ans

MOD_FOLDER_CONST = ""
if __name__ == "__main__":
    MOD_FOLDER_CONST = getModFolderPath()
    app = App()
