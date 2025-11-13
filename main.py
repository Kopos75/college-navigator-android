from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog  # ← ДОБАВИЛОСЬ

Window.size = (400, 700)


class LocationPoint:
    def __init__(self, id, title, cabinet, building, floor, route, department, photo):
        self.id = id
        self.title = title
        self.cabinet = cabinet
        self.building = building
        self.floor = floor
        self.route = route
        self.department = department  # "СПО" или "НПО"
        self.photo = photo            # путь к фото


# Данные по точкам с фото-заглушками
LOCATIONS = [
    LocationPoint(
        id='director_spo',
        title='К директору (СПО)',
        cabinet='каб. 201',
        building='Главный корпус',
        floor='2 этаж',
        route='Зайдите через главный вход, поверните направо и идите до конца коридора, '
              'поверните налево, поднимитесь на 2 этаж. Железная дверь "Приемная".',
        department='СПО',
        photo='images/foto1.png.jpg',
    ),
    LocationPoint(
        id='study_spo',
        title='Учебная часть (СПО)',
        cabinet='каб. 305',
        building='Главный корпус',
        floor='3 этаж',
        route='Зайдите через главный вход, поверните налево и идите до конца коридора, '
              'поверните направо, поднимайтесь на 3 этаж, затем поверните направо, '
              'пройдите чуть подальше — слева дверь "Учебная часть".',
        department='СПО',
        photo='images/foto2.png.jpg',
    ),
    LocationPoint(
        id='canteen',
        title='Столовая',
        cabinet='—',
        building='Левое крыло',
        floor='1 этаж',
        route='От главного входа идите прямо до конца коридора, затем налево. '
              'Столовая по правой стороне.',
        department='СПО',  # при желании можно показывать и для НПО
        photo='images/foto3.png.jpg',
    ),
    LocationPoint(
        id='director_npo',
        title='К директору (НПО)',
        cabinet='каб. 15',
        building='Корпус НПО',
        floor='2 этаж',
        route='Зайдите в корпус НПО, поднимитесь на 2 этаж, кабинет 15 будет справа по коридору.',
        department='НПО',
        photo='images/foto4.png.jpg',
    ),
]


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_department = 'СПО'
        self.info_dialog = None  # ← ДЛЯ ДИАЛОГА «ДЛЯ СПРАВКИ»

        root = MDBoxLayout(orientation='vertical')

        # Верхняя панель (AppBar)
        toolbar = MDTopAppBar(
            title="Навигатор колледжа",
            elevation=4,
            pos_hint={"top": 1},
        )
        root.add_widget(toolbar)

        # Основное содержимое под тулбаром
        content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        root.add_widget(content)

        # Фото колледжа в карточке
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=200,
            radius=[16, 16, 16, 16],
            elevation=4,
        )
        img = FitImage(
            source='images/logo.png',
        )
        card.add_widget(img)
        content.add_widget(card)

        # Переключатель СПО / НПО (две Material-кнопки)
        dep_layout = MDBoxLayout(
            size_hint=(1, None),
            height=50,
            spacing=10,
            padding=(0, 10, 0, 0),
        )

        self.btn_spo = MDRaisedButton(
            text="СПО",
            on_release=lambda *_: self.set_department('СПО'),
        )
        self.btn_npo = MDFlatButton(
            text="НПО",
            on_release=lambda *_: self.set_department('НПО'),
        )

        dep_layout.add_widget(self.btn_spo)
        dep_layout.add_widget(self.btn_npo)
        content.add_widget(dep_layout)

        # Заголовок
        title_label = MDLabel(
            text="Куда хотите пройти?",
            font_style="H6",
            size_hint_y=None,
            height=40,
        )
        content.add_widget(title_label)

        # ← КНОПКА «ДЛЯ СПРАВКИ»
        info_btn = MDRaisedButton(
            text="Для справки",
            size_hint=(1, None),
            height=40,
            on_release=self.show_hint,
        )
        content.add_widget(info_btn)

        # Список направлений в ScrollView + MDList
        scroll = ScrollView()
        self.list_widget = MDList()
        scroll.add_widget(self.list_widget)
        content.add_widget(scroll)

        self.add_widget(root)

        self.update_buttons()
        self.update_department_buttons_style()

    def set_department(self, dep):
        self.current_department = dep
        self.update_department_buttons_style()
        self.update_buttons()

    def update_department_buttons_style(self):
        app = MDApp.get_running_app()
        primary = app.theme_cls.primary_color

        if self.current_department == 'СПО':
            self.btn_spo.md_bg_color = primary
            self.btn_spo.text_color = (1, 1, 1, 1)
            self.btn_npo.md_bg_color = (0, 0, 0, 0)
            self.btn_npo.text_color = (0, 0, 0, 1)
        else:
            self.btn_npo.md_bg_color = primary
            self.btn_npo.text_color = (1, 1, 1, 1)
            self.btn_spo.md_bg_color = (0, 0, 0, 0)
            self.btn_spo.text_color = (0, 0, 0, 1)

    def update_buttons(self):
        self.list_widget.clear_widgets()
        dept_locations = [loc for loc in LOCATIONS if loc.department == self.current_department]

        for loc in dept_locations:
            item = OneLineListItem(
                text=loc.title,
                on_release=lambda instance, loc=loc: self.open_location(loc),
            )
            self.list_widget.add_widget(item)

    def open_location(self, location: LocationPoint):
        app = MDApp.get_running_app()
        app.location_screen.set_location(location)
        app.sm.current = 'location'

    # ==== НОВЫЕ МЕТОДЫ ДЛЯ ДИАЛОГА ====
    def show_hint(self, *args):
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                title="Для справки",
                text=(
                    "Если номер кабинета начинается с 2 — это второй этаж.\n"
                    "Если начинается с 3 — это третий этаж."
                ),
                buttons=[
                    MDFlatButton(
                        text="Понятно",
                        on_release=self.close_hint
                    )
                ],
            )
        self.info_dialog.open()

    def close_hint(self, instance):
        if self.info_dialog:
            self.info_dialog.dismiss()


class LocationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = MDBoxLayout(orientation='vertical')
        self.add_widget(root)

        # Верхняя панель с кнопкой "назад"
        self.toolbar = MDTopAppBar(
            title="",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        root.add_widget(self.toolbar)

        # Основной контент
        content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        root.add_widget(content)

        # Фото локации
        self.image_widget = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=200,
            radius=[16, 16, 16, 16],
            elevation=4,
        )
        self.fit_image = FitImage(source="")
        self.image_widget.add_widget(self.fit_image)
        content.add_widget(self.image_widget)

        # Название
        self.title_label = MDLabel(
            text="",
            font_style="H6",
            size_hint_y=None,
            height=40,
        )
        content.add_widget(self.title_label)

        # Описание (Markup)
        self.info_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            markup=True,
        )
        self.info_label.bind(size=self._update_text_size)
        content.add_widget(self.info_label)

    def _update_text_size(self, *args):
        self.info_label.text_size = self.info_label.size

    def set_location(self, location: LocationPoint):
        self.toolbar.title = location.title
        self.title_label.text = location.title
        self.fit_image.source = location.photo

        parts = []
        if location.building:
            parts.append(f"[b]Корпус:[/b] {location.building}")
        if location.floor:
            parts.append(f"[b]Этаж:[/b] {location.floor}")
        if location.cabinet and location.cabinet != '—':
            parts.append(f"[b]Кабинет:[/b] {location.cabinet}")
        parts.append(f"\n[b]Как пройти:[/b]\n{location.route}")

        self.info_label.text = "\n".join(parts)

    def go_back(self, *_args):
        app = MDApp.get_running_app()
        app.sm.current = 'main'


class CollegeNavigatorMDApp(MDApp):
    def build(self):
        self.title = "Навигатор колледжа"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        self.sm = ScreenManager(transition=FadeTransition())

        self.main_screen = MainScreen(name='main')
        self.location_screen = LocationScreen(name='location')

        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.location_screen)

        return self.sm


if __name__ == "__main__":
    CollegeNavigatorMDApp().run()
