import os
import threading
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename, StringVar, asksaveasfile, IntVar
from tkinter import ttk, filedialog, messagebox

from GUIUtils import GUIUtils
from ProgressbarCallback import ProgressbarCallback


class ModelCreationWindow:
    WIDTH = 500
    HEIGHT = 500

    def __init__(self, generator_facade, parent_window):
        self.parent_window = parent_window
        self.root = tk.Toplevel()
        self.root.resizable(False, False)
        self.root.grab_set()
        self.number_of_loaded_files_variable = tk.StringVar()
        self.number_of_epochs = tk.StringVar()
        self.sequence_length = tk.StringVar()
        self.test_sample_ratio = tk.StringVar()
        self.lstm_layer_size = tk.StringVar()
        self.dense_layer_size = tk.StringVar()
        self.dropout_rate = tk.StringVar()
        self.generator_facade = generator_facade
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH, highlightthickness=0,
                                bg=GUIUtils.BACKGROUND_COLOR)
        self.load_data_set_button = GUIUtils.init_button(self.root, 'load data set', self.load_data_set_button_callback)
        self.number_of_loaded_files_label = tk.Label(self.root, textvariable=self.number_of_loaded_files_variable,
                                                     bg=GUIUtils.BACKGROUND_COLOR)
        self.progressbar = ttk.Progressbar(self.root, orient='horizontal', mode='determinate')
        self.train_button = GUIUtils.init_button(self.root, 'train', self.train_button_callback)
        self.cancel_button = GUIUtils.init_button(self.root, 'cancel', self.cancel_button_callback)
        self.epochs_number_entry = tk.Entry(self.root, textvariable=self.number_of_epochs)
        self.sequence_length_entry = tk.Entry(self.root, textvariable=self.sequence_length)
        self.test_sample_ratio_entry = tk.Entry(self.root, textvariable=self.test_sample_ratio)
        self.lstm_layer_size_entry = tk.Entry(self.root, textvariable=self.lstm_layer_size)
        self.dense_layer_size_entry = tk.Entry(self.root, textvariable=self.dense_layer_size)
        self.dropout_rate_entry = tk.Entry(self.root, textvariable=self.dropout_rate)

        self.init_widgets()

    def init_widgets(self):
        self.canvas.pack()
        self.init_data_set_loading_section()
        self.init_number_of_epochs_section()
        self.init_sequence_length_section()
        self.init_test_sample_ratio_section()
        self.init_lstm_layer_size_section()
        self.init_dense_layer_size_section()
        self.init_dropout_rate_section()
        self.init_confirmation_buttons()
        self.init_progressbar()

    def init_data_set_loading_section(self):
        self.load_data_set_button.place(relx=0.1, rely=0.1, relwidth=0.35, relheight=0.1)
        self.number_of_loaded_files_variable.set('Number of loaded files: 0')
        self.number_of_loaded_files_label.place(relx=0.55, rely=0.1, relheight=0.1)

    def init_number_of_epochs_section(self):
        epochs_label = tk.Label(self.root, text='number of epochs: ', bg=GUIUtils.BACKGROUND_COLOR)
        epochs_label.place(relx=0.1, rely=0.3)
        self.number_of_epochs.set(100)
        self.epochs_number_entry.place(relx=0.55, rely=0.3)

    def init_sequence_length_section(self):
        sequence_length_label = tk.Label(self.root, text='sequence length: ', bg=GUIUtils.BACKGROUND_COLOR)
        sequence_length_label.place(relx=0.1, rely=0.35)
        self.sequence_length.set(20)
        self.sequence_length_entry.place(relx=0.55, rely=0.35)

    def init_test_sample_ratio_section(self):
        test_sample_ratio_label = tk.Label(self.root, text='test sample ratio: ', bg=GUIUtils.BACKGROUND_COLOR)
        test_sample_ratio_label.place(relx=0.1, rely=0.40)
        self.test_sample_ratio.set(0.2)
        self.test_sample_ratio_entry.place(relx=0.55, rely=0.40)

    def init_lstm_layer_size_section(self):
        lstm_layer_size_label = tk.Label(self.root, text='lstm layer size: ', bg=GUIUtils.BACKGROUND_COLOR)
        lstm_layer_size_label.place(relx=0.1, rely=0.45)
        self.lstm_layer_size.set(256)
        self.lstm_layer_size_entry.place(relx=0.55, rely=0.45)

    def init_dense_layer_size_section(self):
        dense_layer_size_label = tk.Label(self.root, text='dense layer size: ', bg=GUIUtils.BACKGROUND_COLOR)
        dense_layer_size_label.place(relx=0.1, rely=0.50)
        self.dense_layer_size.set(256)
        self.dense_layer_size_entry.place(relx=0.55, rely=0.50)

    def init_dropout_rate_section(self):
        dropout_rate_label = tk.Label(self.root, text='dropout rate: ', bg=GUIUtils.BACKGROUND_COLOR)
        dropout_rate_label.place(relx=0.1, rely=0.55)
        self.dropout_rate.set(0.3)
        self.dropout_rate_entry.place(relx=0.55, rely=0.55)

    def init_confirmation_buttons(self):
        self.train_button.place(relx=0.1, rely=0.7, relwidth=0.35, relheight=0.1)
        self.cancel_button.place(relx=0.55, rely=0.7, relwidth=0.35, relheight=0.1)

    def init_progressbar(self):
        self.progressbar.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)
        self.progressbar.configure(value=0)

    def train_button_callback(self):
        if self.validate_entries():
            training_thread = threading.Thread(target=self.start_training)
            training_thread.start()
        else:
            messagebox.showerror("Error", "Ivalid parameters values")

    def start_training(self):
        self.disable_window()
        progressbar_callback = ProgressbarCallback(self.progressbar)
        self.progressbar.configure(max=self.number_of_epochs.get())
        self.generator_facade.train(int(self.sequence_length.get()), int(self.lstm_layer_size.get()),
                                    int(self.dense_layer_size.get()), float(self.dropout_rate.get()),
                                    int(self.number_of_epochs.get()), float(self.test_sample_ratio.get()),
                                    [progressbar_callback])
        self.parent_window.refresh_buttons_after_updating_model()
        self.parent_window.set_model_label_text('new untitled model')
        self.root.destroy()

    def disable_window(self):
        self.load_data_set_button.configure(state='disabled')
        self.cancel_button.configure(state='disabled')
        self.train_button.configure(state='disabled')
        self.epochs_number_entry.configure(state='disabled')
        self.sequence_length_entry.configure(state='disabled')
        self.lstm_layer_size_entry.configure(state='disabled')
        self.dense_layer_size_entry.configure(state='disabled')
        self.dropout_rate_entry.configure(state='disabled')
        self.test_sample_ratio_entry.configure(state='disabled')

    def cancel_button_callback(self):
        self.generator_facade.reset_data_set()
        self.root.destroy()

    def load_data_set_button_callback(self):
        files = filedialog.askopenfilenames(parent=self.root, title='Choose midi files')
        files_split_list = self.root.tk.splitlist(files)
        self.generator_facade.load_data_set(files_split_list)
        self.number_of_loaded_files_variable.set('Number of loaded files: ' + str(len(files_split_list)))

    def validate_entries(self):
        epochs_validity = self.is_positive_integer(self.number_of_epochs.get())
        sequence_length_validity = self.is_positive_integer(self.sequence_length.get())
        test_sample_ratio_validity = self.is_proper_ratio(self.test_sample_ratio.get())
        lstm_layer_size_validity = self.is_positive_integer(self.lstm_layer_size.get())
        dense_layer_size_validity = self.is_positive_integer(self.dense_layer_size.get())
        dropout_rate_validity = self.is_proper_ratio(self.dropout_rate.get())
        data_set_validity = self.generator_facade.is_data_set_loaded()
        return epochs_validity and sequence_length_validity and test_sample_ratio_validity and\
            lstm_layer_size_validity and dense_layer_size_validity and dropout_rate_validity and data_set_validity

    @staticmethod
    def is_positive_integer(number):
        if number.isdigit():
            integer = int(number)
            if 0 < integer:
                return True
        return False

    @staticmethod
    def is_proper_ratio(number):
        try:
            float_number = float(number)
            if 0 < float_number < 1:
                return True
            return False
        except ValueError:
            return False

    def display_window(self):
        self.root.mainloop()
