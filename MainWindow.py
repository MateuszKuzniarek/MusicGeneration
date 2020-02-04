import os
import threading
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename, StringVar, asksaveasfile
from tkinter import ttk, messagebox

from GUIUtils import GUIUtils
from ModelCreationWindow import ModelCreationWindow


class MainWindow:
    WIDTH = 500
    HEIGHT = 500

    def __init__(self, generator_facade):
        self.root = tk.Tk()
        self.root.title('Composer')
        self.root.resizable(False, False)
        self.model_label_text = StringVar()
        self.duration_seconds = StringVar()
        self.player_time = StringVar()
        self.should_timer_stop = False
        self.generator_facade = generator_facade
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH, highlightthickness=0,
                                bg=GUIUtils.BACKGROUND_COLOR)
        self.background_image = GUIUtils.get_background_image()
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        self.create_model_button = GUIUtils.init_button(self.root, 'create model', self.create_model_button_callback)
        self.load_model_button = GUIUtils.init_button(self.root, 'load model', self.load_model_button_callback)
        self.save_model_button = GUIUtils.init_button(self.root, 'save model', self.save_model_button_callback, 'disabled')
        self.model_label = GUIUtils.set_label(self.canvas, relx=0.1, rely=0.05, stringvar=self.model_label_text,
                                              change_callback=self.on_model_label_change)
        self.generate_button = GUIUtils.init_button(self.root, 'generate', self.generate_button_callback, 'disabled')
        self.save_melody_button = GUIUtils.init_button(self.root, 'save melody', self.save_melody_button_callback, 'disabled')
        self.play_icon = tk.PhotoImage(file='./img/play2.png')
        self.stop_icon = tk.PhotoImage(file='./img/stop2.png')
        self.melody_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.player_time_label = GUIUtils.set_label(self.canvas, relx=0.4, rely=0.65, stringvar=self.player_time,
                                              change_callback=self.on_timer_label_change)
        self.play_melody_button = GUIUtils.init_button(self.root, None, self.play_melody_button_callback, 'disabled', 50)
        self.stop_melody_button = GUIUtils.init_button(self.root, None, self.stop_melody_button_callback, 'disabled', 50)

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
        self.create_model_button.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)
        self.load_model_button.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.1)
        self.save_model_button.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

    def init_model_label(self):
        self.set_model_label_text('')

    def init_duration_frame(self):
        self.canvas.create_text(0.1*self.WIDTH, 0.3*self.HEIGHT, text='duration (in seconds): ', anchor='w')
        seconds_entry = tk.Entry(self.root, textvariable=self.duration_seconds)
        seconds_entry.place(relx=0.5, rely=0.3, relwidth=0.4, anchor='w')

    def init_melody_player_frame(self):
        self.play_melody_button.place(relx=0.1, rely=0.6, relwidth=0.1, relheight=0.1)
        self.play_melody_button.config(image=self.play_icon, compound='left')
        self.stop_melody_button.place(relx=0.25, rely=0.6, relwidth=0.1, relheight=0.1)
        self.stop_melody_button.config(image=self.stop_icon, compound='left')
        self.player_time.set('00:00')
        self.melody_progress_bar.place(relx=0.5, rely=0.65, relwidth=0.4, anchor='w')

    def init_generate_button(self):
        self.generate_button.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)

    def init_save_melody_button(self):
        self.save_melody_button.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

    def set_model_label_text(self, model_name):
        self.model_label_text.set('Current model: ' + model_name)

    def on_model_label_change(self, varname, index, mode):
        self.canvas.itemconfigure(self.model_label, text=self.root.getvar(varname))

    def on_timer_label_change(self, varname, index, mode):
        self.canvas.itemconfigure(self.player_time_label, text=self.root.getvar(varname))

    def generate_button_callback(self):
        if GUIUtils.is_positive_integer(self.duration_seconds.get()):
            try:
                duration = int(self.duration_seconds.get())
                self.generator_facade.generate_melody(duration)
                self.melody_progress_bar.configure(max=duration)
                self.refresh_buttons_after_generating_melody()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", 'Invalid duration')

    def save_melody_button_callback(self):
        try:
            file = asksaveasfile(mode='w', defaultextension='.midi')
            if file is not None:
                self.generator_facade.save_melody(file.name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def validate_spinbox(new_value):
        if new_value.isdigit():
            new_value = int(new_value)
            if 0 <= new_value <= 60:
                return True
        return False

    def create_model_button_callback(self):
        window = ModelCreationWindow(self.generator_facade, self)
        window.display_window()

    def load_model_button_callback(self):
        try:
            file_path = askopenfilename(defaultextension=self.generator_facade.get_model_file_format())
            if self.generator_facade.load_model(file_path):
                self.set_model_label_text(os.path.basename(file_path))
            self.refresh_buttons_after_updating_model()
        except ValueError:
            messagebox.showerror("Error", 'Invalid file')
        except Exception as e:
            messagebox.showerror("Error", repr(e))

    def save_model_button_callback(self):
        try:
            file = asksaveasfile(mode='w', defaultextension=self.generator_facade.get_model_file_format())
            if file is not None:
                self.generator_facade.save_model(file.name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def play_melody_button_callback(self):
        try:
            self.generator_facade.play_melody()
            timer_thread = threading.Thread(target=self.start_timer, args=(self.generator_facade.duration,))
            timer_thread.start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_melody_button_callback(self):
        try:
            self.generator_facade.stop_melody()
            self.reset_timer()
            self.should_timer_stop = True
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
