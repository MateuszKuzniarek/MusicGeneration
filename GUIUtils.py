import tkinter as tk


class GUIUtils:
    BACKGROUND_COLOR = '#e0f0da'
    BUTTON_COLOR = '#c46869'
    HOVER_COLOR = '#bd8081'
    ACTIVE_COLOR = '#a14f50'

    @staticmethod
    def on_enter(e):
        if e.widget['state'] == 'normal':
            e.widget['background'] = GUIUtils.HOVER_COLOR

    @staticmethod
    def on_leave(e):
        e.widget['background'] = GUIUtils.BUTTON_COLOR

    @staticmethod
    def init_button(frame, text, command, state='normal', width=16):
        button = tk.Button(frame, text=text, width=width, activebackground=GUIUtils.ACTIVE_COLOR, bd=0,
                           background=GUIUtils.BUTTON_COLOR, relief='flat', command=command, state=state)
        button.bind("<Enter>", GUIUtils.on_enter)
        button.bind("<Leave>", GUIUtils.on_leave)
        return button

    @staticmethod
    def get_background_image():
        photoImage = tk.PhotoImage(file='./img/background2.png')
        return photoImage

    @staticmethod
    def set_label(canvas, relx, rely, stringvar, change_callback, total_width=500, total_height=500):
        label = canvas.create_text(relx*total_width, rely*total_height, text=stringvar.get(), anchor='w')
        stringvar.trace_variable('w', change_callback)
        return label
