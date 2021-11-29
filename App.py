import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Seminar Project")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_682=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_682["font"] = ft
        GLabel_682["fg"] = "#333333"
        GLabel_682["justify"] = "center"
        GLabel_682["text"] = "Display"
        GLabel_682.place(x=0,y=0,width=599,height=20)

        GListBox_280=tk.Listbox(root)
        GListBox_280["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_280["font"] = ft
        GListBox_280["fg"] = "#333333"
        GListBox_280["justify"] = "center"
        GListBox_280.place(x=0,y=260,width=181,height=234)

        GListBox_487=tk.Listbox(root)
        GListBox_487["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_487["font"] = ft
        GListBox_487["fg"] = "#333333"
        GListBox_487["justify"] = "center"
        GListBox_487.place(x=418,y=260,width=181,height=234)

        GLabel_16=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_16["font"] = ft
        GLabel_16["fg"] = "#333333"
        GLabel_16["justify"] = "center"
        GLabel_16["text"] = "Tables List"
        GLabel_16.place(x=0,y=230,width=181,height=30)

        GLabel_530=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_530["font"] = ft
        GLabel_530["fg"] = "#333333"
        GLabel_530["justify"] = "center"
        GLabel_530["text"] = "Tables After Operations"
        GLabel_530.place(x=418,y=230,width=181,height=30)

        GLabel_364=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_364["font"] = ft
        GLabel_364["fg"] = "#333333"
        GLabel_364["justify"] = "center"
        GLabel_364["text"] = "SELECT"
        GLabel_364.place(x=190,y=260,width=80,height=30)

        GListBox_935=tk.Listbox(root)
        GListBox_935["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_935["font"] = ft
        GListBox_935["fg"] = "#333333"
        GListBox_935["justify"] = "center"
        GListBox_935.place(x=280,y=260,width=80,height=30)

        GLabel_490=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_490["font"] = ft
        GLabel_490["fg"] = "#333333"
        GLabel_490["justify"] = "center"
        GLabel_490["text"] = "FROM"
        GLabel_490.place(x=190,y=310,width=80,height=30)

        GListBox_847=tk.Listbox(root)
        GListBox_847["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_847["font"] = ft
        GListBox_847["fg"] = "#333333"
        GListBox_847["justify"] = "center"
        GListBox_847.place(x=280,y=310,width=80,height=30)

        GLabel_161=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_161["font"] = ft
        GLabel_161["fg"] = "#333333"
        GLabel_161["justify"] = "center"
        GLabel_161["text"] = "OPERATION"
        GLabel_161.place(x=190,y=360,width=80,height=30)

        GListBox_907=tk.Listbox(root)
        GListBox_907["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_907["font"] = ft
        GListBox_907["fg"] = "#333333"
        GListBox_907["justify"] = "center"
        GListBox_907.place(x=280,y=360,width=80,height=30)

        GListBox_713=tk.Listbox(root)
        GListBox_713["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_713["font"] = ft
        GListBox_713["fg"] = "#333333"
        GListBox_713["justify"] = "center"
        GListBox_713.place(x=210,y=400,width=60,height=25)

        GListBox_421=tk.Listbox(root)
        GListBox_421["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_421["font"] = ft
        GListBox_421["fg"] = "#333333"
        GListBox_421["justify"] = "center"
        GListBox_421.place(x=280,y=400,width=60,height=25)

        GLineEdit_799=tk.Entry(root)
        GLineEdit_799["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_799["font"] = ft
        GLineEdit_799["fg"] = "#333333"
        GLineEdit_799["justify"] = "center"
        GLineEdit_799["text"] = "Entry"
        GLineEdit_799.place(x=350,y=400,width=60,height=25)

        GButton_243=tk.Button(root)
        GButton_243["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_243["font"] = ft
        GButton_243["fg"] = "#000000"
        GButton_243["justify"] = "center"
        GButton_243["text"] = "Execute"
        GButton_243.place(x=280,y=450,width=70,height=25)
        GButton_243["command"] = self.GButton_243_command

    def GButton_243_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
