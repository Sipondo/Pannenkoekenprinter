from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
# Declare both screens
class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.current = 'menu'


class TestApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
