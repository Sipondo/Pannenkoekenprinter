import requests, json
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import AsyncImage

dir_path = os.path.dirname(os.path.realpath(__file__))

allies = {}
enemies = {}
maps = {}
neutral = {}

picks = []
MapImg = AsyncImage();

def request_hero_data():
    url = "https://api.hotslogs.com/Public/Data/Heroes"
    response = requests.get(url)
    data = response.json()
    response.close();

    with open(dir_path + '/data/data_heroes.json', 'w') as f:
        json.dump(data, f)
    team_dict = {}
    enemy_dict = {}
    map_dict = {}

    for i, hero in enumerate(data):
        if (hero['ImageURL']!='Probius'):
            print hero ['ImageURL'] + " [" + str(i+1) + "/" + str(len(data)) + "]"
            response = requests.get('https://www.hotslogs.com/Sitewide/HeroDetails?Hero='+hero['ImageURL'])
            input = response.text
            wins = input.split('class="rgHeader">Opposing Hero</th>', 1)[1].split('</thead><tbody>',1)[1].split('</tbody>', 1)[0].split('/Portraits/')[1:]

            scores = {}
            for win in wins:
                matchup, win = win.split('.png',1)
                winrate = float(win.split('></div></td><td>',1)[1].split(' ',1)[0])
                scores[matchup] = 100-winrate

            response.close()
            team_dict[hero['ImageURL']] = scores

            input = response.text
            wins = input.split('class="rgHeader">Team Hero</th>', 1)[1].split('</thead><tbody>', 1)[1].split('</tbody>', 1)[0].split('/Portraits/')[1:]

            scores = {}
            for win in wins:
                matchup, win = win.split('.png', 1)
                winrate = float(win.split('></div></td><td>', 1)[1].split(' ', 1)[0])
                scores[matchup] = winrate

            response.close()
            enemy_dict[hero['ImageURL']] = scores

            input = response.text
            wins = input.split('class="rgHeader">Map Name</th>', 1)[1].split('</thead><tbody>', 1)[1].split('</tbody>', 1)[0].split('/Maps/')[1:]

            scores = {}
            for win in wins:
                matchup, win = win.split('.png', 1)
                winrate = float(win.split('></div></td><td>', 1)[1].split(' ', 1)[0])
                scores[matchup] = winrate

            response.close()
            map_dict[hero['ImageURL']] = scores

    with open(dir_path + '/data/data_allies.json', 'w') as f:
        json.dump(team_dict, f)
    with open(dir_path + '/data/data_enemies.json', 'w') as f:
        json.dump(enemy_dict, f)
    with open(dir_path + '/data/data_maps.json', 'w') as f:
        json.dump(map_dict, f)

def open_allies():
    data = {}
    with open(dir_path + '/data/data_allies.json', 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def open_enemies():
    data = {}
    with open(dir_path + '/data/data_enemies.json', 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def open_maps():
    data = {}
    with open(dir_path + '/data/data_maps.json', 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def open_heroes():
    data = {}
    with open(dir_path + '/data/data_heroes.json', 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def fuse_dict(dict1, dict2):
    return_dict = {}
    for key, value in dict1.iteritems():
        if(dict2.has_key(key)):
            return_dict[key] = (dict2[key] + value)
        else:
            print key
    return return_dict

class HotsAnalyse(Screen):
    def __init__(self,**kwargs):
        super(HotsAnalyse, self).__init__(**kwargs)
        # runTouchApp(mainbutton)
    pass

class HotsApp(App):
    stack = ""
    allies = open_enemies()
    enemies = open_allies()
    maps = open_maps()
    heroes = open_heroes()
    neutral = {}
    selections = []
    selected_map = ""
    w = Window.width
    h = Window.height
    hero_buttons = []

    for hero in heroes:
        print hero['ImageURL']
        if (hero['ImageURL'] != 'Probius'):
            neutral[hero['ImageURL']] = 50

    for i in range (0,10):
        selections.append(neutral)

    def show_selected_value(self,spinner, text):
        index = self.hero_buttons.index(spinner)
        self.selections[index] = self.allies[text] if index < 5 else self.enemies[text]

        return_dict = {}
        for id, selection in enumerate(self.selections):
            if(id==0):
                return_dict = selection
            else:
                return_dict = fuse_dict(selection,return_dict)

        for key in return_dict:
            return_dict[key] = return_dict[key]/10

        self.stack.clear_widgets()
        dict_list = sorted(return_dict, key=return_dict.get,reverse=True)
        for hero in dict_list:
            self.stack.add_widget(Button(text=hero + "\n" + str(return_dict[hero]), size_hint=(0.142, 0.1), halign='center'))

    def build(self):
        dropdown = DropDown()

        for map in self.maps['Alarak']:
            btn = Button(text=map, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))


            dropdown.add_widget(btn)
        mainbutton = Button(text='Map', size_hint=(None, None))

        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        mainbutton.pos = (self.w/4, self.h-50)
        mainbutton.size_hint = (.5,.06)

        layout = FloatLayout(size=(self.w, self.h))
        layout.add_widget(mainbutton)
        MapImg.pos = (self.w/4-110, self.h-90)
        mainbutton.add_widget(MapImg)

        for i in range(0,10):
            self.hero_buttons.append(Spinner(
                # default value shown
                text='Player ' + str(i),
                # available values
                values=sorted(self.neutral),
                # just for positioning in our example
                size_hint=(None, None),
                size=(90, 50),
                pos=(5 + (self.w-100) * int(i / 5), self.h / 5 * (i % 5))))
            self.hero_buttons[i].bind(text=self.show_selected_value)
            layout.add_widget(self.hero_buttons[i])



        # spinner.bind(text=show_selected_value)

        # layout.add_widget(spinner)

        self.stack = StackLayout(size_hint=(0.7,0.8),pos=(120,0))
        dict_list = sorted(self.neutral, key=self.neutral.get, reverse=True)
        for hero in dict_list:
            self.stack.add_widget(
                Button(text=hero + "\n" + str(self.neutral[hero]), size_hint=(0.142, 0.1), halign='center'))

        layout.add_widget(self.stack)

        manager = ScreenManager()

        screen = HotsAnalyse(name='HotsAnalyse')

        screen.add_widget(layout)
        manager.add_widget(screen)


        return manager

if __name__ == '__main__':
    HotsApp().run()


# request_hero_data()
# allies =  open_allies()
# enemies =  open_enemies()
#
# print sorted(allies['Greymane'],key=allies['Greymane'].get)
# print sorted(enemies['Greymane'],key=enemies['Greymane'].get)
#
# new_dict = fuse_dict(allies['Greymane'],enemies['Greymane'])
# print allies['Greymane']
# print enemies['Greymane']