from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.text import Label as CoreLabel
import math
import string


import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class DrawSpace(Widget):
    def build(self):
        self.text = Root.text_input

    def on_touch_down(self, touch):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)

        lines = self.text.split('\n')

        a = 600 # 0 - 1200
        b = -300   # 0 - 1040
        flowing = False

        for instruction in lines:
            if instruction != "":
                while instruction[0] == ' ':
                    instruction = instruction[1:]
                if instruction != "":
                    if("MOVE" in instruction):
                        instruction = instruction[8:]

                        if(',' in instruction):
                            comma = instruction.index(',')
                            c = a - int(instruction[:comma])
                            instruction = instruction[comma+2:]

                            if (']' in instruction):
                                comma = instruction.index(']')
                                d = b - int(instruction[:comma])
                                instruction = instruction[comma + 2:]

                                with self.canvas:
                                    if(flowing):
                                        Line(points=[200 + a / 2, b / 2, 200 + c / 2, d / 2], width=3)
                                    else:
                                        Line(points=[200 + a / 2, b / 2, 200 + c / 2, d / 2], width=1)

                                a = c
                                b = d

                    if ("WAIT" in instruction) and flowing:
                        instruction = instruction[8:]

                        if (']' in instruction):
                            comma = instruction.index(']')
                            size = math.sqrt(int(instruction[:comma])*1000)
                            instruction = instruction[comma + 2:]

                            with self.canvas:
                                Color(1, 0, 1)
                                Ellipse(pos=[200 + a / 2 - size/2, b / 2 - size/2], size=(size,size))
                                Color(1, 1, 0)

                    if ("FLOW" in instruction):
                        flowing = True
                        with self.canvas:
                            Color(1, 1, 0)
                    if ("BLOCK" in instruction):
                        flowing = False
                        with self.canvas:
                            Color(1, 0, 0)
        label = CoreLabel(text="(" + str(600-a) + "," + str(-300-b) + ')', font_size=20)
        label.refresh()
        text = label.texture
        with self.canvas:
            Rectangle(size=text.size, pos=(225,25), texture=text)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class Editor(App):
    def build(self):
        self.title = 'Pannenkoek Studio'
    pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('DrawSpace', cls=DrawSpace)

if __name__ == '__main__':
    Editor().run()
