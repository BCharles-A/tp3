import tkinter as tk

class HUD:
    def __init__(self, size=100):
        #window
        self.root = tk.Tk()
        self.root.geometry(f"{size}x{size}")
        self.root.config(bg="gray20")
        self.display = tk.Canvas(self.root, width=size, height=int(size/2), bg="darkblue")
        #variables
        self.size = size/2
        self.checkb_var = tk.BooleanVar()
        self.checkb_var2 = tk.BooleanVar()
        self.border = []
        self.holes = []
        #labels
        self.lab1 = tk.Label(self.root, text="Jeu de Bliard🎱", font=("Arial",20), bg="gray20", fg="white")
        self.lab2 = tk.Label(self.root, text="angle", bg="gray20", fg="yellow", font=("Arial", 12))
        self.lab3 = tk.Label(self.root, text="force", bg="gray20", fg="yellow", font=("Arial", 12))
        #inputs
        self.spinbox_angle = tk.Spinbox(self.root, from_=0, to=360, bd=2, command=self.arrow_update)
        self.spinbox_force = tk.Spinbox(self.root, from_=0, to=100, bd=2, command=self.arrow_update, increment=10)
        self.button_shot = tk.Button(self.root, text="Tirer", command=self.play, bg="yellow", bd=2)
        self.checkbox = tk.Checkbutton(self.root, text="Bord", bg="gray20", fg="white", variable=self.checkb_var, onvalue=True, offvalue=False, command=self.plan_update, )
        self.checkbox2 = tk.Checkbutton(self.root, text="Trous", bg="gray20", fg="white", variable=self.checkb_var2, onvalue=True, offvalue=False, command=self.plan_update)

    def plan_update(self):
        bord_color = "darkgreen"
        if self.checkb_var.get():
            self.border.append(self.display.create_rectangle(0, 0, self.size*2, 15, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(self.size*2-15, 0, self.size*2, self.size, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(0, self.size-13, self.size*2, self.size+3, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(0, 0, 15, self.size, fill=bord_color, outline=bord_color))
        else:
            for element in self.border:
                self.display.delete(element)
            del self.border[:]
        for element in self.holes:
            self.display.delete(element)
        del self.holes[:]
        if self.checkb_var2.get():
            self.holes.append(self.display.create_oval(8,8,34,34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(self.size-13, 8, self.size+13, 34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(self.size*2-34, 8, self.size*2-8, 34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(8 ,self.size-32, 34,self.size-6, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(self.size-13, self.size-32, self.size+13, self.size-6, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(self.size*2-32, self.size-32, self.size*2-6, self.size-6, fill="black", outline="black"))
        
    
    def arrow_update(self):
        angle = self.spinbox_angle.get()
        force = self.spinbox_force.get()
        pass

    def play(self):
        angle = self.spinbox_angle.get()
        force = self.spinbox_force.get()
        pass
        
    def show(self):
        self.lab1.pack()
        #Canvas
        self.display.pack(anchor="w")
        #Angle
        self.spinbox_angle.place(x=60, y=self.size+50, height=30, width=80)
        self.lab2.place(x=10, y=self.size+55, height=20, width=50)
        #Force
        self.spinbox_force.place(x=self.size-40, y=self.size+50, height=30, width=80)
        self.lab3.place(x=self.size-90, y=self.size+55, height=20, width=50)
        #Play
        self.button_shot.place(x=self.size+55, y=self.size+49, height=34, width=self.size-60)
        #Setting
        self.checkbox.place(x=10, y=self.size+90, height=30, width=80)
        self.checkbox2.place(x=10, y=self.size+120, height=30, width=80)

        #mainloop
        self.root.mainloop()

if __name__ == "__main__":
    test = HUD(size=500)
    test.show()