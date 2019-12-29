import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, StringVar, asksaveasfile

from RecurrentNeuralNetwork import RecurrentNeuralNetwork


class MainWindow:

    WIDTH = 500
    HEIGHT = 500
    BACKGROUND_COLOR = '#c3d6c3'
    BUTTON_COLOR = '#4CAF50'
    HOVER_COLOR = '#3e8e41'
    ACTIVE_COLOR = '#7db37f'

    root = None
    model_label_text = None
    neural_network = RecurrentNeuralNetwork()

    def __init__(self):
        self.root = tk.Tk()
        canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH, highlightthickness=0, bg=self.BACKGROUND_COLOR)
        canvas.pack()
        self.init_model_buttons()
        self.init_model_label()
        #generate_button.pack()

    def init_model_buttons(self):
        model_buttons_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        model_buttons_frame.place(rely=0.1, relwidth=1, relheight=0.1)

        create_model_button = self.init_button(model_buttons_frame, 'create model', None)
        create_model_button.grid(row=0, column=0, padx=10, sticky='nsew')
        load_model_button = self.init_button(model_buttons_frame, 'load model', self.load_model_button_callback)
        load_model_button.grid(row=0, column=1, padx=10, sticky='nsew')
        save_model_button = self.init_button(model_buttons_frame, 'save model', self.save_model_button_callback)
        save_model_button.grid(row=0, column=2, padx=10, sticky='nsew')

        model_buttons_frame.grid_columnconfigure(0, weight=1)
        model_buttons_frame.grid_columnconfigure(1, weight=1)
        model_buttons_frame.grid_columnconfigure(2, weight=1)
        model_buttons_frame.grid_rowconfigure(0, weight=1)

    def init_model_label(self):
        self.model_label_text = StringVar()
        self.model_label_text.set('Current model: ')
        model_label_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        model_label_frame.place(relwidth=1, relheight=0.1)

        model_label = tk.Label(model_label_frame, textvariable=self.model_label_text, bg=self.BACKGROUND_COLOR, padx=10)
        model_label.pack(side='left')

    def on_enter(self, e):
        e.widget['background'] = self.HOVER_COLOR

    def on_leave(self, e):
        e.widget['background'] = self.BUTTON_COLOR

    def init_button(self, frame, text, command):
        button = tk.Button(frame, text=text, width=16, activebackground=self.ACTIVE_COLOR, bd=0,
                           background=self.BUTTON_COLOR, relief='flat', command=command)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def load_model_button_callback(self):
        self.root.grab_set()
        file_path = askopenfilename(defaultextension='.h5')
        self.neural_network.load_model(file_path)
        self.model_label_text.set('Current model: ' + os.path.basename(file_path))
        self.root.grab_release()

    def save_model_button_callback(self):
        self.root.grab_set()
        file = asksaveasfile(mode='w', defaultextension='.h5')
        if file is None:
            self.root.grab_release()
            return
        self.neural_network.save_model(file.name)
        self.root.grab_release()

    def display_window(self):
        self.root.mainloop()
