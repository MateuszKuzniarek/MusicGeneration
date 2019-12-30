import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, StringVar, asksaveasfile, IntVar

from RecurrentNeuralNetwork import RecurrentNeuralNetwork


class MainWindow:
    WIDTH = 500
    HEIGHT = 500
    BACKGROUND_COLOR = '#c3d6c3'
    BUTTON_COLOR = '#4CAF50'
    HOVER_COLOR = '#3e8e41'
    ACTIVE_COLOR = '#7db37f'

    def __init__(self, generator_facade):
        self.root = tk.Tk()
        self.model_label_text = StringVar()
        self.duration_minutes = IntVar()
        self.duration_seconds = IntVar()
        self.generator_facade = generator_facade
        canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH, highlightthickness=0,
                           bg=self.BACKGROUND_COLOR)
        canvas.pack()
        self.init_model_buttons()
        self.init_model_label()
        self.init_duration_frame()
        self.init_generate_button()

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
        self.model_label_text.set('Current model: ')
        model_label_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        model_label_frame.place(relwidth=1, relheight=0.1)

        model_label = tk.Label(model_label_frame, textvariable=self.model_label_text, bg=self.BACKGROUND_COLOR, padx=10)
        model_label.pack(side='left')

    def init_duration_frame(self):
        duration_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        duration_frame.place(rely=0.3, relwidth=1, relheight=0.1)
        duration_label = tk.Label(duration_frame, text='duration: ', bg=self.BACKGROUND_COLOR)
        duration_label.grid(row=0, column=1, padx=0)
        validate_command = (duration_frame.register(self.validate_spinbox), '%P')
        minute_spinbox = tk.Spinbox(duration_frame, from_=0, to=60, width=5, validate='key',
                                    validatecommand=validate_command, textvariable=self.duration_minutes)
        minute_spinbox.grid(row=0, column=2, padx=10)
        seconds_spinbox = tk.Spinbox(duration_frame, from_=0, to=60, width=5, validate='key',
                                     validatecommand=validate_command, textvariable=self.duration_seconds)
        seconds_spinbox.grid(row=0, column=3, padx=10)

        duration_frame.grid_columnconfigure(0, weight=1)
        duration_frame.grid_columnconfigure(4, weight=1)

    def init_generate_button(self):
        generation_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        generation_frame.place(rely=0.5, relwidth=1, relheight=0.1)

        generate_button = self.init_button(generation_frame, 'generate', self.generate_button_callback)

        generate_button.pack(side='top', expand=True,  fill='y')

    def generate_button_callback(self):
        self.root.grab_set()
        self.generator_facade.generate_melody(self.duration_minutes.get() * 60 + self.duration_seconds.get())
        self.root.grab_release()

    def validate_spinbox(self, new_value):
        if new_value.isdigit():
            new_value = int(new_value)
            if 0 <= new_value <= 60:
                return True
        return False

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
        file_path = askopenfilename(defaultextension=self.generator_facade.get_model_file_format())
        if self.generator_facade.load_model(file_path):
            self.model_label_text.set('Current model: ' + os.path.basename(file_path))
        self.root.grab_release()

    def save_model_button_callback(self):
        self.root.grab_set()
        file = asksaveasfile(mode='w', defaultextension=self.generator_facade.get_model_file_format())
        if file is not None:
            self.generator_facade.save_model(file.name)
        self.root.grab_release()

    def display_window(self):
        self.root.mainloop()
