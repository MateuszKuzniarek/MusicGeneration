import os
import threading
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename, StringVar, asksaveasfile, IntVar
from tkinter import ttk


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
        self.player_time = StringVar()
        self.should_timer_stop = False
        self.generator_facade = generator_facade
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH, highlightthickness=0,
                           bg=self.BACKGROUND_COLOR)
        self.model_buttons_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.create_model_button = self.init_button(self.model_buttons_frame, 'create model', None)
        self.load_model_button = self.init_button(self.model_buttons_frame, 'load model', self.load_model_button_callback)
        self.save_model_button = self.init_button(self.model_buttons_frame, 'save model', self.save_model_button_callback, 'disabled')
        self.generation_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.generate_button = self.init_button(self.generation_frame, 'generate', self.generate_button_callback, 'disabled')
        self.melody_saving_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.save_melody_button = self.init_button(self.melody_saving_frame, 'save melody', self.save_melody_button_callback, 'disabled')
        self.melody_player_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.play_icon = tk.PhotoImage(file='./img/play2.png')
        self.stop_icon = tk.PhotoImage(file='./img/stop2.png')
        self.melody_progress_bar = ttk.Progressbar(self.melody_player_frame, orient='horizontal', length=300, mode='determinate')
        self.player_time_label = tk.Label(self.melody_player_frame, textvariable=self.player_time, bg=self.BACKGROUND_COLOR)

        self.play_melody_button = self.init_button(self.melody_player_frame, None, self.play_melody_button_callback, 'disabled', 50)
        self.stop_melody_button = self.init_button(self.melody_player_frame, None, self.stop_melody_button_callback, 'disabled', 50)

        self.init_widgets()

    def init_widgets(self):
        self.canvas.pack()
        self.init_model_buttons()
        self.init_model_label()
        self.init_duration_frame()
        self.init_generate_button()
        self.init_save_melody_button()
        self.init_melody_player_frame()

    def init_model_buttons(self):
        self.model_buttons_frame.place(rely=0.1, relwidth=1, relheight=0.1)

        self.create_model_button.grid(row=0, column=0, padx=10, sticky='nsew')
        self.load_model_button.grid(row=0, column=1, padx=10, sticky='nsew')
        self.save_model_button.grid(row=0, column=2, padx=10, sticky='nsew')
        self.save_model_button

        self.model_buttons_frame.grid_columnconfigure(0, weight=1)
        self.model_buttons_frame.grid_columnconfigure(1, weight=1)
        self.model_buttons_frame.grid_columnconfigure(2, weight=1)
        self.model_buttons_frame.grid_rowconfigure(0, weight=1)

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

    def init_melody_player_frame(self):
        self.melody_player_frame.place(rely=0.6, relwidth=1, relheight=0.1)
        self.play_melody_button.grid(row=0, column=0, padx=10, sticky='ns')
        self.play_melody_button.config(image=self.play_icon, compound='left')
        self.stop_melody_button.grid(row=0, column=1, padx=10, sticky='ns')
        self.stop_melody_button.config(image=self.stop_icon, compound='left')
        self.player_time.set('00:00')
        self.player_time_label.grid(row=0, column=2, padx=10)
        self.melody_progress_bar.grid(row=0, column=3, padx=10)
        self.melody_player_frame.columnconfigure(3, weight=1)
        self.melody_player_frame.rowconfigure(0, weight=1)

    def init_generate_button(self):
        self.generation_frame.place(rely=0.4, relwidth=1, relheight=0.1)
        self.generate_button.pack(side='top', expand=True,  fill='y')

    def init_save_melody_button(self):
        self.melody_saving_frame.place(rely=0.8, relwidth=1, relheight=0.1)
        self.save_melody_button.pack(side='top', expand=True,  fill='y')

    def generate_button_callback(self):
        self.root.grab_set()
        total_melody_time = self.duration_minutes.get() * 60 + self.duration_seconds.get()
        self.generator_facade.generate_melody(total_melody_time)
        self.melody_progress_bar.configure(max=total_melody_time)
        self.refresh_buttons_after_generating_melody()
        self.root.grab_release()

    def save_melody_button_callback(self):
        self.root.grab_set()
        file = asksaveasfile(mode='w', defaultextension='.midi')
        if file is not None:
            self.generator_facade.save_melody(file.name)
        self.root.grab_release()

    @staticmethod
    def validate_spinbox(new_value):
        if new_value.isdigit():
            new_value = int(new_value)
            if 0 <= new_value <= 60:
                return True
        return False

    def on_enter(self, e):
        if e.widget['state'] == 'normal':
            e.widget['background'] = self.HOVER_COLOR

    def on_leave(self, e):
        e.widget['background'] = self.BUTTON_COLOR

    def init_button(self, frame, text, command, state='normal', width=16):
        button = tk.Button(frame, text=text, width=width, activebackground=self.ACTIVE_COLOR, bd=0,
                           background=self.BUTTON_COLOR, relief='flat', command=command, state=state)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def load_model_button_callback(self):
        self.root.grab_set()
        file_path = askopenfilename(defaultextension=self.generator_facade.get_model_file_format())
        if self.generator_facade.load_model(file_path):
            self.model_label_text.set('Current model: ' + os.path.basename(file_path))
        self.refresh_buttons_after_updating_model()
        self.root.grab_release()

    def save_model_button_callback(self):
        self.root.grab_set()
        file = asksaveasfile(mode='w', defaultextension=self.generator_facade.get_model_file_format())
        if file is not None:
            self.generator_facade.save_model(file.name)
        self.root.grab_release()

    def play_melody_button_callback(self):
        self.generator_facade.play_melody()
        timer_thread = threading.Thread(target=self.start_timer, args=(self.generator_facade.duration,))
        timer_thread.start()

    def stop_melody_button_callback(self):
        self.generator_facade.stop_melody()
        self.reset_timer()
        self.should_timer_stop = True

    def refresh_buttons_after_updating_model(self):
        if self.generator_facade.is_model_loaded():
            self.save_model_button.config(state='normal')
            self.generate_button.config(state='normal')

    def refresh_buttons_after_generating_melody(self):
        if self.generator_facade.is_melody_generated():
            self.save_melody_button.config(state='normal')
            self.play_melody_button.config(state='normal')
            self.stop_melody_button.config(state='normal')

    def display_window(self):
        self.root.mainloop()

    def reset_timer(self):
        self.player_time.set('00:00')
        self.melody_progress_bar.configure(value=0)

    def start_timer(self, total_time):
        current_time = 0
        self.should_timer_stop = False
        while current_time <= total_time and not self.should_timer_stop:
            minutes, seconds = divmod(current_time, 60)
            minutes = round(minutes)
            seconds = round(seconds)
            formatted_time = '{:02d}:{:02d}'.format(minutes, seconds)
            self.player_time.set(formatted_time)
            self.melody_progress_bar.configure(value=current_time)
            time.sleep(1)
            current_time += 1
        self.reset_timer()
        self.should_timer_stop = False
