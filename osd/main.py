from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class DrawSpace(Widget):
    def build(self):
        self.text = Root.text_input


class Root(FloatLayout):
    pass


class PannenkoekenApp(App):

    def build(self):
        self.title = "Pannenkoekenswag"


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    PannenkoekenApp().run()
