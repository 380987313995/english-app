import os
import json
import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout

# --- ЗАВАНТАЖЕННЯ СЛОВНИКА ---
try:
    with open('vocabulary.json', 'r', encoding='utf-8') as f:
        VOCAB_DATA = json.load(f)
except Exception as e:
    VOCAB_DATA = {}
    print(f"JSON Error: {e}")

PROGRAMMES = {
    "Programme 1": [("A Quiet Life", 1), ("A Date for the Theatre", 2), ("A Picnic", 3), ("Help Page", 4)],
    "Programme 2": [("Peter Parker", 5), ("Holiday Plans", 6), ("The Lost Tie", 7), ("Help Page", 8)],
    "Programme 3": [("A Road Accident", 9), ("A little Gossip", 10), ("A few Errands", 11), ("Help Page", 12)],
    "Programme 4": [("Work and Play", 13), ("Career Prospects", 14), ("After the Exams", 15), ("Help Page", 16)],
    "Programme 5": [("An Informal Invitation", 17), ("Detailed Directions", 18), ("Arranging the House", 19), ("Help Page", 20)],
    "Programme 6": [("Saturday Night Thoughts", 21), ("The Expert's Fee", 22), ("The Suspect", 23), ("Help Page", 24)],
    "Programme 7": [("U.K. Elections", 25), ("In Luck", 26), ("Sea or Air", 27), ("Help Page", 28)],
    "Programme 8": [("A Matter of Habit", 29), ("A Helpful Neighbour", 30), ("The Commuter", 31), ("Help Page", 32)],
    "Programme 9": [("Blunders", 33), ("Loyal Fans", 34), ("Linguistic Talent", 35), ("Help Page", 36)],
    "Programme 10": [("Get Well Soon", 37), ("Service, please", 38), ("The Season of Change", 39), ("Help Page", 40)],
}

class MainMenu(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Label(text="Професор Валєра: English", font_size='26sp', size_hint_y=0.15))
        scroll = ScrollView()
        grid = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))

        for p_name in sorted(PROGRAMMES.keys(), key=lambda x: int(x.split()[1])):
            btn = Button(text=p_name, size_hint_y=None, height=65, background_color=(0.2, 0.4, 0.8, 1))
            btn.bind(on_release=lambda x, n=p_name: self.select_prog(n))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def select_prog(self, name):
        self.manager.current_prog = name
        self.manager.current = 'prog_menu'

class ProgMenu(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(Button(text="< Назад", size_hint_y=None, height=50,
                                 on_release=lambda x: setattr(self.manager, 'current', 'main_menu')))
        for title, pg in PROGRAMMES[self.manager.current_prog]:
            btn = Button(text=f"Стор. {pg}: {title}", size_hint_y=None, height=70)
            btn.bind(on_release=lambda x, t=title, p=pg: self.open_work(t, p))
            layout.add_widget(btn)
        self.add_widget(layout)

    def open_work(self, title, pg):
        self.manager.active_title, self.manager.active_page = title, pg
        self.manager.current = 'work_screen'

class WorkScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.sound = None
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Button(text="Назад", size_hint_y=None, height=50, on_release=self.go_back))

        layout.add_widget(Button(text="ЧИТАТИ РОЗПОВІДЬ", size_hint_y=None, height=80, background_color=(0.2, 0.5, 0.8, 1),
                                 on_release=lambda x: setattr(self.manager, 'current', 'image_view')))

        if "Help" not in self.manager.active_title:
            layout.add_widget(Button(text="СЛОВНИК", size_hint_y=None, height=80, background_color=(0.8, 0.4, 0.2, 1),
                                     on_release=lambda x: setattr(self.manager, 'current', 'dict_view')))

            self.btn_audio = Button(text="СЛУХАТИ АУДІО", size_hint_y=None, height=80, background_color=(0.2, 0.7, 0.2, 1))
            self.btn_audio.bind(on_press=self.toggle_audio)
            layout.add_widget(self.btn_audio)
        else:
            layout.add_widget(Label(text="На цій сторінці лише текст", color=(0.7, 0.7, 0.7, 1)))

        self.add_widget(layout)

    def toggle_audio(self, inst):
        if not self.sound:
            p = str(self.manager.active_page).zfill(2)
            path = os.path.join('Mp3', f"{p}.mp3")
            if os.path.exists(path):
                self.sound = SoundLoader.load(path)
            else:
                self.btn_audio.text = "ФАЙЛ НЕ ЗНАЙДЕНО"
                return

        if self.sound.state == 'play':
            self.sound.stop()
            self.btn_audio.text = "СЛУХАТИ АУДІО"
        else:
            self.sound.play()
            self.btn_audio.text = "СТОП"

    def go_back(self, x):
        if self.sound: self.sound.stop()
        self.manager.current = 'prog_menu'

class ImageViewScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text="< Назад", size_hint_y=None, height=50,
                                 on_release=lambda x: setattr(self.manager, 'current', 'work_screen')))
        path = os.path.join('Texts', f"temp_page_{self.manager.active_page}.png")
        if os.path.exists(path):
            s = ScatterLayout(do_rotation=False)
            s.add_widget(Image(source=path, allow_stretch=True, keep_ratio=True))
            layout.add_widget(s)
        self.add_widget(layout)

class DictViewScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        nav = BoxLayout(size_hint_y=None, height=60, spacing=10)
        nav.add_widget(Button(text="Назад", on_release=lambda x: setattr(self.manager, 'current', 'work_screen')))
        self.btn_all = Button(text="Показати все", background_color=(0.2, 0.6, 0.8, 1))
        self.btn_all.bind(on_press=self.toggle_all)
        nav.add_widget(self.btn_all)
        layout.add_widget(nav)

        self.labels = []
        self.all_visible = False
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        box.bind(minimum_height=box.setter('height'))

        # Прямий пошук по номеру сторінки
        page_data = VOCAB_DATA.get(str(self.manager.active_page), {})

        for k, v in page_data.items():
            is_k_ukr = bool(re.search('[а-яА-ЯіїєґІЇЄҐ]', k))
            ukr, eng = (k, v) if is_k_ukr else (v, k)
            row = BoxLayout(size_hint_y=None, height=50, spacing=10)
            btn = Button(text=ukr, size_hint_x=0.5, background_color=(0.3, 0.3, 0.3, 1))
            lbl = Label(text=eng, size_hint_x=0.5, opacity=0, color=(1, 1, 0, 1), font_size='18sp')
            self.labels.append(lbl)
            btn.bind(on_press=lambda x, target=lbl: setattr(target, 'opacity', 1 if target.opacity == 0 else 0))
            row.add_widget(btn)
            row.add_widget(lbl)
            box.add_widget(row)

        if not page_data:
            box.add_widget(Label(text="Словник для цієї сторінки відсутній", halign="center"))

        scroll.add_widget(box)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def toggle_all(self, inst):
        self.all_visible = not self.all_visible
        for l in self.labels: l.opacity = 1 if self.all_visible else 0
        self.btn_all.text = "Сховати все" if self.all_visible else "Показати все"

class Manager(ScreenManager):
    current_prog = ""
    active_title = ""
    active_page = 0

class EnglishApp(App):
    def build(self):
        sm = Manager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(ProgMenu(name='prog_menu'))
        sm.add_widget(WorkScreen(name='work_screen'))
        sm.add_widget(ImageViewScreen(name='image_view'))
        sm.add_widget(DictViewScreen(name='dict_view'))
        return sm

if __name__ == '__main__':
    EnglishApp().run()