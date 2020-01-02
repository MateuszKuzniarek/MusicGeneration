import tkinter as tk


class GUIUtils:
    BACKGROUND_COLOR = '#e0f0da'
    BUTTON_COLOR = '#4CAF50'
    HOVER_COLOR = '#3e8e41'
    ACTIVE_COLOR = '#7db37f'

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
