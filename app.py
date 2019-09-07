from tkinter import *
import os
from controller.ModController import ModController

class App():


    def save(self):
        self.mod_controller.save();

    def restore(self):
        self.mod_controller.restore_all_moves()

    def __init__(self, *args, **kwargs):
        self.mod_controller = ModController()
        root = Tk();
        root.geometry('640x480')
        canvas = Canvas(root, bg='white')
        Button(root, text='Restore', command=root.quit).pack()
        Button(root, text='Save', command=root.quit).pack()

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

        self.mod_controller.load("D:\hentai\Enlit3D - Heroinev0.621\data")
        tk_mod_data = {}
        for mod_list in self.mod_controller.get_mod_lists():
            tokens = mod_list.full_mod_path.split(os.sep);
            one_dir_up = tokens[-2] + os.sep + tokens[-1]
            temp = mod_list.get_move_delta()
            for move_delta in temp.keys():
                temp[move_delta] = IntVar(master=root, value=temp[move_delta])
            tk_mod_data[one_dir_up] = temp

        for mod_label in tk_mod_data:
            Label(frame_left, text=mod_label).grid(sticky=W)
            for mod_move in tk_mod_data[mod_label]:
                Checkbutton(frame_left, text=mod_move, variable=tk_mod_data[mod_label][mod_move]).grid(sticky=W, padx=4)

        root.mainloop()

if __name__ == "__main__":
    app = App()