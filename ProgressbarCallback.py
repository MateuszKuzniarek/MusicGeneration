from tensorflow import keras
from tensorflow_core.python.keras.callbacks import Callback


class ProgressbarCallback(keras.callbacks.Callback):
    def __init__(self, progressbar):
        super(ProgressbarCallback, self).__init__()
        self.progressbar = progressbar

    def on_epoch_end(self, epoch, logs=None):
        self.progressbar.configure(value=epoch+1)
