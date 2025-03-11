from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window

class Hellpad(App):
    def build(self):
        Window.fullscreen = 'auto'
        return Button(text="Hellpad Test!")

if __name__ == "__main__":
    Hellpad().run()