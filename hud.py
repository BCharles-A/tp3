import json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import object
import linked_list
import personalized_exception as pe

class HUD:
    def __init__(self, path_default = "setting_default.json"):
        with open(path_default, "r") as f:
            self.default_setting = json.load(f)
        self.current_setting = self.default_setting

        #animation speed in ms
        self.time = self.current_setting["time_step"]
        self.round_history = linked_list.LinkedList()

        #visual elements
        #window
        self.root = tk.Tk()
        self.root.geometry(f"{self.current_setting['canvas_dimension'][0]}x{self.current_setting['canvas_dimension'][0]}")
        self.root.config(bg="gray20")
        self.display = tk.Canvas(self.root, width=self.current_setting['canvas_dimension'][0], height=int(self.current_setting['canvas_dimension'][1]), bg="darkblue")
        
        #variables
        self.force_multiplier = self.current_setting["force_multiplier"]
        self.checkb_var = tk.BooleanVar()   #Bord
        self.checkb_var2 = tk.BooleanVar()  #Trous
        self.checkb_var3 = tk.StringVar()      #N for replay step up/down
        self.border = []
        self.holes = []
        self.objects = []
        self.objects_show = []
        
        #labels
        self.lab1 = tk.Label(self.root, text="Jeu de Billard🎱", font=("Arial",20), bg="gray20", fg="white")
        self.lab2 = tk.Label(self.root, text="angle", bg="gray20", fg="yellow", font=("Arial", 12))
        self.lab3 = tk.Label(self.root, text="force", bg="gray20", fg="yellow", font=("Arial", 12))
        self.lab4 = tk.Label(self.root, text="Tir : 0/0", bg="gray20", fg="yellow", font=("Arial", 12))
        self.lab5 = tk.Label(self.root, text="Étape : 0/0", bg="gray20", fg="yellow", font=("Arial", 12))
        self.lab6 = tk.Label(self.root, text="N :", bg="gray20", fg="yellow", font=("Arial", 12))
        #inputs
        self.spinbox_angle = tk.Spinbox(self.root, from_=0, to=360, bd=2, command=self.arrow_update)
        self.spinbox_force = tk.Spinbox(self.root, from_=0, to=100, bd=2, command=self.arrow_update, increment=10)
        self.spinbox_n = tk.Spinbox(self.root, from_=1, to=100, bd=2, textvariable=self.checkb_var3)
        self.button_shot = tk.Button(self.root, text="Tirer", command=self.play, bg="yellow", bd=2)
        self.checkbox = tk.Checkbutton(self.root, text="Bord", bg="gray20", fg="white", variable=self.checkb_var, onvalue=True, offvalue=False, command=self.plan_update, )
        self.checkbox2 = tk.Checkbutton(self.root, text="Trous", bg="gray20", fg="white", variable=self.checkb_var2, onvalue=True, offvalue=False, command=self.plan_update)
        self.button_replay_first = tk.Button(self.root, text="|◀", command=self.replay_first, bg="lightblue", bd=2)
        self.button_replay_up = tk.Button(self.root, text="1 ▶", command=self.replay_step_up, bg="lightblue", bd=2)
        self.button_replay_down = tk.Button(self.root, text="◀ 1", command=self.replay_step_down, bg="lightblue", bd=2)
        self.button_replay_last = tk.Button(self.root, text="▶|", command=self.replay_last, bg="lightblue", bd=2)
        self.button_replay_up_n = tk.Button(self.root, text="◀ N", command=self.replay_step_up_n, bg="lightblue", bd=2)
        self.button_replay_down_n = tk.Button(self.root, text="N ▶", command=self.replay_step_down_n, bg="lightblue", bd=2)
        self.button_round_up = tk.Button(self.root, text="tir prochain", command=self.round_up, bg="lightblue", bd=2)
        self.button_round_down = tk.Button(self.root, text="tir précédent", command=self.round_down, bg="lightblue", bd=2)
        self.button_reset = tk.Button(self.root, text="Réinitialiser", command=self.reset_command, bg="darkred", fg="white", bd=2)
        self.button_configure = tk.Button(self.root, text="Changer de configuration", command=self.configure, fg="white", bg="darkgreen", bd=2)
        #pointer
        self.arrow = self.display.create_line(0,0,0,0, fill="white", arrow="last")
        #Load the objects
        self.load_objects()
        #state
        self.motion = False
    
    def load_objects(self):
        side_thickness = 25
        main_obj_data = self.current_setting["objects"]["main"]
        main_obj = object.Object(
                velocity = np.array(main_obj_data["velocity_start"]),
                position = np.array(main_obj_data["position_start"]),
                radius = self.current_setting["object_radius"],
                resistance = self.current_setting["friction_value"],
                epsilon = self.current_setting["min_speed"],
                name = main_obj_data["name"],
                color = main_obj_data["color"],
                pos_min = np.array([side_thickness, side_thickness]),
                pos_max = np.array([value-side_thickness for value in self.current_setting["canvas_dimension"]])
        )
        self.objects.append(main_obj)
        for element in self.current_setting["objects"]["others"].values():
            obj = object.Object(
                velocity = np.array(element["velocity_start"]),
                position = np.array(element["position_start"]),
                radius = self.current_setting["object_radius"],
                resistance = self.current_setting["friction_value"],
                epsilon = self.current_setting["min_speed"],
                name = element["name"],
                color = element["color"],
                pos_min = np.array([side_thickness, side_thickness]),
                pos_max = np.array([value-side_thickness for value in self.current_setting["canvas_dimension"]])
            )
            self.objects.append(obj)
    
    #Toggle the edges and the holes of the table
    def plan_update(self):
        x_middle = int(self.current_setting["canvas_dimension"][0]/2)
        x_max = self.current_setting["canvas_dimension"][0]
        y_max = self.current_setting["canvas_dimension"][1]

        bord_color = "darkgreen"
        if self.checkb_var.get():
            self.border.append(self.display.create_rectangle(0, 0, x_max, 15, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(x_max-15, 0, x_max, y_max, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(0, y_max-13, x_max, y_max+3, fill=bord_color, outline=bord_color))
            self.border.append(self.display.create_rectangle(0, 0, 15, y_max, fill=bord_color, outline=bord_color))
        else:
            for element in self.border:
                self.display.delete(element)
            del self.border[:]
        for element in self.holes:
            self.display.delete(element)
        del self.holes[:]
        if self.checkb_var2.get():
            self.holes.append(self.display.create_oval(8,8,34,34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(x_middle-13, 8, x_middle+13, 34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(x_max-34, 8, x_max-8, 34, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(8 ,y_max-32, 34,y_max-6, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(x_middle-13, y_max-32, x_middle+13, y_max-6, fill="black", outline="black"))
            self.holes.append(self.display.create_oval(x_max-32, y_max-32, x_max-6, y_max-6, fill="black", outline="black"))

    #Change the orientation and the length of the pointer
    def arrow_update(self):
        angle = self.spinbox_angle.get()
        force = self.spinbox_force.get()
        self.display.delete(self.arrow)
        self.arrow = self.display.create_line(self.objects[0].position[0], self.objects[0].position[1], 
                                              self.objects[0].position[0] + (25 + int(force)/5)*np.cos(np.radians(int(angle))), 
                                              self.objects[0].position[1] + (25 + int(force)/5)*np.sin(np.radians(int(angle))), 
                                              fill="white", arrow="last", width=2)

    def play(self):
        self.motion = True
        #Reset the position of the objects
        for obj in self.objects_show:
            self.display.delete(obj)
        del self.objects_show[:]
        for obj in self.objects:
            self.objects_show.append(self.display.create_oval(obj.position[0]-obj.radius, obj.position[1]-obj.radius, obj.position[0]+obj.radius, obj.position[1]+obj.radius, fill=obj.color, outline="Black"))

        #Add the current round to the history
        self.round_history.append(linked_list.LinkedList())
        #Delete the pointer
        self.display.delete(self.arrow)
        #set the initial velocity of the main ball
        angle = self.spinbox_angle.get()
        force = self.spinbox_force.get()
        self.objects[0].set_velocity(np.array([self.force_multiplier*int(force)*np.cos(np.radians(int(angle)))*(self.time/1000), 
                                               self.force_multiplier*int(force)*np.sin(np.radians(int(angle)))*(self.time/1000)
                                               ]))
        #Start the anumation
        self.animation()
    
    #Animate the movements of the objects
    def animation(self):
        history = {}
        #Mouvement
        for i, obj in enumerate(self.objects):
            pos = obj.position
            obj.move(self.time)
            self.display.move(self.objects_show[i], obj.position[0]-pos[0], obj.position[1]-pos[1])
            history[obj.name] = obj.position
        self.round_history.get().append(history)
        #Calculating the total velocity of the objects
        total_velocity = 0
        for obj in self.objects:
            total_velocity += np.linalg.norm(obj.velocity)
        #Collision check
        for i in range(len(self.objects) - 1):
            for j in range(i+1, len(self.objects)):
                self.objects[i].collision(self.objects[j])
        #Stop if all the objects are static then show the pointer
        if total_velocity > 0:
            self.root.after(self.time, self.animation)
        else:
            self.arrow_update()
            self.replay_label_update()
            self.motion = False

    def replay_label_update(self):
        self.lab4.config(text=f"Tir : {self.round_history.index+1}/{self.round_history.len()}")
        self.lab5.config(text=f"Étape : {self.round_history.get().index+1}/{self.round_history.get().size}")

    def replay(self):
        if not self.motion:
            self.display.delete(self.arrow)
            for obj in self.objects_show:
                self.display.delete(obj)
            del self.objects_show[:]
            history = self.round_history.get().get()
            for obj in self.objects:
                self.objects_show.append(self.display.create_oval(history[obj.name][0]-obj.radius, history[obj.name][1]-obj.radius, history[obj.name][0]+obj.radius, history[obj.name][1]+obj.radius, fill=obj.color, outline="Black"))
            self.replay_label_update()

    def replay_first(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.get().set_cursor(0)
            self.replay()

    def replay_step_up(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.get().step_up()
            self.replay()

    def replay_step_down(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.get().step_down()    
            self.replay()

    def replay_last(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.get().set_cursor(self.round_history.get().size - 1)
            self.replay()
            self.arrow_update()

    def replay_step_up_n(self):
        if self.round_history.size != 0 and not self.motion:
            increment = int(self.checkb_var3.get())
            if self.round_history.get().index - increment >= 0:
                self.round_history.get().set_cursor(self.round_history.get().index - increment)
                self.replay()
            else:
                self.replay_first()

    def replay_step_down_n(self):
        if self.round_history.size != 0 and not self.motion:
            increment = int(self.checkb_var3.get())
            if self.round_history.get().index + increment < self.round_history.get().size:
                self.round_history.get().set_cursor(self.round_history.get().index + increment)
                self.replay()
            else:
                self.replay_last()

    def round_up(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.step_up()
            self.replay()

    def round_down(self):
        if self.round_history.size != 0 and not self.motion:
            self.round_history.step_down()
            self.replay()
    
    def reset_command(self):
        try:
            self.reset()
        except pe.InMotion as e:
            tk.messagebox.showerror("Erreur", e)

    def reset(self, setting = None, resize = False):
        if self.motion:
            raise pe.InMotion("Impossible de réinitialiser pendant un mouvement")
        if setting is not None:
            self.current_setting = setting
        #reset objects position
        for obj in self.objects_show:
            self.display.delete(obj)
        del self.objects_show[:]
        del self.objects[:]
        self.load_objects()
        for obj in self.objects:
            self.objects_show.append(self.display.create_oval(obj.position[0]-obj.radius, obj.position[1]-obj.radius, obj.position[0]+obj.radius, obj.position[1]+obj.radius, fill=obj.color, outline="Black"))
        #reset history
        self.round_history = linked_list.LinkedList()
        #reset labels
        self.lab4.config(text="Tir : 0/0")
        self.lab5.config(text="Étape : 0/0")
        #reset other elements
        self.checkb_var.set(False)
        self.checkb_var2.set(False)
        self.plan_update()
        self.arrow_update()
        if resize:
            self.root.geometry(f"{self.current_setting['canvas_dimension'][0]}x{self.current_setting['canvas_dimension'][0]}")
            self.display.config(width=self.current_setting['canvas_dimension'][0], height=int(self.current_setting['canvas_dimension'][1]))
            self.show()

    def configure(self):
        path = filedialog.askopenfilename()
        try:
            current_dimension = self.current_setting["canvas_dimension"]
            with open(path, "r") as f:
                self.current_setting = json.load(f)
            self.reset(resize=current_dimension != self.current_setting["canvas_dimension"])

        except pe.InMotion as e:
            tk.messagebox.showerror("Erreur",e)

        except Exception as e:
            tk.messagebox.showerror("Erreur", f"{e}\nLes configrations seront réinitialisées aux valeurs par défaut")
            self.reset(setting=self.default_setting, resize=True)


    def show(self):
        x_middle = int(self.current_setting["canvas_dimension"][0]/2)
        y_canvas = self.current_setting["canvas_dimension"][1]

        self.lab1.pack()
        #Canvas
        self.display.pack(anchor="w")
        #Angle
        self.spinbox_angle.place(x=60, y=y_canvas+50, height=30, width=80)
        self.lab2.place(x=10, y=y_canvas+55, height=20, width=50)
        #Force
        self.spinbox_force.place(x=x_middle-40, y=y_canvas+50, height=30, width=80)
        self.lab3.place(x=x_middle-90, y=y_canvas+55, height=20, width=50)
        #Play
        self.button_shot.place(x=x_middle+55, y=y_canvas+49, height=34, width=x_middle-60)
        #Setting
        self.checkbox.place(x=10, y=y_canvas+90, height=30, width=80)
        self.checkbox2.place(x=90, y=y_canvas+90, height=30, width=80)
        #Replay
        self.lab4.place(x=110, y=y_canvas+125, height=30, width=60)
        self.button_round_up.place(x=185, y=y_canvas+130, height=23, width=90)
        self.button_round_down.place(x=10, y=y_canvas+130, height=23, width=90)
        #Replay 2
        self.lab5.place(x=40, y=y_canvas+150, height=30, width=200)
        self.button_replay_first.place(x=10, y=y_canvas+180, height=30, width=40)
        self.button_replay_up_n.place(x=55, y=y_canvas+180, height=30, width=40)
        self.button_replay_down.place(x=100, y=y_canvas+180, height=30, width=40)
        self.button_replay_up.place(x=145, y=y_canvas+180, height=30, width=40)
        self.button_replay_down_n.place(x=190, y=y_canvas+180, height=30, width=40)
        self.button_replay_last.place(x=235, y=y_canvas+180, height=30, width=40)
        self.lab6.place(x=280, y=y_canvas+180, height=30, width=30)
        self.spinbox_n.place(x=310, y=y_canvas+180, height=30, width=40)
        #Additional buttons
        self.button_reset.place(x=10, y=y_canvas+220, height=30, width=100)
        self.button_configure.place(x=120, y=y_canvas+220, height=30, width=150)
        #Objects show
        for element in self.objects:
            self.objects_show.append(self.display.create_oval(element.position[0]-element.radius, element.position[1]-element.radius, element.position[0]+element.radius, element.position[1]+element.radius, fill=element.color, outline="Black"))
        #arrow show
        self.arrow_update()
    
    def launch(self):
        self.show()
        self.root.mainloop()