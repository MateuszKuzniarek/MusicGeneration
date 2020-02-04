from GeneratorFacade import GeneratorFacade
from MainWindow import MainWindow

generator_facade = GeneratorFacade()

window = MainWindow(generator_facade)
window.display_window()
